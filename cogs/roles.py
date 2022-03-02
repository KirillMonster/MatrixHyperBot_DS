import discord
from discord.ext import commands
from discord import utils
from config import ROLES_GAMES, ROLES_GENDER, POST_ID_GAMES, POST_ID_GENDER, EXCROLES, MAX_ROLES_GAMES, MAX_ROLES_GENDER
 
class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == POST_ID_GAMES:
            channel = self.client.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=ROLES_GAMES[emoji]) # объект выбранной роли (если есть)

                if(len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_GAMES):
                    await member.add_roles(role)
                    #print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    #print('[ERROR] Too many roles for user {0.display_name}'.format(member))
           
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
        
        elif payload.message_id == POST_ID_GENDER:
            channel = self.client.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=ROLES_GENDER[emoji]) # объект выбранной роли (если есть)
           
                if(len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_GENDER):
                    await member.add_roles(role)
                    #print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    #print('[ERROR] Too many roles for user {0.display_name}'.format(member))
           
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        channel = self.client.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
        try:
            if POST_ID_GAMES == payload.message_id or POST_ID_GENDER == payload.message_id:
                ROLE_REM = None
                emoji = str(payload.emoji)
                print(emoji)
                if emoji in ROLES_GENDER:
                    ROLE_REM = ROLES_GENDER[emoji]
                if emoji in ROLES_GAMES:
                    ROLE_REM = ROLES_GAMES[emoji]
                if not ROLE_REM is None:
                    role = utils.get(message.guild.roles, id=ROLE_REM) # объект выбранной роли (если есть)
                    await member.remove_roles(role)
                    print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
                else:
                    print('why?)')
        except KeyError as e:
            print(f'[ERROR] KeyError, no role found for {emoji}')
        except Exception as e:
            print(repr(e))
            
def setup(client):
    client.add_cog(Roles(client))
    