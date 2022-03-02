import discord
from discord.ext import commands
from discord.utils import get
from db import check_user, new_user, item_user, give_user, not_money, take_user, adv_num, emoji_cash, emoji_lvl, emoji_rep, top_user, embed_color, not_money
from random import randint

class Eco(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()    
    async def on_ready(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if not str(member) in ['VoiceMaster#9351', 'MartixHyper BOT#7848']:
                    if check_user(member.id):
                        new_user(member)
                    await member.add_roles(get(member.guild.roles, id=921818688271839282)) # player
                    #await member.add_roles(get(member.guild.roles, id=921817617197588480)) # привилегия
                    #await member.add_roles(get(member.guild.roles, id=921818051354198036)) # игры
                    #await member.add_roles(get(member.guild.roles, id=921818218539147265)) # гендер
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if check_user(member.id):
            new_user(member)
        await member.add_roles(get(member.guild.roles, id=921818688271839282)) # player
        #await member.add_roles(get(member.guild.roles, id=921817617197588480)) # привилегия
        #await member.add_roles(get(member.guild.roles, id=921818051354198036)) # игры
        #await member.add_roles(get(member.guild.roles, id=921818218539147265)) # гендер
        
    @commands.command()
    async def eco(self, ctx):
        await ctx.send(embed = discord.Embed(title='Экономика:leaves: **!eco**', description ='**!prof** - `узнать информацию о своем\игрока профиле.`\n**!card** `получить карочку своего профиля.`\n**!mining** - `майнинг на видеокартах.`\n**!upgrade [кол-во/пусто]** - `прокачка уровня.`\n**!cash [игрок/пусто]** - `узнать баланс игрока/себя.`\n**!lvl [игрок/пусто]** - `узнать уровень игрока/себя.`\n**!rep [игрок/пусто]** - `узнать репутацию игрока/себя.`\n**!rep+ [игрок] - `выдать 1 репутацию игроку.`**\n**!items** - `ваши предметы.`', color = embed_color))
    
    @commands.command()
    async def mining(self, ctx):
        mined = 0
        rtx3060 = item_user('rtx3060', ctx.author.id);rtx3070 = item_user('rtx3070', ctx.author.id);rtx3080 = item_user('rtx3080', ctx.author.id);rtx3090 = item_user('rtx3090', ctx.author.id)
        if rtx3060 > 0 or rtx3070 > 0 or rtx3080 > 0 or rtx3090 > 0:
            if rtx3060 > 0:
                for i in range(rtx3060):
                    kof = randint(100, 250)/100
                    mined += int(randint(100, 1000)*kof)
            if rtx3070 > 0:
                for i in range(rtx3070):
                    kof = randint(100, 500)/100
                    mined += int(randint(100, 1000)*kof)
            if rtx3080 > 0:
                for i in range(rtx3080):
                    kof = randint(100, 750)/100
                    mined += int(randint(100, 1000)*kof)
            if rtx3090 > 0:
                for i in range(rtx3090):
                    kof = randint(100, 1000)/100
                    mined += int(randint(100, 1000)*kof)
            give_user('cash', mined, ctx.author.id)
            await ctx.send(f'**{ctx.author}**, вы намайнили целых **{adv_num(mined)}** {emoji_cash}')
        else:
            await ctx.send(f'**{ctx.author}**, у вас нету видеокарты')
    
    @commands.command()
    async def upgrade(self, ctx, count=None):
        lvl = item_user('lvl', ctx.author.id)
        cash = item_user('cash', ctx.author.id)
        price = 10000
        if count is None:
            count = '1'
        if count.isdigit():
            count = int(count)
            for i in range(lvl+count):
                price += 10000
            if cash >= price:
                take_user('cash', price, ctx.author.id)
                give_user('lvl', 1, ctx.author.id)
                await ctx.send(f'**{ctx.author}**, вы успешно улучшили свой уровень до **{adv_num(lvl+1)}**, потратив - **{adv_num(price)}**{emoji_cash}')
            else:
                await ctx.send(not_money(ctx, price, cash))
        else:
            await ctx.send(f'**{ctx.author}**, введите число.')
        
    @commands.command()        
    async def cash(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'Баланс пользователя **{ctx.author}** составляет **{adv_num(item_user("cash", ctx.author.id))}** {emoji_cash}')
        else:
            if check_user(member.id):
                await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных')
            else:
                await ctx.send(f'Баланс пользователя **{member}** составляет **{adv_num(item_user("cash", ctx.author.id))}** {emoji_cash}')
                
    @commands.command()        
    async def lvl(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'Уровень пользователя **{ctx.author}** составляет **{adv_num(item_user("lvl", ctx.author.id))} {emoji_lvl}**')
        else:
            if check_user(member.id):
                await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных')
            else:
                await ctx.send(f'Уровень пользователя **{member}** составляет **{adv_num(item_user("lvl", ctx.author.id))} {emoji_lvl}**')
    
    @commands.command()        
    async def rep(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'Репутация пользователя **{ctx.author}** составляет **{adv_num(item_user("rep", ctx.author.id))} {emoji_rep}**')
        else:
            if check_user(member.id):
                await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных')
            else:
                await ctx.send(f'Репутация пользователя **{member}** составляет **{adv_num(item_user("rep", ctx.author.id))} {emoji_rep}**')
    
    @commands.command(aliases=['rep+'])
    @commands.cooldown(1,60,commands.BucketType.user)
    async def __rep(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, укажите пользователя которому желаете выдать репутацию')
        else:
            if member.id == ctx.author.id:
                await ctx.send(f'**{ctx.author}**, вы не можете указать самого себя')
            else:
                if check_user(member.id):
                    await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных')
                else:
                    give_user('rep', 1, member.id)
                    await ctx.send(f'**{ctx.author}**, вы успешно выдали репутацию пользователю {member}')
    
    @__rep.error
    async def __rep_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Повторно выдать можно только через {int(error.retry_after)} секунд(ы)')
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def give(self, ctx, member: discord.Member = None, item=None, amount:int=None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, укажите пользователя которому желаете выдать предмет')
        else:
            if item is None:
                await ctx.send(f'**{ctx.author}**, укажите товар который желаете выдать игроку')
            else:
                if amount is None:
                    await ctx.send(f'**{ctx.author}**, укажите количество товара которое желаете выдать игроку')
                else:
                    if check_user(member.id):
                        await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных.')
                    else:
                        give_user(item, amount, member.id)
                        await ctx.send(f'**{ctx.author}**, вы успешно выдали **{item}** пользователю **{member}** в размере **{adv_num(amount)}**')

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def take(self, ctx, member: discord.Member = None, item=None, amount:int=None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, укажите пользователя у которого желаете забрать предмет')
        else:
            if item is None:
                await ctx.send(f'**{ctx.author}**, укажите товар который желаете забрать у игрока')
            else:
                if amount is None:
                    await ctx.send(f'**{ctx.author}**, укажите количество товара которое желаете забрать у игрока')
                else:
                    if check_user(member.id):
                        await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных.')
                    else:
                        give_user(item, amount, member.id)
                        await ctx.send(f'**{ctx.author}**, вы успешно забрали {item} пользователю {member} в размере {adv_num(amount)}')

    @commands.command()
    async def top(self, ctx):
        await ctx.send(embed = discord.Embed(title='Команды:', description='**!top_cash** - топ по балансу\n**!top_bank** - топ по балансу в банке\n**!top_lvl** - топ по уровню\n**!top_rep** - топ по репутации', color = embed_color))
    
    @commands.command()
    async def top_cash(self, ctx):
        embed = discord.Embed(title='Топ 10 сервера по балансу', color = embed_color)
        counter = 0
        for row in top_user('cash'):
            counter += 1
            embed.add_field(name=f'# {counter} | `{row[0]}`', value=f"Баланс: **{adv_num(row[1])}** {emoji_cash}", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def top_bank(self, ctx):
        embed = discord.Embed(title='Топ 10 сервера по балансу в банке', color = embed_color)
        counter = 0
        for row in top_user('bank'):
            counter += 1
            embed.add_field(name=f'# {counter} | `{row[0]}`', value=f"Баланс: **{adv_num(row[1])}** {emoji_cash}", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def top_rep(self, ctx):
        embed = discord.Embed(title='Топ 10 сервера по репутации', color = embed_color)
        counter = 0
        for row in top_user('rep'):
            counter += 1
            embed.add_field(name=f'# {counter} | `{row[0]}`', value=f"Репутация: **{row[1]}** {emoji_rep}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def top_lvl(self, ctx):
        embed = discord.Embed(title='Топ 10 сервера по уровню', color = embed_color)
        counter = 0
        for row in top_user('lvl'):
            counter += 1
            embed.add_field(name=f'# {counter} | `{row[0]}`', value=f"Уровень: **{row[1]}** {emoji_lvl}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def top_item(self, ctx):
        emb = discord.Embed(title='Топ 10 сервера по предметам', color = embed_color)
        counter = 0
        all_items = []
        for row in top_user():
            counter += 1
            rtx3060 = item_user('rtx3060', ctx.author.id)
            rtx3070 = item_user('rtx3070', ctx.author.id)
            rtx3080 = item_user('rtx3080', ctx.author.id)
            rtx3090 = item_user('rtx3090', ctx.author.id)
            if rtx3060 > 0:
                all_items.append({'RTX 3060': rtx3060})
            if rtx3070 > 0:
                all_items.append({'RTX 3070': rtx3070})
            if rtx3080 > 0:
                all_items.append({'RTX 3080': rtx3080})
            if rtx3090 > 0:
                all_items.append({'RTX 3090': rtx3090})
            for item in all_items:
                for item_ in item:
                    emb.add_field(name=f'# {counter} | `{row[0]}`', value=f"Предметов: **{list(item.values())[0]}**", inline=False)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Eco(client))
