import discord
from discord.ext import commands
import json
import requests
import random
from db import item_user, take_user, give_user, embed_color, emoji_cash
from tokens import TOKEN

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def games(self, ctx):
        await ctx.send(embed = discord.Embed(title='Игры:video_game: !games', description = '**!youtube** - `совместный просмотр ютуба.`\n**!pocker** - `сыграй покер с друзьями/ботами.`\n**!casino [ставка]** - `ставь ставку и попытай удачу.`', color=embed_color))
    
    @commands.command()
    async def youtube(self, ctx):
        """target_application_id
    
            Youtube Together - 755600276941176913
            Betrayal.io - 773336526917861400
            Fishington.io - 814288819477020702
            Poker Night - 755827207812677713
            Chess - 832012774040141894
    
        """
    
        data = {
            "max_age": 86400,
            "max_uses": 0,
            "target_application_id": 755600276941176913, # YouTube Together
            "target_type": 2,
            "temporary": False,
            "validate": None
        }
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        }
    
        if ctx.author.voice is not None:
            if ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel.id
            else:
                await ctx.send("Зайдите в канал")
        else:
            await ctx.send("Зайдите в канал")
    
        response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
        link = json.loads(response.content)
    
        await ctx.send(f"https://discord.com/invite/{link['code']}")
    
    @commands.command()
    async def pocker(self, ctx):
        data = {
            "max_age": 86400,
            "max_uses": 0,
            "target_application_id": 755827207812677713,
            "target_type": 2,
            "temporary": False,
            "validate": None
        }
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        }
    
        if ctx.author.voice is not None:
            if ctx.author.voice.channel is not None:
                channel = ctx.author.voice.channel.id
                response = requests.post(f"https://discord.com/api/v8/channels/{channel}/invites", data=json.dumps(data), headers=headers)
                link = json.loads(response.content)
                await ctx.send(f"Нажми на ссылку.\nhttps://discord.com/invite/{link['code']}")
            else:
                await ctx.send("Зайдите в голосовой канал.")
        else:
            await ctx.send("Зайдите в голосовой канал.")
    
    @commands.command()
    async def casino(self, ctx, amount: int=None):
        if amount is None:
            await ctx.send(f'**{ctx.author}**, укажите ставку.')
        else:
            if amount < 1:
                await ctx.send(f'**{ctx.author}**, укажите ставку больше 0 {emoji_cash}')
            else: 
                if item_user('cash', ctx.author.id) >= amount:
                    take_user('cash', amount, ctx.author.id)
                    if random.randint(1, 100) >= 50:
                        kof = random.randint(100, 500)/100
                        win = int(amount*kof)
                        give_user('cash', win, ctx.author.id)
                        await ctx.send(f'🔥**{ctx.author}**🔥,\n🤑**Выигрышь!**🤑\n💸Вы выиграли: **+{win}:leaves:**\n💶Ставка: **{amount} :leaves:**\n📊Коэффициент: **x{kof}**\n💰Ваш баланс: **{item_user("cash", ctx.author.id)}** :leaves:')
                    else:
                        await ctx.send(f'🔥**{ctx.author}**🔥,\n😵Проигрыш **-{amount}** :leaves: 😵\n💰Ваш баланс: **{item_user("cash", ctx.author.id)}** :leaves:')
                else:
                    await ctx.send(f'**{ctx.author}**, недостаточно средств.')        

def setup(client):
    client.add_cog(Games(client))
