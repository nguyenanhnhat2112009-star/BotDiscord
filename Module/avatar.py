import disnake
from disnake.ext import commands
from disnake.ui import View, Button
from datetime import datetime
from typing import Optional
from utils.ClientUser import ClientUser

COLORS = {
    "pink": 0xFFB6C1,
    "purple": 0xDDA0DD,
    "blue": 0x87CEEB,
    "green": 0x98FF98,
    "orange": 0xFFB347,
    "yellow": 0xFFEB3B
}

# ═══════════════════════════════════════════════════════════════
#                    🖼️ AVATAR VIEW
# ═══════════════════════════════════════════════════════════════

class AvatarView(View):
    def __init__(self, user: disnake.User, author: disnake.User):
        super().__init__(timeout=300)
        self.user = user
        self.author = author

    @disnake.ui.button(label="📥 Copy PNG", emoji="🖼️", style=disnake.ButtonStyle.secondary)
    async def copy_png_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.author.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng nút này!", ephemeral=True)
            return
        
        avatar_png = self.user.display_avatar.with_format('png').url
        await inter.response.send_message(f"```\n{avatar_png}\n```", ephemeral=True)

    @disnake.ui.button(label="📥 Copy JPG", emoji="🖼️", style=disnake.ButtonStyle.secondary)
    async def copy_jpg_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.author.id:
            return
        
        avatar_jpg = self.user.display_avatar.with_format('jpg').url
        await inter.response.send_message(f"```\n{avatar_jpg}\n```", ephemeral=True)

    @disnake.ui.button(label="📥 Copy WebP", emoji="🖼️", style=disnake.ButtonStyle.secondary)
    async def copy_webp_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.author.id:
            return
        
        avatar_webp = self.user.display_avatar.with_format('webp').url
        await inter.response.send_message(f"```\n{avatar_webp}\n```", ephemeral=True)

    @disnake.ui.button(label="❌ Đóng", emoji="❌", style=disnake.ButtonStyle.danger)
    async def close_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.author.id:
            return
        await inter.response.defer()
        await inter.message.delete()


# ═══════════════════════════════════════════════════════════════
#                    🖼️ AVATAR COG
# ═══════════════════════════════════════════════════════════════

