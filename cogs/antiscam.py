import discord
from discord.ext import commands
from db import log

words = ['nitro', 'бесплатный нитро', 'free nitro', 'freenitro', 'бесплатныйнитро', 'нитро']

class AntiScam(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) in ['VoiceMaster#9351', 'MartixHyper BOT#7848']:
            pass
        else:
            if message.content.lower() in words:
                await message.channel.send(f'Сработала AntiScam система.\nПользователь: **{message.author}**\nСообщение будет удалено.\n\n<@643017727728025602>')
                await message.delete()
                await self.client.get_channel(917002261320859658).send(log('Music', 'AntiScam', message.author))
            
def setup(client):
    client.add_cog(AntiScam(client))
