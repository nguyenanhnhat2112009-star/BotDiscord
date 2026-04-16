r"""A module containing a :class:`NodePool`, used to manage :class:`Node`\s."""
# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from functools import partial
from logging import getLogger
from random import choice
from typing import TYPE_CHECKING, Any, Generic, TypeVar, Union, cast

import os
import warnings

from .errors import NoNodesAvailable, PlayerNotConnected
from .node import Node
from .strategy import Strategy, StrategyCallable, call_strategy
from .type_variables import ClientT
from .utils import classproperty

if TYPE_CHECKING:
    from typing import ClassVar

    import aiohttp

    from .player import Player
    from .region import Group, Region, VoiceRegion


T = TypeVar("T")
__all__ = ("NodePool",)

_mafic_strict = os.getenv("MAFIC_STRICT", "false").lower() in ("1", "true", "yes")
# If strict mode is off, suppress the specific message emitted by mafic about Lavalink version.
# This prevents the repeated message: "The version of Lavalink you are using is not supported by Mafic..."
if not _mafic_strict:
    # ignore warnings whose message starts with that text (keeps other warnings intact)
    warnings.filterwarnings(
        "ignore",
        message=r"The version of Lavalink you are using is not supported by Mafic.*",
    )
# If strict mode is on, keep default behavior (warning will be shown).

_log = getLogger(__name__)
# enable logging for easier debugging with Lavalink v4
_log.disabled = False

StrategyList = Union[
    StrategyCallable[ClientT],
    Sequence[Strategy],
    Sequence[StrategyCallable[ClientT]],
    Sequence[Union[Strategy, StrategyCallable[ClientT]]],
]
"""A type hint for a list of strategies to select the best node.

This can either be:

- A single :data:`.StrategyCallable`.
- A sequence of :class:`.Strategy`\\s.
- A sequence of :data:`.StrategyCallable`\\s.
- A sequence of :class:`.Strategy`\\s and :data:`.StrategyCallable`\\s.
"""


