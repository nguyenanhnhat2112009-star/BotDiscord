import disnake
from disnake.ext import commands
from datetime import datetime
from typing import Optional
from utils.ClientUser import ClientUser

COLORS = {
    "pink": 0xFFB6C1,
    "purple": 0xDDA0DD,
    "blue": 0x87CEEB,
    "green": 0x98FF98,
    "red": 0xFF6B6B,
    "orange": 0xFFB347
}

class InviteDropdown(disnake.ui.StringSelect):
    def __init__(self, view_instance):
        self.view_instance = view_instance
        
        options = [
            disnake.SelectOption(
                label="🔗 Quyền Đầy Đủ",
                description="Administrator - Tất cả quyền",
                value="full",
                emoji="🔓"
            ),
            disnake.SelectOption(
                label="⭐ Quyền Khuyến Nghị",
                description="Recommended - Chỉ quyền cần thiết",
                value="recommended",
                emoji="✨"
            ),
            disnake.SelectOption(
                label="🔒 Quyền Tối Thiểu",
                description="Minimal - An toàn nhất",
                value="minimal",
                emoji="🛡️"
            ),
        ]
        
        super().__init__(
            placeholder="✨ Chọn loại invite...",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        if inter.user.id != self.view_instance.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        
        await inter.response.defer()
        embed = self.view_instance.create_permission_embed(self.values[0])
        await inter.edit_original_response(embed=embed, view=self.view_instance)

class InviteView(disnake.ui.View):
    def __init__(self, bot: ClientUser, user: disnake.User):
        super().__init__(timeout=300)
        self.bot = bot
        self.user = user
        self.current_view = "main"

        # Permission sets
        self.full_permissions = disnake.Permissions(administrator=True)

        self.recommended_permissions = disnake.Permissions(
            manage_channels=True, manage_roles=True, manage_messages=True,
            embed_links=True, attach_files=True, read_message_history=True,
            use_external_emojis=True, add_reactions=True, connect=True, speak=True,
            use_voice_activation=True, priority_speaker=True, moderate_members=True,
            kick_members=True, ban_members=True, send_messages=True, view_channel=True
        )

        self.minimal_permissions = disnake.Permissions(
            send_messages=True, embed_links=True, connect=True, speak=True,
            use_voice_activation=True, view_channel=True
        )
        
        self.add_item(InviteDropdown(self))

    def create_main_embed(self) -> disnake.Embed:
        """Main invite menu embed"""
        embed = disnake.Embed(
            title="🎀 Mời Hatsune Miku Bot vào Server!",
            description="""
╭─────────── • ◆ • ───────────╮
   **Hãy thêm bot vào server của bạn ngay!**
╰─────────── • ◆ • ───────────╯

💖 **Bot được đặc biệt thiết kế với:**
✨ Giao diện cute và dễ sử dụng
🎵 Hệ thống nhạc chất lượng cao
🛡️ Quản lý server chuyên nghiệp
🎮 Game và tiện ích vui nhộn
🎫 Ticket system hiệu quả
🚀 Performance tối ưu

─────────────────────────────

📋 **Chọn loại invite phù hợp bạn:**
            """,
            color=COLORS["pink"],
            timestamp=datetime.now()
        )

        # Add invite options
        embed.add_field(
            name="🔓 Quyền Đầy Đủ (Administrator)",
            value="✅ Tất cả quyền\n✅ Dễ setup\n⚠️ Cần tin tưởng hoàn toàn",
            inline=True
        )

        embed.add_field(
            name="✨ Quyền Khuyến Nghị (Recommended)",
            value="✅ Đủ chức năng\n✅ An toàn\n✅ Tốt nhất",
            inline=True
        )

        embed.add_field(
            name="🛡️ Quyền Tối Thiểu (Minimal)",
            value="✅ An toàn nhất\n⚠️ Hạn chế\n⚠️ Cần setup thêm",
            inline=True
        )

        # Bot stats
        embed.add_field(
            name="📊 Thống kê Bot",
            value=f"""
```
🏠 Servers: {len(self.bot.guilds)}
👥 Users: {len(self.bot.users)}
🏓 Ping: {round(self.bot.latency * 1000)}ms
```
            """,
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"💖 Chọn dropdown menu để mời bot • Requested by {self.user.display_name}",
            icon_url=self.user.display_avatar.url
        )

        return embed

    def create_permission_embed(self, perm_type: str) -> disnake.Embed:
        """Create detailed permission embed"""
        if perm_type == "full":
            title = "🔓 Quyền Đầy Đủ (Administrator)"
            color = COLORS["orange"]
            desc = "Bot sẽ có **tất cả quyền quản trị** trong server"
            perms = "✅ Administrator - Toàn quyền"
        elif perm_type == "recommended":
            title = "✨ Quyền Khuyến Nghị (Recommended)"
            color = COLORS["pink"]
            desc = "**Quyền tối ưu** - Đủ cho tất cả tính năng"
            perms = """✅ Quản lý channels
✅ Quản lý roles
✅ Quản lý tin nhắn
✅ Nhúng nội dung
✅ Kết nối voice
✅ Phát âm thanh
✅ Kiểm duyệt members"""
        else:  # minimal
            title = "🛡️ Quyền Tối Thiểu (Minimal)"
            color = COLORS["green"]
            desc = "**An toàn nhất** - Quyền cơ bản"
            perms = """✅ Gửi tin nhắn
✅ Nhúng nội dung
✅ Kết nối voice
✅ Phát âm thanh"""

        embed = disnake.Embed(
            title=title,
            description=f"```\n{desc}\n```",
            color=color,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="📋 Quyền được cấp",
            value=f"```\n{perms}\n```",
            inline=False
        )

        # Advantages
        if perm_type == "full":
            advantages = "✅ Không cần config thêm\n✅ Tất cả tính năng hoạt động\n⚠️ Cao nhất"
        elif perm_type == "recommended":
            advantages = "✅ An toàn\n✅ Đầy đủ chức năng\n✅ **Được khuyến nghị**"
        else:
            advantages = "✅ An toàn nhất\n⚠️ Cần cấp quyền thêm\n⚠️ Một số tính năng hạn chế"

        embed.add_field(
            name="💡 Ưu điểm",
            value=advantages,
            inline=False
        )

        embed.add_field(
            name="📝 Hướng dẫn",
            value="1. Nhấp vào nút invite bên dưới\n2. Chọn server\n3. Xác nhận quyền\n4. Hoàn tất! 🎉",
            inline=False
        )

        embed.set_footer(text="💖 Chọn nút invite bên dưới để thêm bot")

        return embed

    @disnake.ui.button(label="🔗 Full Permissions", emoji="🔓", style=disnake.ButtonStyle.success, row=1)
    async def full_invite_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Chỉ người dùng lệnh mới có thể sử dụng!", ephemeral=True)
            return
        
        url = disnake.utils.oauth_url(
            self.bot.user.id,
            permissions=self.full_permissions,
            scopes=('bot', 'applications.commands')
        )
        await inter.response.send_message(f"🔓 **Full Permissions Link:**\n{url}", ephemeral=True)

    @disnake.ui.button(label="⭐ Recommended", emoji="✨", style=disnake.ButtonStyle.primary, row=1)
    async def recommended_invite_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Chỉ người dùng lệnh mới có thể sử dụng!", ephemeral=True)
            return
        
        url = disnake.utils.oauth_url(
            self.bot.user.id,
            permissions=self.recommended_permissions,
            scopes=('bot', 'applications.commands')
        )
        await inter.response.send_message(f"⭐ **Recommended Link:**\n{url}", ephemeral=True)

    @disnake.ui.button(label="🔒 Minimal", emoji="🛡️", style=disnake.ButtonStyle.secondary, row=1)
    async def minimal_invite_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Chỉ người dùng lệnh mới có thể sử dụng!", ephemeral=True)
            return
        
        url = disnake.utils.oauth_url(
            self.bot.user.id,
            permissions=self.minimal_permissions,
            scopes=('bot', 'applications.commands')
        )
        await inter.response.send_message(f"🔒 **Minimal Link:**\n{url}", ephemeral=True)

    @disnake.ui.button(label="📊 Stats", emoji="📊", style=disnake.ButtonStyle.secondary, row=2)
    async def stats_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            return
        
        embed = disnake.Embed(
            title="📊 Bot Statistics",
            color=COLORS["blue"],
            timestamp=datetime.now()
        )
        
        embed.add_field(name="🏠 Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="👥 Users", value=f"`{len(self.bot.users)}`", inline=True)
        embed.add_field(name="🏓 Ping", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        
        await inter.response.send_message(embed=embed, ephemeral=True)

    @disnake.ui.button(label="🏠 Back", emoji="🔙", style=disnake.ButtonStyle.primary, row=2)
    async def back_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            return
        embed = self.create_main_embed()
        await inter.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="Close", emoji="❌", style=disnake.ButtonStyle.danger, row=2)
    async def close_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            return
        await inter.response.defer()
        await inter.message.delete()

class Invite(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot: ClientUser = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(name="invite", description="🎀 Mời bot vào server của bạn")
    async def invite(self, interaction: disnake.ApplicationCommandInteraction):
        """Enhanced cute invite command"""
        view = InviteView(self.bot, interaction.author)
        embed = view.create_main_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(name="botinfo", description="ℹ️ Thông tin chi tiết về bot")
    async def botinfo(self, interaction: disnake.ApplicationCommandInteraction):
        """Bot information"""
        embed = disnake.Embed(
            title="🎀 Hatsune Miku Bot",
            description="Bot Discord cute với nhạc, game và tiện ích",
            color=COLORS["pink"],
            timestamp=datetime.now()
        )

        embed.add_field(name="📋 Thông tin cơ bản", value=f"**Tên:** {self.bot.user.name}\n**ID:** `{self.bot.user.id}`", inline=True)
        embed.add_field(name="📊 Thống kê", value=f"**Servers:** `{len(self.bot.guilds)}`\n**Users:** `{len(self.bot.users)}`", inline=True)

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(
            label="🔗 Mời Bot",
            url=disnake.utils.oauth_url(self.bot.user.id, permissions=disnake.Permissions(administrator=True), scopes=('bot', 'applications.commands')),
            style=disnake.ButtonStyle.link
        ))

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="💖 Hatsune Miku Bot")

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.slash_command(name="support", description="🆘 Hỗ trợ và liên hệ")
    async def support(self, interaction: disnake.ApplicationCommandInteraction):
        """Support information"""
        embed = disnake.Embed(
            title="🆘 Hỗ trợ & Liên hệ",
            description="Cần trợ giúp? Chúng tôi luôn sẵn sàng!",
            color=COLORS["red"],
            timestamp=datetime.now()
        )

        embed.add_field(name="💬 Discord", value="[Join Server](https://discord.gg/mFnAZp49ZU)", inline=False)
        embed.add_field(name="👨‍💻 Developer", value="<@1299777672905363569>", inline=False)

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label="💬 Discord", url="https://discord.gg/mFnAZp49ZU", style=disnake.ButtonStyle.link))

        embed.set_footer(text="💖 Chúng tôi luôn lắng nghe!")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="invite", aliases=["inv"])
    async def invite_prefix(self, ctx: commands.Context):
        """Prefix version"""
        if ctx.author.bot:
            return
        view = InviteView(self.bot, ctx.author)
        embed = view.create_main_embed()
        await ctx.send(embed=embed, view=view)

def setup(bot: ClientUser):
    bot.add_cog(Invite(bot))