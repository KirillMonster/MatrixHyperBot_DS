import discord
from discord.ext import commands
import asyncio
import random
import sqlite3
from db import all_users, item_user, check_user, percent, adv_num, emoji_cash, take_user, give_user, item_crypto, new_crypto, check_crypto
db = sqlite3.connect("server.db")
sql = db.cursor()
price, lastprice = None, None

def bank_deposit():
    for user in all_users():
        bank = sql.execute(f'SELECT `bank` FROM `users` WHERE `id` = ?',(user[0],)).fetchone()[0]
        if bank >= 200:
            sql.execute(f'UPDATE `users` SET `bank` = bank + ? WHERE `id` = ?',(int(bank*percent),user[0],))
    db.commit()


async def hypercoin():
    global price, last_price
    if check_crypto('hypercoin') is None:
        new_crypto('hypercoin', 10000)
    else:
        while True:
            price = item_crypto('hypercoin')+random.randint(-999,999)
            await asyncio.sleep(3600)


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def bank(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(f'Баланс банка пользователя **{ctx.author}** составляет **{adv_num(item_user("bank", ctx.author.id))}** {emoji_cash}')
        else:
            if check_user(member.id):
                await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных.')
            else:
                await ctx.send(f'Баланс банка пользователя **{member}** составляет **{adv_num(item_user("bank", member.id))}** {emoji_cash}')
                
    @commands.command()
    async def bankpay(self, ctx, member: discord.Member = None, amount: int=None):
        if member is None:
            await ctx.send(f'**{ctx.author}**, вы не указали игрока.')
        else:
            if check_user(member.id):
                await ctx.send(f'**{ctx.author}**, пользователя под ником **{member}** не существует в базе данных.')
            else:
                if member.id == ctx.author.id:
                    await ctx.send(f'**{ctx.author}**, вы не можете указать самого себя.')
                else:
                    if amount is None:
                        await ctx.send(f'**{ctx.author}**, вы не указали сумму.')
                    else:
                        if amount > 0:
                            if item_user('bank', ctx.author.id) >= amount:
                                take_user('bank', amount, ctx.author.id)
                                give_user('bank', amount, member.id)
                                await ctx.send(f'**{ctx.author}**, вы успешно отправили **{adv_num(amount)}** {emoji_cash} пользователю **{member}**.')
                            else:
                                await ctx.send(f'**{ctx.author}**, недостаточно средств, нехватает - **{adv_num(amount-item_user("bank", ctx.author.id))}** {emoji_cash}')
                        else:
                            await ctx.send(f'**{ctx.author}**, укажите сумму больше 0 {emoji_cash}')
    
    @commands.command()
    async def deposit(self, ctx, amount: int=None):
        if amount is None:
            await ctx.send(f'**{ctx.author}**, вы не указали сумму.')
        else:
            if amount > 0:
                if item_user('cash', ctx.author.id) >= amount:
                    give_user('bank', amount, ctx.author.id) 
                    take_user('cash', amount, ctx.author.id)
                    await ctx.send(f'**{ctx.author}**, вы успешно положили **{adv_num(amount)}** {emoji_cash} на депозитный счёт.')
                else:
                    await ctx.send(f'**{ctx.author}**, недостаточно средств, нехватает - **{adv_num(amount-item_user("cash", ctx.author.id))}**{emoji_cash}')
            else:
                await ctx.send(f'**{ctx.author}**, укажите сумму больше 0 {emoji_cash}')
    
    @commands.command()
    async def withdraw(self, ctx, amount: int=None):
        if amount is None:
            await ctx.send(f'**{ctx.author}**, вы не указали сумму.')
        else:
            if amount > 0:
                if item_user('bank', ctx.author.id) >= amount:
                    give_user('cash', amount, ctx.author.id) 
                    take_user('bank', amount, ctx.author.id)
                    await ctx.send(f'**{ctx.author}**, вы успешно сняли со счёта банка **{adv_num(amount)}** {emoji_cash}')
                else:
                    await ctx.send(f'**{ctx.author}**, недостаточно средств, нехватает - **{adv_num(amount-item_user("bank", ctx.author.id))}**{emoji_cash}')
            else:
                await ctx.send(f'**{ctx.author}**, укажите сумму больше 0 {emoji_cash}')
    
def setup(client):
    client.add_cog(Bank(client))
