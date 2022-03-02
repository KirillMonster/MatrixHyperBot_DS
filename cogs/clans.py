import discord
from discord.ext import commands
from db import check_clan_count, clan_users, embed_color, emoji_cash, item_user, adv_num, clan_cost, take_user, new_clan, check_clan_name, check_clan_count, not_money, get_clan, set_user, clan_users, check_clan, del_clan

class Clans(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def clan(self, ctx):
        if item_user('clan_id', ctx.author.id) is None:
            await ctx.send(embed=discord.Embed(title='Кланы:shield: !clan', description = f'**!newclan [навзание]** - `создать свой клан,цена - 50.000`{emoji_cash}', color = embed_color))
        else:
            if get_clan('id_owner', 'id_owner', ctx.author.id) == ctx.author.id:
                await ctx.send(embed=discord.Embed(title='Клан', description=f'Название: **{get_clan("name", "id_owner", ctx.author.id)}**\nУчастников: **{len(clan_users(get_clan("id", "id_owner", ctx.author.id)))}**', color= embed_color))
            else:
                pass

    @commands.command()
    async def newclan(self, ctx, name=None):
        if name is None:
            await ctx.send(f'**{ctx.author}**, вы не указали название нового клана.')
        else:
            if check_clan_name(name):
                if item_user('clan_id', ctx.author.id) is None:
                    if item_user('cash', ctx.author.id) >= clan_cost:
                        take_user('cash', clan_cost, ctx.author.id)
                        new_clan(name, ctx.author)
                        set_user('clan_id', get_clan('id', 'name', name), ctx.author.id)
                        await ctx.send(f'**{ctx.author}**, вы успешно создали новый клан под названием **{name}**')
                    else:
                        await ctx.send(not_money(ctx, clan_cost, item_user("cash", ctx.author.id)))
                else:
                    await ctx.send(f'**{ctx.author}**, вы уже состоите в клане.')
            else:
                await ctx.send(f'**{ctx.author}**, клан с таким именем уже существует.')

    @commands.command()
    async def joinclan(self, ctx, clan_id:int=None):
        if clan_id is None:
            await ctx.send(f'**{ctx.author}**, вы не указали id клана.')
        else:
            if check_clan(clan_id):
                if item_user('clan_id', ctx.author.id) == clan_id:
                    await ctx.send(f'**{ctx.author}**, вы уже состоите в клане.')
                else:
                    set_user('clan_id', clan_id, ctx.author.id)
                    await ctx.send(f'**{ctx.author.id}**, вы успешно присоеденились к клану **{get_clan("name", "clan_id", clan_id)}**')
            else:
                await ctx.send(f'**{ctx.author}**, клана с таким id не найден.')

    @commands.command()
    async def leftclan(self, ctx):
        if item_user('clan_id', ctx.author.id) is None:
            await ctx.send(f'**{ctx.author}**, вы не состоите в клане.')
        else:
            if get_clan('id_owner', 'id_owner', ctx.author.id) == ctx.author.id:
                await ctx.send(f'**{ctx.author}**, вы не можете выйти из своего клана так как вы владелец этого клана.')
            else:
                await ctx.send(f'**{ctx.author.id}**, вы успешно покинули клан **{get_clan("name", "clan_id", item_user("clan_id", ctx.author.id))}**')
                set_user('clan_id', None, ctx.author.id)

    @commands.command()
    async def delclan(self, ctx):
        if get_clan('id_owner', 'id_owner', ctx.author.id) == ctx.author.id:
            del_clan(item_user('clan_id', ctx.author.id))
            print('a')
            set_user('clan_id', None, ctx.author.id)
            print('c')
            await ctx.send(f'**{ctx.author}**, вы успешно удалил свой клан.')
        else:
            await ctx.send(f'**{ctx.author}**, вы не имеете своего клана.')


def setup(client):
    client.add_cog(Clans(client))
