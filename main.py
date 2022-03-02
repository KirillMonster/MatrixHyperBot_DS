import os
import time

import discord
from config import AUTHOR_ID
from db import create_users, create_auc, create_pay, create_crypto, create_clans
from discord.ext import commands
from tokens import TOKEN

create_users()
create_auc()
create_pay()
create_crypto()
create_clans()
timer1 = time.time()
intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    time_launched = time.time() - timer1
    print(f'Запущен за {time_launched}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help | !menu'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'** {ctx.author.name}**, данной команды не существует.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'** {ctx.author.name}**, для этой команды нужны права администратора.')


@client.command()
async def load(ctx, extension=None):
    if ctx.author.id == AUTHOR_ID:
        if extension is not None:
            await ctx.send('Cogs is loaded...')
            client.load_extension(f'cogs.{extension}')
            await ctx.send('Successfully!')
        else:
            await ctx.send('You have not entered extension')
    else:
        await ctx.send('Вы не разработчик!')


@client.command()
async def unload(ctx, extension=None):
    if ctx.author.id == AUTHOR_ID:
        if extension is not None:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send('Cogs is unloaded...')
        else:
            await ctx.send('You have not entered extension')
    else:
        await ctx.send('Вы не разработчик!')


@client.command()
async def reload(ctx, extension=None):
    if ctx.author.id == AUTHOR_ID:
        if extension is None:
            cogs_reload()
            await ctx.send('Successfully!')
        else:
            await ctx.send('Cogs is reloaded...')
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send('Successfully!')
    else:
        await ctx.send('Вы не разработчик!')


@client.command()
async def reloadall(ctx):
    if ctx.author.id == AUTHOR_ID:
        cogs_reload()
        await ctx.send('Successfully!')
    else:
        await ctx.send('Вы не разработчик!')


def cogs_reload():
    global extensions
    extensions = ''
    file_names = []
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            if file_name != 'config.py':
                extensions += ' ' + file_name[:-3] + '\n'
                file_names.append(file_name[:-3])
                client.unload_extension(f'cogs.{file_name[:-3]}')
                client.load_extension(f'cogs.{file_name[:-3]}')


@client.command()
async def ext(ctx):
    if ctx.author.id == AUTHOR_ID:
        await ctx.send(f'Extensions:\n{extensions}')
    else:
        await ctx.send('Вы не разработчик!')


extensions = ''
file_names = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename != 'config.py' and filename != 'db.py':
            extensions += ' ' + filename[:-3] + '\n'
            filenames.append(filename[:-3])
            client.load_extension(f'cogs.{filename[:-3]}')

# RUN
if __name__ == '__main__':
    client.run(TOKEN)
