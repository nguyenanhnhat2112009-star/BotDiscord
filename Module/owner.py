import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext.commands import Cog, slash_command, is_owner
from utils.ClientUser import ClientUser
from datetime import datetime

COLORS = {
    "blue": 0x87CEEB,
    "green": 0x98FF98,
    "red": 0xFF6B6B,
    "yellow": 0xFFEB3B,
    "purple": 0xDDA0DD
}

class OwnerButtons(disnake.ui.View):
    def __init__(self, action: str):
        super().__init__(timeout=30)
        self.action = action
        self.confirmed = None
    
    @disnake.ui.button(label="✅ Xác nhận", style=disnake.ButtonStyle.green)
    async def confirm(self, button: disnake.ui.Button, interaction: ApplicationCommandInteraction):
        self.confirmed = True
        self.stop()
        await interaction.response.defer()
    
    @disnake.ui.button(label="❌ Hủy", style=disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.ui.Button, interaction: ApplicationCommandInteraction):
        self.confirmed = False
        self.stop()
        await interaction.response.defer()

class Owner(Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot
        
    @is_owner()
    @slash_command(name="reload", description="🔄 Tải lại tất cả các module")
    async def reload_module(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            embed = disnake.Embed(
                title="🔄 Đang tải lại module...",
                description="```⏳ Vui lòng đợi...```",
                color=COLORS["yellow"],
                timestamp=datetime.now()
            )
            await inter.edit_original_response(embed=embed)
            
            load = self.bot.load_modules()
            
            if not load:
                embed = disnake.Embed(
                    title="✅ Reload Thành Công!",
                    description="```💚 Tất cả module đã được tải lại!```",
                    color=COLORS["green"],
                    timestamp=datetime.now()
                )
                embed.add_field(name="📊 Trạng thái", value="🟢 Tất cả module hoạt động bình thường", inline=False)
                embed.set_footer(text=f"👑 Owner: {inter.author.display_name}")
            else:
                embed = disnake.Embed(
                    title="⚠️ Reload Có Lỗi!",
                    description=f"```❌ {load}```",
                    color=COLORS["red"],
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"👑 Owner: {inter.author.display_name}")
            
            await inter.edit_original_response(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Lỗi!",
                description=f"```{str(e)[:100]}```",
                color=COLORS["red"]
            )
            await inter.edit_original_response(embed=embed)

    @is_owner()
    @slash_command(name="shutdown", description="🛑 Tắt bot")
    async def shutdown(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()
        
        if self.bot.is_closed():
            embed = disnake.Embed(
                title="⚠️ Thông báo",
                description="```Bot đã tắt rồi!```",
                color=COLORS["yellow"]
            )
            await inter.edit_original_response(embed=embed)
            return
        
        embed = disnake.Embed(
            title="🛑 Bạn chắc chắn muốn tắt bot?",
            description="```⚠️ Bot sẽ offline sau 5 giây!```",
            color=COLORS["red"],
            timestamp=datetime.now()
        )
        embed.add_field(name="⏱️ Thời gian", value="Chờ 30 giây để hủy", inline=False)
        embed.set_footer(text=f"👑 Owner: {inter.author.display_name}")
        
        view = OwnerButtons("shutdown")
        await inter.edit_original_response(embed=embed, view=view)
        
        await view.wait()
        
        if view.confirmed:
            embed = disnake.Embed(
                title="👋 Tạm biệt!",
                description="```🛑 Bot đang tắt...```",
                color=COLORS["red"],
                timestamp=datetime.now()
            )
            embed.add_field(name="⏰ Thời gian", value="Bây giờ", inline=False)
            await inter.edit_original_response(embed=embed, view=None)
            await self.bot.close()
        else:
            embed = disnake.Embed(
                title="✅ Đã hủy!",
                description="```💚 Bot vẫn online!```",
                color=COLORS["green"],
                timestamp=datetime.now()
            )
            await inter.edit_original_response(embed=embed, view=None)

    @is_owner()
    @slash_command(name="status", description="📊 Xem trạng thái bot")
    async def status(self, inter: ApplicationCommandInteraction):
        await inter.response.defer()
        try:
            embed = disnake.Embed(
                title="📊 Bot Status",
                description="```🤖 Thông tin trạng thái hiện tại```",
                color=COLORS["blue"],
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="🟢 Trạng thái",
                value=f"```{'ONLINE' if not self.bot.is_closed() else 'OFFLINE'}```",
                inline=True
            )
            
            embed.add_field(
                name="⏱️ Uptime",
                value=f"```{str(datetime.now() - self.bot.start_time).split('.')[0]}```",
                inline=True
            )
            
            embed.add_field(
                name="📅 Thời gian khởi động",
                value=f"```{self.bot.start_time.strftime('%Y-%m-%d %H:%M:%S')}```",
                inline=True
            )
            
            embed.set_footer(text=f"👑 Owner: {inter.author.display_name}")
            
            await inter.edit_original_response(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="❌ Lỗi!",
                description=f"```{str(e)[:100]}```",
                color=COLORS["red"]
            )
            await inter.edit_original_response(embed=embed)

def setup(bot: ClientUser):
    bot.add_cog(Owner(bot))