class NodePool(Generic[ClientT]):
    """A class that manages nodes and chooses them based on strategies.

    Parameters
    ----------
    client:
        The client to use to connect to the nodes.
    default_strategies:
        The default strategies to use when selecting a node. Defaults to
        [:attr:`Strategy.SHARD`, :attr:`Strategy.LOCATION`, :attr:`Strategy.USAGE`].
    """

    __slots__ = ()

    # Generics as expected, do not work in class variables.
    # Don't fear, the public methods using this are typed well.
    _nodes: ClassVar[dict[str, Node[Any]]] = {}
    _client: ClientT | None = None

    def __init__(
        self,
        client: ClientT,
        default_strategies: StrategyList[ClientT] | None = None,
    ) -> None:
        NodePool._client = client

        NodePool._default_strategies = (
            [
                Strategy.SHARD,
                Strategy.LOCATION,
                Strategy.USAGE,
            ]
            if default_strategies is None
            else default_strategies
        )

    @classproperty
    def label_to_node(cls) -> dict[str, Node[ClientT]]:
        """Get a mapping node labels to nodes."""
        return cls._nodes

    @classproperty
    def nodes(cls) -> list[Node[ClientT]]:
        """Get the list of all available nodes."""
        return list(filter(lambda n: n.available, cls._nodes.values()))

    async def create_node(
        self,
        *,
        host: str,
        port: int,
        label: str,
        password: str,
        secure: bool = False,
        heartbeat: int = 30,
        timeout: float = 10,
        session: aiohttp.ClientSession | None = None,
        resume_key: str | None = None,
        regions: Sequence[Group | Region | VoiceRegion] | None = None,
        shard_ids: Sequence[int] | None = None,
        resuming_session_id: str | None = None,
        player_cls: type[Player[ClientT]] | None = None,
    ) -> Node[ClientT]:
        r"""Create a node and connect it.

        The parameters here relate to :class:`Node`.

        Parameters
        ----------
        host:
            The host of the node to connect to.
        port:
            The port of the node to connect to.
        label:
            The label of the node used to identify it.
        password:
            The password of the node to authenticate.
        secure:
            Whether to use SSL (TLS) or not.
        heartbeat:
            The interval to send heartbeats to the node websocket connection.
        timeout:
            The timeout to use for the node websocket connection.
        session: :data:`~typing.Optional`\[:class:`aiohttp.ClientSession`]
            The session to use for the node websocket connection.
        resume_key:
            The key to use when resuming the node.
            If not provided, the key will be generated from the host, port and label.

            .. warning::

                This is ignored in lavalink V4, use ``resuming_session_id`` instead.
        regions:
            The voice regions that the node can be used in.
            This is used to determine when to use this node.
        shard_ids:
            The shard IDs that the node can be used in.
            This is used to determine when to use this node.
        resuming_session_id:
            The session ID to use when resuming the node.
            If not provided, the node will not resume.

            This should be stored from :func:`~mafic.on_node_ready` with
            :attr:`session_id` to resume the session and gain control of the players.
            If the node is not resuming, players will be destroyed if Lavalink loses
            connection to us.

            .. versionadded:: 2.2
        player_cls:
            The player class to use for this node when resuming.

            .. versionadded:: 2.8

        Returns
        -------
        :class:`Node`
            The created node.

        Raises
        ------
        RuntimeError
            If the node pool has not been initialized.
        """
        if self._client is None:
            msg = "NodePool has not been initialized."
            raise RuntimeError(msg)

        # Compatibility: if resume_key passed for older lavalink, but v4 uses resuming_session_id,
        # prefer resuming_session_id if provided, else fall back to resume_key (non-fatal).
        resuming = resuming_session_id or resume_key

        node = Node(
            host=host,
            port=port,
            label=label,
            password=password,
            client=self._client,
            secure=secure,
            heartbeat=heartbeat,
            timeout=timeout,
            session=session,
            resume_key=resume_key,
            regions=regions,
            shard_ids=shard_ids,
            resuming_session_id=resuming,
        )

        # add_node now protects against node.connect failure
        await self.add_node(node, player_cls=player_cls)
        return node

    async def add_node(
        self, node: Node[ClientT], *, player_cls: type[Player[ClientT]] | None = None
    ) -> None:
        """Add an existing node to this pool.

        .. note::

            You generally do not want this, use :meth:`create_node` instead.
            This is used for after running :meth:`remove_node` to re-add the node
            if it has been restarted.

        .. versionadded:: 2.7

        Parameters
        ----------
        node:
            The node to add.
        player:
            The player class to use for this node when resuming.

            .. versionadded:: 2.8
        """
        _log.info("Created node, connecting it...", extra={"label": node.label})
        try:
            # protect against connection failure on node.connect
            await node.connect(player_cls=player_cls)
        except Exception as e:
            _log.exception("Failed to connect node %s, will not add to pool", node.label)
            # ensure node closed to free resources
            try:
                await node.close()
            except Exception:
                pass
            return

        # only add node to pool if connected successfully
        self._nodes[node.label] = node

    async def remove_node(
        self, node: Node[ClientT] | str, *, transfer_players: bool = True
    ) -> None:
        """Remove a node from the pool.

        .. versionadded:: 2.6

        Parameters
        ----------
        node:
            The node to remove.
        transfer_players:
            Whether to transfer players to other nodes or destroy them.
        """
        if isinstance(node, str):
            node = self._nodes[node]

        # Remove prematurely so it is not chosen.
        if node.label in self._nodes:
            del self._nodes[node.label]

        if transfer_players:

            async def transfer_player(player: Player[ClientT]) -> None:
                try:
                    target = self.get_node(
                        guild_id=player.guild.id,
                        endpoint=player.endpoint,  # pyright: ignore[reportPrivateUsage]
                    )
                    await player.transfer_to(target)
                except (RuntimeError, NoNodesAvailable, PlayerNotConnected):
                    _log.error(
                        "Failed to transfer player %d, destroying it...",
                        player.guild.id,
                        exc_info=True,
                        extra={"label": node.label},
                    )
                    await player.destroy()

            tasks = [transfer_player(player) for player in node.players]
            await asyncio.gather(*tasks)
        else:

            async def destroy_player(player: Player[ClientT]) -> None:
                _log.debug(
                    "Destroying player %d due to node removal...",
                    player.guild.id,
                    extra={"label": node.label},
                )
                await player.destroy()

            tasks = [destroy_player(player) for player in node.players]
            await asyncio.gather(*tasks)

        await node.close()

    async def close(self) -> None:
        """Close all nodes in the pool.

        .. versionadded:: 2.6
        """
        for node in list(self._nodes.values()):
            try:
                await node.close()
            except Exception:
                _log.exception("Error closing node %s", getattr(node, "label", "unknown"))

    @classmethod
    def get_node(
        cls,
        *,
        guild_id: str | int,
        endpoint: str | None,
        strategies: StrategyList[ClientT] | None = None,
    ) -> Node[ClientT]:
        """Get a node based on the given strategies.

        Parameters
        ----------
        guild_id:
            The guild ID to get a node for.
        endpoint:
            The endpoint to get a node for.
        strategies:
            The strategies to use to get a node. If not provided, the default
            strategies will be used.

        Returns
        -------
        :class:`Node`
            The node to use.

        Raises
        ------
        RuntimeError
            If the node pool has not been initialized.
        """
        if cls._client is None:
            msg = "NodePool has not been initialized."
            raise RuntimeError(msg)

        actual_strategies: Sequence[StrategyCallable[ClientT] | Strategy]

        strategies = strategies or cls._default_strategies

        actual_strategies = [strategies] if callable(strategies) else strategies

        # It is a classproperty.
        # fmt: off
        nodes = cast("list[Node[ClientT]]", cls.nodes)  # pyright: ignore  # noqa: PGH003
        # fmt: on

        # if no nodes available, fail early
        if not nodes:
            raise NoNodesAvailable

        for strategy in actual_strategies:
            if isinstance(strategy, Strategy):
                strategy_callable = partial(call_strategy, strategy)
            else:
                strategy_callable = strategy

            # Strategy callable must always return a sequence; protect against bad implementations
            try:
                nodes = strategy_callable(
                    nodes, int(guild_id), getattr(cls._client, "shard_count", None), endpoint
                )
            except Exception:
                _log.exception("Strategy %s raised an exception; skipping it.", getattr(strategy, "__name__", str(strategy)))
                continue

            # ensure nodes is a sequence and filter by availability
            nodes = [n for n in nodes if getattr(n, "available", True)]

            _log.debug(
                "Strategy %s returned nodes %s.",
                strategy.__name__ if callable(strategy) else getattr(strategy, "name", str(strategy)),
                ", ".join(n.label for n in nodes),
            )

            if len(nodes) == 1:
                return nodes[0]
            elif len(nodes) == 0:
                raise NoNodesAvailable

        # final fallback: pick random from remaining nodes
        if not nodes:
            raise NoNodesAvailable
        return choice(nodes)

    @classmethod
    def get_random_node(cls) -> Node[ClientT]:
        """Get a random node.

        Returns
        -------
        :class:`Node`
            The random node.

        Raises
        ------
        ValueError
            If there are no nodes.
        """
        # It is a classproperty.
        nodes = cast(
            "list[Node[ClientT]]", cls.nodes  # pyright: ignore  # noqa: PGH003
        )

        if not nodes:
            raise NoNodesAvailable

        return choice(nodes)
