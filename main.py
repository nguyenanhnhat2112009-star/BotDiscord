import sys
import os

# Add project root to path để import modules đúng
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.ClientUser import load
import utils.logger

utils.logger.setup_loger()
bot = load()
bot.load_extension("cogs.welcome_module")
bot.load_extension("Module.link_saver")
bot.load_extension("Module.link_community")
bot.load_extension("Module.link_info")
bot.load_extension("Module.sysinfo")
bot.load_extension("Module.help")
bot.load_extension("Module.anime_notifier")
bot.load_extension("Module.link_replay")  
bot.run("TOKEN")