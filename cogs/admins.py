import discord
from discord.colour import Color
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, component
from discord import utils
from db import embed_color
import os
import asyncio
from random import choice

class Admins(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client)
    # send msg
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def send(self, ctx, member: discord.Member, *args):
        emb = discord.Embed(title=f'Сообщение от админа сервера {ctx.author}', description=f'Вас зовут с причной:\n**{" ".join(args[:])}**', colour = discord.Color.blue())
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await member.send(embed=emb)
    
    @commands.command()
    async def admins(self, ctx):
        role = utils.get(ctx.guild.roles, id = 892080737828876349)
        emb = discord.Embed(title='Админов в сети', color=embed_color)
        players, online, number = [], False, 0
        for member in role.members:
            number += 1
            if str(member.status) == 'online':
                online = True
                players.append(member.name)
                emb.add_field(name=member.name, value=f'Статус: :green_circle:**{str(member.status).replace("online","Online")}**', inline=False)
        if online:
            await ctx.send(embed=emb)
        else:
            await ctx.send(embed=discord.Embed(title='Админов нет в сети'))
    # admin
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def admin(self, ctx):
        await ctx.send(embed=discord.Embed(title='ADMIN'), components=[Button(style=ButtonStyle.green, label='Позвать админа', emoji='😁')])
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color=embed_color))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def cls(self, ctx):
        os.system('cls')
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def mute(self, ctx, member: discord.Member = None, amount_time = None, reason = None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, вы не указали игрока которого желаете замьютить.')
        else:
            if amount_time is None:
                await ctx.send(f'**{ctx.author}**, вы не указали время на которое желаете замьютить игрока.')
            else:
                if reason is None:
                    await ctx.send(f'**{ctx.author}**, вы не указали причину мута.')
                else:
                    await ctx.send(embed = discord.Embed(
                        description = f'''[:mute:] Игрок **{member}** был замучен на **{amount_time}**.
                        **Выдал мут:** **{ctx.author}**
                        ```css
        Причина: [{reason}]
                        ```
                        ''',
                        color = 0x36393E,
                    ))
                    mute_role = discord.utils.get(ctx.guild.roles, id = 921401974476378213)
                    await member.add_roles(mute_role)
                    await asyncio.sleep(int(amount_time[:-1]) * 60)
                    await member.remove_roles(mute_role)

                    await ctx.send(embed = discord.Embed(
                        description = f'''**[:loud_sound:]** Время мута истекло, вы были размучены''',
                        color = 0x2F3136
                    ))  
def setup(client):
    client.add_cog(Admins(client))