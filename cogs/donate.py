import discord
from discord.ext import commands
from tokens import TOKEN_QIWI
from pyqiwip2p import QiwiP2P
from random import randint
from datetime import datetime
from db import new_pay, all_pays

p2p = QiwiP2P(auth_key=TOKEN_QIWI)

class Donate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def donate(self, ctx, amount=None, *args):
        if amount is None:
            await ctx.send(f'**{ctx.author}**, введите сумму которой желаете поддержать автора и сообщение автору (по желанию).')
        else:
            if amount.isdigit():
                amount = int(amount)
                if amount > 9:
                    comment = f'ID {ctx.author.id}, ID заказа: '
                    bill = p2p.bill(amount=amount, lifetime=15, comment=comment)
                    new_pay(ctx.author, amount, bill.bill_id, p2p.check(bill_id=bill).status)
                    await ctx.send(embed=discord.Embed(title='Спасибо!', description=f'Оплата для **{ctx.author}**\n:moneybag: Оплата на **{amount}** RUB\n:link: Сыллка для оплаты: {bill.pay_url}\n:hourglass_flowing_sand:Ссылка действительна в течении 15 минут.\n:warning:**Внимание!**:warning:\nЭту оплату может сделать любой игрок, и если оплатили не вы, то все равно вы получите бонус за поддержку', color = 0x00eeff))
                else:
                    await ctx.send(f'**{ctx.author}**, введите целую сумму больше 9 рублей.')
            else:
                await ctx.send(f'**{ctx.author}**, введите целую сумму.')
    
    @commands.command
    async def donates(self, ctx):
        print(all_pays(ctx.author.id))
    
    @commands.command()
    async def statuspay(self, ctx):
       pass         
def setup(client):
    client.add_cog(Donate(client))
