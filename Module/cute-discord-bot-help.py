"""
🎀 Hatsune Miku Bot - Cute Help System
Giao diện đẹp và dễ thương với Discord Embeds & Components

Author: Hatsune Miku Bot Team
Version: 3.1.0 - Enhanced Cute Edition
"""

import disnake
from disnake.ext import commands
from datetime import datetime
from typing import Optional
import asyncio

# ═══════════════════════════════════════════════════════════════
#                        🎨 CẤU HÌNH MÀU SẮC PASTEL
# ═══════════════════════════════════════════════════════════════

COLORS = {
    "pink": 0xFFB6C1,        # Light Pink
    "purple": 0xDDA0DD,      # Plum  
    "blue": 0x87CEEB,        # Sky Blue
    "teal": 0x40E0D0,        # Turquoise
    "orange": 0xFFB347,      # Pastel Orange
    "violet": 0xEE82EE,      # Violet
    "rose": 0xFF69B4,        # Hot Pink
    "mint": 0x98FF98,        # Mint Green
}

# ═══════════════════════════════════════════════════════════════
#                        ✨ COMMAND CATEGORIES
# ═══════════════════════════════════════════════════════════════

CATEGORIES = {
    "🛡️ Moderation": {
        "description": "Các lệnh quản lý và kiểm duyệt server với tính năng nâng cao",
        "color": COLORS["rose"],
        "emoji": "🛡️",
        "thumbnail": "https://cdn.discordapp.com/emojis/1234567890.png",  # Thay bằng emoji URL
        "commands": {
            "mute": "⏸️ Timeout thành viên với thời gian tùy chỉnh",
            "unmute": "▶️ Bỏ timeout cho thành viên", 
            "kick": "👢 Kick thành viên ra khỏi server",
            "ban": "🔨 Ban thành viên với tùy chọn xóa tin nhắn",
            "unban": "🔓 Unban user khỏi server",
            "clear": "🧹 Xóa tin nhắn với bộ lọc thông minh"
        }
    },
    
    "🎫 Ticket System": {
        "description": "Hệ thống ticket hỗ trợ chuyên nghiệp với giao diện modal đẹp như Discord",
        "color": COLORS["violet"],
        "emoji": "🎫",
        "commands": {
            "ticket setup": "⚙️ Setup hệ thống ticket",
            "ticket panel": "📋 Gửi panel ticket với giao diện đã config",
            "ticket config": "🎨 Config giao diện với modal forms đẹp",
            "ticket close": "🔒 Đóng ticket hiện tại",
            "ticket reopen": "🔓 Mở lại ticket đã đóng",
            "ticket add": "➕ Thêm user vào ticket",
            "ticket remove": "➖ Xóa user khỏi ticket"
        }
    },
    
    "🎵 Music Player": {
        "description": "Hệ thống phát nhạc chuyên nghiệp với player controller đẹp",
        "color": COLORS["blue"],
        "emoji": "🎵",
        "commands": {
            "play": "▶️ Phát nhạc từ YouTube/Spotify",
            "pause": "⏸️ Tạm dừng bài hát",
            "skip": "⏭️ Bỏ qua bài hiện tại",
            "queue": "📋 Danh sách nhạc chờ",
            "volume": "🔊 Điều chỉnh âm lượng",
            "loop": "🔁 Chế độ lặp lại",
            "shuffle": "🔀 Trộn ngẫu nhiên queue",
            "lyrics": "📝 Hiển thị lời bài hát"
        }
    },
    
    "🎣 Fishing Game": {
        "description": "Trò chơi câu cá tương tác với hệ thống kinh tế hoàn chỉnh",
        "color": COLORS["teal"],
        "emoji": "🎣",
        "commands": {
            "fish": "🎣 Câu cá để kiếm tiền (cooldown 30s)",
            "inventory": "🎒 Xem túi đồ và thống kê",
            "fishmarket": "🏪 Cửa hàng - bán cá và nâng cấp",
            "dailyfish": "🎁 Phần thưởng hàng ngày",
            "fishquest": "📜 Nhiệm vụ câu cá",
            "fishhelp": "❓ Hướng dẫn chi tiết game"
        }
    },
    
    "🎉 Giveaway": {
        "description": "Hệ thống giveaway chuyên nghiệp với tự động hóa hoàn toàn",
        "color": COLORS["orange"],
        "emoji": "🎉",
        "commands": {
            "giveaway": "🎁 Tạo giveaway với giao diện đẹp",
            "giveaway-list": "📋 Danh sách giveaway đang diễn ra",
            "giveaway-end": "🏁 Kết thúc giveaway sớm",
            "giveaway-reroll": "🔄 Quay lại người thắng mới",
            "giveaway-info": "ℹ️ Thông tin chi tiết giveaway"
        }
    },
    
    "🚀 Boost Tracker": {
        "description": "Hệ thống theo dõi Server Boost tự động với thông báo đẹp",
        "color": COLORS["pink"],
        "emoji": "🚀",
        "commands": {
            "boost-setup": "⚙️ Setup thông báo boost",
            "boost-disable": "❌ Tắt hệ thống boost",
            "boost-stats": "📊 Thống kê boost với tier",
            "boost-history": "📜 Lịch sử boost server",
            "boost-test": "🧪 Test thông báo boost"
        }
    },
    
    "🎮 Fun & Games": {
        "description": "Các lệnh giải trí và game tương tác vui nhộn",
        "color": COLORS["purple"],
        "emoji": "🎮",
        "commands": {
            "8ball": "🎱 Hỏi quả cầu thần số 8",
            "dice": "🎲 Tung xúc xắc",
            "flip": "🪙 Tung đồng xu",
            "joke": "😂 Chuyện cười lập trình",
            "love": "💖 Tính độ tương hợp",
            "sfw": "🖼️ Ảnh anime an toàn"
        }
    },
    
    "⚙️ System": {
        "description": "Các lệnh hệ thống và thông tin bot",
        "color": COLORS["blue"],
        "emoji": "⚙️",
        "commands": {
            "ping": "🏓 Kiểm tra độ trễ bot",
            "about": "ℹ️ Thông tin chi tiết về bot",
            "status": "📊 Trạng thái chi tiết bot",
            "invite": "🔗 Menu mời bot với quyền",
            "support": "💬 Hỗ trợ và liên hệ",
            "help": "❓ Menu trợ giúp tương tác"
        }
    }
}

