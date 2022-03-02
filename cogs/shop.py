import discord
from discord.ext import commands
from Cybernator import Paginator
from db import item_user, give_user, take_user, items_price, items_sell, adv_num, adv_item, embed_color, emoji_cash, not_money

class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shop(self, ctx):
        emb = discord.Embed(title='Навигация', description='⏩ - следущая страница\n⏪ - продедущая страница\n❌ - закрыть', color=embed_color)
        emb_video = discord.Embed(title='Магазин Видеокарт',color=embed_color)
        emb_video.add_field(name='RTX 3060', value='Максимальный доход **2.500**:leaves:\nСтоимость - **100.000**:leaves:\nКоманда - **!buy rtx3060 [кол-во]**', inline=False)
        emb_video.add_field(name='RTX 3070', value='Максимальный доход **5.000**:leaves:\nСтоимость - **200.000**:leaves:\nКоманда - **!buy rtx3070 [кол-во]**', inline=False)
        emb_video.add_field(name='RTX 3080', value='Максимальный доход **7.500**:leaves:\nСтоимость - **400.000**:leaves:\nКоманда - **!buy rtx3080 [кол-во]**', inline=False)
        emb_video.add_field(name='RTX 3090', value='Максимальный доход **10.000**:leaves:\nСтоимость - **550.000**:leaves:\nКоманда - **!buy rtx3090 [кол-во]**\n\n\nСтраница 1/1', inline=False)
        embeds = [emb, emb_video]
        msg = await ctx.send(embed=emb)
        reactions = ['⏪','⏩']
        page = Paginator(self.client,message=msg,only=ctx.author,timeout=90,reactions=reactions,use_exit=True,exit_reaction=["❌"],delete_message=True,footer=False, embeds=embeds)
        await page.start()
    
    @commands.command()
    async def buy(self, ctx, item=None, count='1'):
        if item is None: 
            await ctx.send(f'**{ctx.author}**, укажите товар который желаете купить.')
        else: 
            if count.isdigit(): 
                count = int(count)
                if count > 0:
                    cash = item_user('cash', ctx.author.id)
                    if [i for i in ['rtx3060', 'rtx3070', 'rtx3080', 'rtx3090'] if i == item] != []:
                        for i in items_price:
                            price = i[item]
                            if cash >= price:
                                take_user('cash', price, ctx.author.id)
                                give_user(item, count, ctx.author.id)                              
                                await ctx.send(f'**{ctx.author}**, Вы успешно купили **{count}** видеокарт(у) **{adv_item(item)}**, за **{adv_num(price)}**{emoji_cash}')
                            else:
                                await ctx.send(not_money(ctx, price, cash))
                    else:
                        await ctx.send(f'**{ctx.author}**, такого товара нету в магазине.')
                else:
                    await ctx.send(f'**{ctx.author}**, укажите число больше 0.')
            else: 
                await ctx.send(f'**{ctx.author}**, укажите число.')

    @commands.command()
    async def sell(self, ctx, item=None, count='1'):
        if item is None: 
            await ctx.send(f'**{ctx.author}**, укажите товар который желаете продать.')
        else: 
            if count.isdigit() == True: 
                count = int(count)
                if count > 0:
                    if [i for i in ['rtx3060', 'rtx3070', 'rtx3080', 'rtx3090'] if i == item] != []:
                        for i in items_sell:
                            sale = i[item]
                            item_count = item_user(item, ctx.author.id)
                            if item_count >= count:
                                give_user('cash', sale, ctx.author.id)
                                take_user(item, count, ctx.author.id)
                                await ctx.send(f'**{ctx.author}**, Вы успешно продали **{count}** видеокарт(ы) **{adv_item(item)}**, за **{adv_num(sale)}**{emoji_cash}')
                            else:
                                await ctx.send(f'**{ctx.author}**, недостаточно товара(ов). Нехватает - **{adv_num(count-item_count)} {adv_item(item)}**')
                    else:
                        await ctx.send(f'**{ctx.author}**, такого товара несуществует.')
                else:
                    await ctx.send(f'**{ctx.author}**, укажите число больше 0.')
            else: 
                await ctx.send(f'**{ctx.author}**, укажите число.')

    @commands.command()
    async def items(self, ctx):
        all_items = []
        emb = discord.Embed(title='Ваши предметы', color=embed_color)
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
        if all_items == []:
            await ctx.send(f'**{ctx.author}**, у вас нету ниодного предмета.')
        else:
            for item in all_items:
                for item_ in item:
                    emb.add_field(name=item_, value=f'Количество: **{list(item.values())[0]}**', inline=False)
            await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Shop(client))
