import discord
from discord.ext import commands
from db import embed_color

class RP(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def roles(self, ctx):
        await ctx.send(embed=discord.Embed(title='Роли', description='Гражданин', color=embed_color))
    
    @commands.command()
    async def role(self, ctx):
        pass

def setup(client):
    client.add_cog(RP(client))
