import discord
from discord.ext import commands
from psutil import cpu_percent, virtual_memory
from psutil._common import bytes2human
from PIL import Image, ImageFont, ImageDraw
import requests
import io
import asyncio
from Cybernator import Paginator
from db import item_user, adv_num, all_count_users, check_user, embed_color, emoji_cash, emoji_lvl, emoji_rep, count_items

class Main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bot(self, ctx):
        await ctx.send(f'🤖Бот:\n📋Версия бота 1.2\n📅Дата обновления версии: 10.12.2021\n👥Игроков: {all_count_users()}\n📊Нагрузка системы:\n🖥CPU: {cpu_percent()}%\nRAM: {bytes2human(virtual_memory()[3])}/{bytes2human(virtual_memory()[0])}({virtual_memory()[2]}%)')
    
    @commands.command()
    async def prof(self, ctx, member: discord.Member = None):
        if member is None:
            cash = adv_num(item_user('cash', ctx.author.id))
            bank = adv_num(item_user('bank', ctx.author.id))
            rep = adv_num(item_user('rep', ctx.author.id))
            lvl = adv_num(item_user('lvl', ctx.author.id))
            await ctx.send(f'Ваш профиль:\nID: **{ctx.author.id}**\nCash: **{cash}**{emoji_cash}\nBank: **{bank}**{emoji_cash}\nRep: **{rep}**{emoji_rep}\nLVL: **{lvl}**{emoji_lvl}')
        else:
            if member == ctx.author:
                await ctx.send(f'**{ctx.author}**, вы не можете указать самого себя.')
            else:
                if check_user(member.id):
                    await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных.')
                else:
                    await ctx.send(f'Профиль игрока:\nID: **{member.id}**\nCash: **{adv_num(item_user("cash", member.id))}**{emoji_cash}\nRep: **{adv_num(item_user("rep", member.id))}**{emoji_rep}\nLVL: **{adv_num(item_user("lvl", member.id))}**{emoji_lvl}')

    @commands.command()
    async def project(self, ctx):
        await ctx.send('Информация о проекте:\nСоздатель проекта: ※Why not?※\nБот Matrix HyperBot был написаным - **<@643017727728025602>**')
        
    @commands.command()
    async def card(self, ctx):
        img = Image.open('mountain1.jpg').resize((400, 200), Image.ANTIALIAS)
        url = str(ctx.author.avatar_url)
        response = requests.get(url, stream = True)
        response = Image.open(io.BytesIO(response.content))
        response = response.convert('RGBA')
        response = response.resize((100, 100), Image.ANTIALIAS)
        img.paste(response, (15, 15, 115, 115))
        idraw = ImageDraw.Draw(img)
        headline = ImageFont.truetype('arial.ttf', size = 20)
        undertext = ImageFont.truetype('arial.ttf', size = 16)
        items = count_items(ctx.author.id)
        idraw.text((200, 10), f'{ctx.author}', font = headline)
        idraw.text((200, 35), f'ID: {ctx.author.id}', font = undertext)
        idraw.text((200, 60), f"Cash: {adv_num(item_user('cash', ctx.author.id))}", font = undertext)
        idraw.text((200, 85), f"Rep: {adv_num(item_user('rep', ctx.author.id))}", font = undertext)
        idraw.text((200, 110), f"LVL: {adv_num(item_user('lvl', ctx.author.id))}", font = undertext)
        idraw.text((200, 135), f"Items: {items}", font = undertext)
        img.save('user_card.png')
        await ctx.send(file = discord.File(fp = 'user_card.png'))
    
    @commands.command(aliases=['help', 'menu'])
    async def __menu(self, ctx):
        emb = discord.Embed(title='Навигация', description='⏩ - следущая страница.\n⏪ - продедущая страница.\n❌ - закрыть.',color = embed_color)
        emb_main = discord.Embed(title='Основые команды', description='**!eco** - `команды экономики.`\n**!bank** - `команды банка.`\n**!shop** - `команды магазина.`\n**!music** - `команды диджея.`\n**!games** - `команды игр.`\n**!auc** - `аукцион.`\n**!buns** - `команды плюшек.`', color = embed_color)
        emb_eco = discord.Embed(title='Экономика:leaves: **!eco**', description='**!prof** - `узнать информацию о своем\игрока профиле.`\n**!card** `получить карочку своего профиля.`\n**!mining** - `майнинг на видеокартах.`\n**!upgrade [кол-во/пусто]** - `прокачка уровня.`\n**!cash [игрок/пусто]** - `узнать баланс игрока/себя.`\n**!lvl [игрок/пусто]** - `узнать уровень игрока/себя.`\n**!rep [игрок/пусто]** - `узнать репутацию игрока/себя.`\n**!rep+ [игрок] - `выдать 1 репутацию игроку.`**\n**!items** - `ваши предметы.`\n\n\n\nСтраница 1/7.', color = embed_color)
        emb_bank = discord.Embed(title='Банк:bank: **!bank**', description='**!bank [игрок/пусто]** - `узнать баланс игрока/себя.`\n**!bankpay [игрок] [сумма]** - `передать деньги с своего счета банка ко счету банка игрока.`\n**!deposit** - `положить деньги на депозитный счёт банка.`\n**!withdraw** - `снять деньги со счёта банка.`\n\n\n\nСтраница 2/7.', color = embed_color)
        emb_shop = discord.Embed(title='Магазин:shopping_cart: **!shop**', description='**!shop** - `магазин предметов.`\n**!buy [предмет] [кол-во]** - `покупка предметов.`\n**!sell [предмет] [кол-во]** - `продажа предметов.`\n\n\n\nСтраница 3/7.', color=embed_color)
        emb_music = discord.Embed(title='Музыка:notes: **!music**', description='**!play [url]** - `воспроизведение музыки.`\n**!repeat** - `воспроизведение предыдущей музыки.`\n**!join** - `подключить бота к голосовому чату.`\n**!pause** - `пауза.`\n**!resume** - `продолжить.`\n**!skip** - `Пропустить музыку.`\n**!disconnect** - `отключить бота от гос чата.`\n\n\nСтраница 4/7.', color=embed_color)
        emb_games = discord.Embed(title='Игры:video_game: !games', description='**!youtube** - `совместный просмотр ютуба.`\n**!pocker** - `сыграй покер с друзьями/ботами.`\n**!casino [ставка]** - `ставь ставку и попытай удачу.`\n\n\n\nСтраница 5/7.', color=embed_color)
        emb_auc = discord.Embed(title='Аукцион:synagogue: **!auc**', description='**!auc** - `аукцион.`\n**!auc_buy [товар]** `купить товар на аукционе.`\n**!auc_sell [товар] [цена]** - `выставить товар на аукцион.`\n\n\n\nСтраница 6/7.', color = embed_color)
        emb_buns = discord.Embed(title='Плюшки:game_die: **!buns**', description='**!project** - `узнать информацию о проекте.`\n**!bot** - `узнать статистику бота.`\n**!freegames** - `все бесплатные игры в Epic Games.`\n**!kiss [игрок]** - `поцеловать игрока.`\n**!hug [игрок]]** - `обнять игрока.`\n\n\n\nСтраница 7/7.', color = embed_color)
        embeds = [emb, emb_main, emb_eco, emb_bank, emb_shop, emb_music, emb_games, emb_auc, emb_buns]
        msg = await ctx.send(embed=emb)
        reactions = ['⏪','⏩']
        page = Paginator(self.client,message=msg,only=ctx.author,timeout=90,reactions=reactions,use_exit=True,exit_reaction=['❌'],delete_message=True,footer=False, embeds=embeds)
        await page.start()
    
def setup(client):
    client.add_cog(Main(client))
