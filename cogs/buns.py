import discord
from discord.ext import commands
from db import embed_color

class Buns(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def buns(self, ctx):
        await ctx.send(embed=discord.Embed(title='Плюшки:game_die: **!buns**', description='**!project** - `узнать информацию о проекте.`\n**!bot** - `узнать статистику бота.`\n**!freegames** - `все бесплатные игры в Epic Games.`\n**!kiss [игрок]** - `поцеловать игрока.`\n**!hug [игрок]]** - `обнять игрока.`', color = embed_color))
    
    @commands.command()
    async def kiss(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, вы не указали игрока.')
        else:
            await ctx.send(f'**{ctx.author}**, вы поцеловали игрока **{member}**.')
    
    @commands.command()
    async def hug(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, вы не указали игрока.')
        else:
            await ctx.send(f'**{ctx.author}**, вы обняли игрока **{member}**.')

def setup(client):
    client.add_cog(Buns(client))