class Avatar(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(name="avatar", description="👩‍🎨 Xem avatar của người dùng")
    async def avatar(
        self, 
        interaction: disnake.ApplicationCommandInteraction,
        user: Optional[disnake.User] = None
    ):
        """Display user's avatar with cute interface"""
        target_user = user or interaction.author
        
        avatar_url = target_user.display_avatar.url
        avatar_png = target_user.display_avatar.with_format('png').url
        avatar_jpg = target_user.display_avatar.with_format('jpg').url
        avatar_webp = target_user.display_avatar.with_format('webp').url
        
        avatar_gif = None
        if target_user.display_avatar.is_animated():
            avatar_gif = target_user.display_avatar.with_format('gif').url

        embed = disnake.Embed(
            title=f"👩‍🎨 Avatar của {target_user.display_name}",
            description="Xem và tải xuống avatar",
            color=COLORS["pink"],
            timestamp=datetime.now()
        )

        embed.set_image(url=avatar_url)
        
        embed.add_field(
            name="👤 Thông tin",
            value=f"**Tên:** {target_user.display_name}\n**Username:** {target_user.name}\n**ID:** `{target_user.id}`",
            inline=False
        )

        # Download links
        download_links = f"[PNG]({avatar_png}) • [JPG]({avatar_jpg}) • [WebP]({avatar_webp})"
        if avatar_gif:
            download_links += f" • [GIF]({avatar_gif}) 🎬"
        
        embed.add_field(name="📥 Tải xuống", value=download_links, inline=False)

        # Sizes
        sizes = ["64", "128", "256", "512", "1024", "2048"]
        size_links = " • ".join([f"[{size}]({target_user.display_avatar.with_size(int(size)).url})" for size in sizes])
        embed.add_field(name="📏 Kích thước", value=size_links, inline=False)

        embed.set_footer(text=f"💖 Yêu cầu bởi {interaction.author.display_name}", icon_url=interaction.author.display_avatar.url)

        view = AvatarView(target_user, interaction.author)
        await interaction.response.send_message(embed=embed, view=view)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(name="server-avatar", description="🏠 Xem avatar server của thành viên")
    async def server_avatar(
        self, 
        interaction: disnake.ApplicationCommandInteraction,
        member: Optional[disnake.Member] = None
    ):
        """Display member's server-specific avatar"""
        if not interaction.guild:
            embed = disnake.Embed(title="❌ Chỉ dùng trong server", color=0xFF6B6B)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        target_member = member or interaction.author
        
        if target_member.guild_avatar is None:
            embed = disnake.Embed(
                title="ℹ️ Không có avatar server",
                description=f"{target_member.display_name} không có avatar riêng cho server này",
                color=COLORS["orange"],
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=target_member.display_avatar.url)
        else:
            server_avatar_url = target_member.guild_avatar.url
            server_avatar_png = target_member.guild_avatar.with_format('png').url
            server_avatar_jpg = target_member.guild_avatar.with_format('jpg').url
            server_avatar_webp = target_member.guild_avatar.with_format('webp').url
            
            server_avatar_gif = None
            if target_member.guild_avatar.is_animated():
                server_avatar_gif = target_member.guild_avatar.with_format('gif').url

            embed = disnake.Embed(
                title=f"🏠 Avatar Server - {target_member.display_name}",
                color=COLORS["blue"],
                timestamp=datetime.now()
            )

            embed.set_image(url=server_avatar_url)
            
            embed.add_field(
                name="👤 Thông tin",
                value=f"**Tên:** {target_member.display_name}\n**Username:** {target_member.name}\n**ID:** `{target_member.id}`",
                inline=False
            )

            download_links = f"[PNG]({server_avatar_png}) • [JPG]({server_avatar_jpg}) • [WebP]({server_avatar_webp})"
            if server_avatar_gif:
                download_links += f" • [GIF]({server_avatar_gif}) 🎬"
            
            embed.add_field(name="📥 Tải xuống", value=download_links, inline=False)

        embed.set_footer(text=f"💖 Yêu cầu bởi {interaction.author.display_name}", icon_url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="avatar-compare", description="🔄 So sánh avatar của hai người dùng")
    async def avatar_compare(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user1: disnake.User,
        user2: Optional[disnake.User] = None
    ):
        """Compare avatars of two users"""
        user2 = user2 or interaction.author
        
        embed = disnake.Embed(
            title="🔄 So Sánh Avatar",
            color=COLORS["purple"],
            timestamp=datetime.now()
        )

        embed.add_field(
            name=f"👤 {user1.display_name}",
            value=f"**ID:** `{user1.id}`\n[Xem]({user1.display_avatar.url})",
            inline=True
        )

        embed.add_field(
            name=f"👤 {user2.display_name}",
            value=f"**ID:** `{user2.id}`\n[Xem]({user2.display_avatar.url})",
            inline=True
        )

        embed.set_thumbnail(url=user1.display_avatar.url)
        embed.set_image(url=user2.display_avatar.url)

        embed.set_footer(text=f"💖 Yêu cầu bởi {interaction.author.display_name}", icon_url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(name="banner", description="🎨 Xem banner của người dùng")
    async def banner(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user: Optional[disnake.User] = None
    ):
        """Display user's banner"""
        target_user = user or interaction.author

        try:
            fetched_user = await self.bot.fetch_user(target_user.id)
        except:
            embed = disnake.Embed(title="❌ Lỗi", description="Không thể lấy thông tin!", color=0xFF6B6B)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if fetched_user.banner is None:
            embed = disnake.Embed(
                title="ℹ️ Không có banner",
                description=f"{target_user.display_name} không có banner",
                color=COLORS["orange"],
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=target_user.display_avatar.url)
        else:
            banner_url = fetched_user.banner.url
            banner_png = fetched_user.banner.with_format('png').url
            banner_jpg = fetched_user.banner.with_format('jpg').url
            banner_webp = fetched_user.banner.with_format('webp').url

            banner_gif = None
            if fetched_user.banner.is_animated():
                banner_gif = fetched_user.banner.with_format('gif').url

            embed = disnake.Embed(
                title=f"🎨 Banner - {target_user.display_name}",
                color=fetched_user.accent_color or COLORS["pink"],
                timestamp=datetime.now()
            )

            embed.set_image(url=banner_url)

            embed.add_field(
                name="👤 Thông tin",
                value=f"**Tên:** {target_user.display_name}\n**ID:** `{target_user.id}`",
                inline=False
            )

            download_links = f"[PNG]({banner_png}) • [JPG]({banner_jpg}) • [WebP]({banner_webp})"
            if banner_gif:
                download_links += f" • [GIF]({banner_gif}) 🎬"

            embed.add_field(name="📥 Tải xuống", value=download_links, inline=False)

            if fetched_user.accent_color:
                embed.add_field(name="🌈 Màu chủ đạo", value=f"`{str(fetched_user.accent_color)}`", inline=True)

        embed.set_footer(text=f"💖 Yêu cầu bởi {interaction.author.display_name}", icon_url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="user-info", description="📋 Xem thông tin chi tiết của người dùng")
    async def user_info(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        user: Optional[disnake.User] = None
    ):
        """Display detailed user information"""
        target_user = user or interaction.author

        try:
            fetched_user = await self.bot.fetch_user(target_user.id)
        except:
            embed = disnake.Embed(title="❌ Lỗi", description="Không thể lấy thông tin!", color=0xFF6B6B)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = disnake.Embed(
            title=f"📋 Thông Tin - {target_user.display_name}",
            color=fetched_user.accent_color or COLORS["pink"],
            timestamp=datetime.now()
        )

        created_at = target_user.created_at.strftime("%d/%m/%Y %H:%M")
        account_age = (datetime.now() - target_user.created_at.replace(tzinfo=None)).days

        basic_info = f"""
**Tên hiển thị:** {target_user.display_name}
**Username:** {target_user.name}
**ID:** `{target_user.id}`
**Tạo:** {created_at}
**Tuổi:** {account_age} ngày
        """
        embed.add_field(name="👤 Cơ bản", value=basic_info, inline=False)

        avatar_info = f"[Xem]({target_user.display_avatar.url})"
        if target_user.display_avatar.is_animated():
            avatar_info += " • 🎬"
        embed.add_field(name="🖼️ Avatar", value=avatar_info, inline=True)

        banner_info = "Không có" if not fetched_user.banner else f"[Xem]({fetched_user.banner.url})" + (" • 🎬" if fetched_user.banner.is_animated() else "")
        embed.add_field(name="🎨 Banner", value=banner_info, inline=True)

        embed.set_thumbnail(url=target_user.display_avatar.url)
        if fetched_user.banner:
            embed.set_image(url=fetched_user.banner.url)

        embed.set_footer(text=f"💖 Yêu cầu bởi {interaction.author.display_name}", icon_url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # Prefix commands
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="avatar", aliases=["av", "pfp"])
    async def avatar_prefix(self, ctx, user: Optional[disnake.User] = None):
        """Prefix avatar command"""
        if ctx.author.bot:
            return
        
        target_user = user or ctx.author
        avatar_url = target_user.display_avatar.url

        embed = disnake.Embed(
            title=f"👩‍🎨 Avatar - {target_user.display_name}",
            color=COLORS["pink"],
            timestamp=datetime.now()
        )
        embed.set_image(url=avatar_url)
        embed.add_field(name="🔗 Link", value=f"[Mở]({avatar_url})", inline=False)
        embed.set_footer(text=f"💖 Yêu cầu bởi {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        view = AvatarView(target_user, ctx.author)
        await ctx.send(embed=embed, view=view)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="banner", aliases=["bn"])
    async def banner_prefix(self, ctx, user: Optional[disnake.User] = None):
        """Prefix banner command"""
        if ctx.author.bot:
            return

        target_user = user or ctx.author
        try:
            fetched_user = await self.bot.fetch_user(target_user.id)
        except:
            await ctx.send("❌ Không thể lấy thông tin!")
            return

        if not fetched_user.banner:
            await ctx.send(f"ℹ️ {target_user.display_name} không có banner")
            return

        embed = disnake.Embed(
            title=f"🎨 Banner - {target_user.display_name}",
            color=fetched_user.accent_color or COLORS["pink"]
        )
        embed.set_image(url=fetched_user.banner.url)
        embed.set_footer(text=f"💖 Yêu cầu bởi {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="userinfo", aliases=["ui", "info"])
    async def userinfo_prefix(self, ctx, user: Optional[disnake.User] = None):
        """Prefix userinfo command"""
        if ctx.author.bot:
            return

        target_user = user or ctx.author
        try:
            fetched_user = await self.bot.fetch_user(target_user.id)
        except:
            await ctx.send("❌ Không thể lấy thông tin!")
            return

        embed = disnake.Embed(
            title=f"📋 {target_user.display_name}",
            color=fetched_user.accent_color or COLORS["pink"]
        )
        
        created_at = target_user.created_at.strftime("%d/%m/%Y")
        account_age = (datetime.now() - target_user.created_at.replace(tzinfo=None)).days
        
        embed.add_field(name="ID", value=f"`{target_user.id}`", inline=True)
        embed.add_field(name="Tạo", value=f"{created_at} ({account_age}d)", inline=True)
        embed.set_thumbnail(url=target_user.display_avatar.url)
        embed.set_footer(text=f"💖 Yêu cầu bởi {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        
        await ctx.send(embed=embed)

def setup(bot: ClientUser):
    bot.add_cog(Avatar(bot))