# ═══════════════════════════════════════════════════════════════
#                        🎀 ENHANCED DROPDOWN MENU
# ═══════════════════════════════════════════════════════════════

class CuteDropdown(disnake.ui.StringSelect):
    def __init__(self, view_instance):
        self.view_instance = view_instance
        
        options = [
            disnake.SelectOption(
                label="🏠 Main Menu",
                description="Quay về menu chính cute",
                value="main",
                emoji="🏠"
            )
        ]
        
        for cat_name, cat_info in CATEGORIES.items():
            short_name = cat_name.split(" ", 1)[1] if " " in cat_name else cat_name
            options.append(
                disnake.SelectOption(
                    label=short_name,
                    description=cat_info["description"][:50] + "...",
                    value=cat_name,
                    emoji=cat_info["emoji"]
                )
            )
        
        super().__init__(
            placeholder="✨ Chọn danh mục để xem...",
            min_values=1,
            max_values=1,
            options=options,
            row=0
        )
    
    async def callback(self, inter: disnake.MessageInteraction):
        if inter.user.id != self.view_instance.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        
        if self.values[0] == "main":
            embed = self.view_instance.create_main_embed()
        else:
            embed = self.view_instance.create_category_embed(self.values[0])
        
        await inter.response.edit_message(embed=embed, view=self.view_instance)

# ═══════════════════════════════════════════════════════════════
#                        💖 ENHANCED CUTE HELP VIEW
# ═══════════════════════════════════════════════════════════════

