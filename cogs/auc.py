import discord
from discord.ext import commands
from db import embed_color, take_user, give_user, adv_item, adv_num, top_auc, item_user, new_auc, del_auc, check_auc, get_auc
from Cybernator import Paginator

class Auc(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def auc(self, ctx):
        emb = discord.Embed(title='Навигация', description='⏩ - следущая страница\n⏪ - продедущая страница\n❌ - закрыть', color=embed_color)
        emb_help = discord.Embed(title='Команды', description='**!auc_sell [предмет] [цена]** - `восстановление предмета на аукцион.`\n**!auc_buy [id предмета]** - `купить предмет с аукциона.`', color=embed_color)
        emb_auc = discord.Embed(title='Аукцион', color=embed_color)
        count = 0
        for row in top_auc():
            count += 1
            emb_auc.add_field(name=f'Товар: {adv_item(row[1])}', value=f'Стоимость: **{adv_num(row[2])}**:leaves:\nID: **{row[3]}**\nВладелец: **{row[0]}**', inline=False)
        embeds = [emb, emb_help, emb_auc]
        msg = await ctx.send(embed=emb)
        reactions = ['⏪','⏩']
        page = Paginator(self.client,message=msg,only=ctx.author,timeout=90,reactions=reactions,use_exit=True,exit_reaction=["❌"],delete_message=True,footer=False, embeds=embeds)
        await page.start()
    
    @commands.command()
    async def auc_sell(self, ctx, item=None, cost=None):
        if item is None:
            await ctx.send(f'**{ctx.author}**, укажите товар который желаете выставить на аукцион.')
        else:
            if cost is None:
                await ctx.send(f'**{ctx.author}**, укажите цену товара')
            else:
                if cost.isdigit():
                    cost = int(cost)
                    if cost > 0:
                        if item in ['rtx3060', 'rtx3070', 'rtx3080', 'rtx3090']:
                            item_ = item_user(item, ctx.author.id)
                            if item_ > 0:
                                take_user(item, 1, ctx.author.id)
                                new_auc(ctx.author, ctx.author.id, cost, item)
                                await ctx.send(f'**{ctx.author}**, вы успешно выставили товар на аукцион.')
                            else:
                                await ctx.send(f'**{ctx.author}**, вы не имеете такого товара.')
                        else:
                            await ctx.send(f'**{ctx.author}**, такого товара не существует.')
                    else:
                        await ctx.send(f'**{ctx.author}**, укажите цену товара больше 0.')
                else:
                    await ctx.send(f'**{ctx.author}**, укажите цену товара')
    
    @commands.command()
    async def auc_buy(self, ctx, item_id=None):
        if item_id is None:
            await ctx.send(f'**{ctx.author}**, укажите ID товара который желаете купить на аукционе.')
        else:
            if item_id.isdigit():
                item_id = int(item_id)
                if check_auc(item_id):
                    cash = item_user('cash', ctx.author.id)
                    price = get_auc(item_id)[0]
                    id_owner = get_auc(item_id)[1]
                    print('as')
                    if id_owner == ctx.author.id:
                        await ctx.send(f'**{ctx.author}**, вы не можете купить товар у самого себя.')
                    else:
                        if cash >= price:
                            take_user(cash, price, ctx.author.id)
                            give_user(cash, price, id_owner)
                            del_auc(item_id)
                            await ctx.send(f'**{ctx.author}**, вы успешно купили **** видеокарт(у) ****, за **{adv_num(price)}**:leaves:')
                        else:
                            await ctx.send(f'**{ctx.author}**, недостаточно средств, нехватает - **{adv_num(price-cash)}**:leaves:')
                else:
                    await ctx.send(f'**{ctx.author}**, такого ID товара нет на аукционе.')
            else:
                await ctx.send(f'**{ctx.author}**, укажите ID товара')
                
def setup(client):
    client.add_cog(Auc(client))