class CuteHelpView(disnake.ui.View):
    def __init__(self, bot, user: disnake.User):
        super().__init__(timeout=300)
        self.bot = bot
        self.user = user
        self.current_page = "main"
        
        self.add_item(CuteDropdown(self))
    
    def create_main_embed(self) -> disnake.Embed:
        """Tạo embed main menu siêu cute"""
        embed = disnake.Embed(
            title="🎀 **Hatsune Miku Bot** 🎀",
            description=f"""
╭─────────── • ◆ • ───────────╮
   **Chào mừng đến với bot cute nhất Discord!** 
╰─────────── • ◆ • ───────────╯

💖 **Bot Information:**
✨ Version: `3.1.0 Enhanced`
🌸 Servers: `{len(self.bot.guilds)}` 
🎵 Users: `{len(self.bot.users)}`
⚡ Commands: `{sum(len(cat["commands"]) for cat in CATEGORIES.values())}`
🏓 Ping: `{round(self.bot.latency * 1000)}ms`
💾 Uptime: `Running`

─────────────────────────────

🌟 **Tính năng nổi bật:**

🎫 **Ticket System** - Modal forms đẹp như Discord
🎵 **Music Player** - Controller với 25+ lệnh  
🎣 **Fishing Game** - 8 loại cá, hệ thống kinh tế
🎉 **Giveaway** - Tự động hóa hoàn toàn
🚀 **Boost Tracker** - Theo dõi boost server
🛡️ **Moderation** - Quản lý server nâng cao
🎮 **Fun & Games** - 10+ mini game vui nhộn
⚙️ **System** - Các lệnh hệ thống tiện ích

─────────────────────────────

📋 **Sử dụng dropdown menu bên dưới để xem các danh mục!**
            """,
            color=COLORS["pink"],
            timestamp=datetime.now()
        )
        
        # Thêm category overview
        categories_list = ""
        for cat_name, cat_info in CATEGORIES.items():
            cmd_count = len(cat_info["commands"])
            categories_list += f"{cat_info['emoji']} **{cat_name}** • `{cmd_count} lệnh`\n"
        
        embed.add_field(
            name="📚 Danh mục lệnh",
            value=categories_list,
            inline=False
        )
        
        # Quick links
        embed.add_field(
            name="🔗 Quick Links",
            value="[Discord Server](https://discord.gg/mFnAZp49ZU) • [Website](https://guns.lol/themiy2009) • [Invite Bot](https://discord.com/oauth2/authorize)",
            inline=False
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"💖 Requested by {self.user.display_name} • Made with love",
            icon_url=self.user.display_avatar.url
        )
        
        return embed
    
    def create_category_embed(self, category_name: str) -> disnake.Embed:
        """Tạo embed cho category cụ thể với format tốt hơn"""
        if category_name not in CATEGORIES:
            return self.create_main_embed()
        
        cat_info = CATEGORIES[category_name]
        
        embed = disnake.Embed(
            title=f"{cat_info['emoji']} **{category_name}**",
            description=f"✨ {cat_info['description']}\n\n",
            color=cat_info["color"],
            timestamp=datetime.now()
        )
        
        # Format commands tốt hơn
        commands_text = ""
        for idx, (cmd_name, cmd_desc) in enumerate(cat_info["commands"].items(), 1):
            commands_text += f"{idx}. **`/{cmd_name}`** - {cmd_desc}\n"
        
        embed.add_field(
            name=f"📋 Available Commands ({len(cat_info['commands'])})",
            value=commands_text,
            inline=False
        )
        
        # Stats
        embed.add_field(
            name="📊 Statistics",
            value=f"Commands: `{len(cat_info['commands'])}`\nCategory Color: `{hex(cat_info['color'])}`",
            inline=True
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"💖 Page: {category_name} • Use dropdown to navigate",
            icon_url=self.user.display_avatar.url
        )
        
        return embed
    
    # Buttons với emoji cute
    @disnake.ui.button(label="Home", emoji="🏠", style=disnake.ButtonStyle.primary, row=1)
    async def home_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        embed = self.create_main_embed()
        await inter.response.edit_message(embed=embed, view=self)
    
    @disnake.ui.button(label="Music", emoji="🎵", style=disnake.ButtonStyle.secondary, row=1)
    async def music_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        embed = self.create_category_embed("🎵 Music Player")
        await inter.response.edit_message(embed=embed, view=self)
    
    @disnake.ui.button(label="Ticket", emoji="🎫", style=disnake.ButtonStyle.secondary, row=1)
    async def ticket_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        embed = self.create_category_embed("🎫 Ticket System")
        await inter.response.edit_message(embed=embed, view=self)
    
    @disnake.ui.button(label="Fishing", emoji="🎣", style=disnake.ButtonStyle.secondary, row=1)
    async def fishing_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        embed = self.create_category_embed("🎣 Fishing Game")
        await inter.response.edit_message(embed=embed, view=self)
    
    @disnake.ui.button(label="Stats", emoji="📊", style=disnake.ButtonStyle.success, row=2)
    async def stats_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        
        stats_embed = disnake.Embed(
            title="📊 Bot Statistics",
            description="Thống kê chi tiết về bot",
            color=COLORS["blue"],
            timestamp=datetime.now()
        )
        
        stats_embed.add_field(
            name="🌸 Server Stats",
            value=f"```\nServers: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}\nLatency: {round(self.bot.latency * 1000)}ms\n```",
            inline=True
        )
        
        total_cmds = sum(len(cat["commands"]) for cat in CATEGORIES.values())
        stats_embed.add_field(
            name="⚡ Command Stats",
            value=f"```\nTotal: {total_cmds}\nCategories: {len(CATEGORIES)}\n```",
            inline=True
        )
        
        await inter.response.send_message(embed=stats_embed, ephemeral=True)
    
    @disnake.ui.button(label="Support", emoji="💬", style=disnake.ButtonStyle.link, url="https://discord.gg/mFnAZp49ZU", row=2)
    async def support_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass  # Link button không cần callback
    
    @disnake.ui.button(label="⬅️ Back", emoji="⬅️", style=disnake.ButtonStyle.danger, row=2)
    async def back_btn(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.user.id != self.user.id:
            await inter.response.send_message("❌ Bạn không thể sử dụng menu này!", ephemeral=True)
            return
        embed = self.create_main_embed()
        await inter.response.edit_message(embed=embed, view=self)

# ═══════════════════════════════════════════════════════════════
#                        🎀 HELP COG
# ═══════════════════════════════════════════════════════════════

class CuteHelp(commands.Cog):
    """Cute Help System Cog"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="help", aliases=["h", "?"])
    async def help_cmd(self, ctx, category: Optional[str] = None):
        """Lệnh help với prefix"""
        view = CuteHelpView(self.bot, ctx.author)
        
        if category:
            cat_map = {
                "moderation": "🛡️ Moderation",
                "ticket": "🎫 Ticket System",
                "music": "🎵 Music Player",
                "fishing": "🎣 Fishing Game",
                "giveaway": "🎉 Giveaway",
                "boost": "🚀 Boost Tracker",
                "fun": "🎮 Fun & Games",
                "system": "⚙️ System"
            }
            embed = view.create_category_embed(cat_map.get(category, "🛡️ Moderation"))
        else:
            embed = view.create_main_embed()
        
        await ctx.send(embed=embed, view=view)
    
    @commands.slash_command(name="cuthelp", description="🎀 Menu trợ giúp cute")
    async def cuthelp_cmd(self, inter: disnake.ApplicationCommandInteraction, category: Optional[str] = None):
        """Lệnh cuthelp chính"""
        view = CuteHelpView(self.bot, inter.author)
        
        if category:
            cat_map = {
                "moderation": "🛡️ Moderation",
                "ticket": "🎫 Ticket System",
                "music": "🎵 Music Player",
                "fishing": "🎣 Fishing Game",
                "giveaway": "🎉 Giveaway",
                "boost": "🚀 Boost Tracker",
                "fun": "🎮 Fun & Games",
                "system": "⚙️ System"
            }
            embed = view.create_category_embed(cat_map.get(category, "🛡️ Moderation"))
        else:
            embed = view.create_main_embed()
        
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @commands.slash_command(name="commands", description="📋 Danh sách tất cả lệnh")
    async def commands_list(self, inter: disnake.ApplicationCommandInteraction):
        """Hiển thị tất cả lệnh"""
        embed = disnake.Embed(
            title="📋 Danh sách tất cả lệnh",
            description="Tất cả lệnh có sẵn của bot",
            color=COLORS["purple"],
            timestamp=datetime.now()
        )
        
        for cat_name, cat_info in CATEGORIES.items():
            cmd_list = "\n".join([f"• `/{cmd}` - {desc}" for cmd, desc in cat_info["commands"].items()])
            embed.add_field(
                name=f"{cat_name}",
                value=cmd_list,
                inline=False
            )
        
        total = sum(len(cat["commands"]) for cat in CATEGORIES.values())
        embed.set_footer(text=f"💖 Total: {total} commands • Use /cuthelp for more info")
        
        await inter.response.send_message(embed=embed, ephemeral=True)

# ═══════════════════════════════════════════════════════════════
#                        🎀 SETUP FUNCTION
# ═══════════════════════════════════════════════════════════════

def setup(bot):
    """Load cog vào bot"""
    bot.add_cog(CuteHelp(bot))
    print("✨ Cute Help System loaded successfully!")
