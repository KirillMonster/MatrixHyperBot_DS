import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
url_last = None
volume_music = 1
music_list = []
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'no_warnings': True,
               'default_search': 'auto', 'noplaylist': True}


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def music(self, ctx):
        await ctx.send(embed=discord.Embed(title='Музыка:notes: **!music**', description='**!play [url]** - `воспроизведение музыки.`\n**!volume [от 0 до 100]** - `изменение громкости музыки.`\n**!repeat** - `воспроизведение предыдущей музыки.`\n**!join** - `подключить бота к голосовому чату.`\n**!pause** - `пауза.`\n**!resume** - `продолжить.`\n**!skip** - `Пропустить музыку.`\n**!disconnect** - `отключить бота от гос чата.`', color=0x00eeff))

    @commands.command()
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Бот не подключен к голосовому каналу. Команда - !join')
        else:
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url=None):
        global url_last
        if url is None:
            await ctx.send('Вы не указали ссылку на видео в YouTube!')
        else:
            url_last = url
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                voice_channel = ctx.author.voice.channel
                if ctx.voice_client is None:
                    await voice_channel.connect()
                else:
                    await ctx.voice_client.move_to(voice_channel)
                # TODO: добавить очередь
                if ctx.voice_client.is_playing():
                    music_list.append(url)
                    ctx.voice_client.stop()
                vc = ctx.voice_client
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    try:
                        info = ydl.extract_info(url, download=False)
                        url2 = info['formats'][0]['url']
                        vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
                            executable="ffmpeg/ffmpeg.exe", source=url2, **FFMPEG_OPTIONS), volume=volume_music))
                        await ctx.send(f'Сейчас проигрывается музыка: **{info["title"]}.**\nГромкость **{volume_music*100}%.**')
                    except Exception as e:
                        await ctx.send(f'**{ctx.author}**, вы ввели неверную ссылку на видео из YouTube')
                        print(e)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('Подключитесь к голосовому каналу!')
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Бот не подключен к голосовому каналу. Команда - !join')
        else:
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                if ctx.voice_client.is_playing():
                    await ctx.send('Пропустил ⏩')
                    ctx.voice_client.stop()
                else:
                    await ctx.send('Музыки небыло.')

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Бот не подключен к голосовому каналу. Команда - !join')
        else:
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                if ctx.voice_client.is_playing():
                    await ctx.send('Пауза ⏸')
                    await ctx.voice_client.pause()
                else:
                    await ctx.send('Я сейчас не играю музыку!')

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Бот не подключен к голосовому каналу. Команда - !join')
        else:
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                if ctx.voice_client.is_paused():
                    await ctx.send('Продолжаю ⏯')
                    await ctx.voice_client.resume()
                else:
                    await ctx.send('Нету остановленной музыки!')

    @commands.command()
    async def repeat(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Бот не подключен к голосовому каналу. Команда - !join')
        else:
            if ctx.author.voice is None:
                await ctx.send('Подключитесь к голосовому каналу!')
            else:
                if url_last is None:
                    await ctx.send('Небыло последней музыки')
                else:
                    await self.play(ctx, url_last)

    @commands.command()
    async def volume(self, ctx, count: int = None):
        global volume_music
        if count is None:
            await ctx.send(f'**{ctx.author}**, вы не указали громкость.')
        else:
            if 0 <= count <= 100:
                volume_music = count/100
                await ctx.send(f'**{ctx.author}**, вы установили громкость на **{volume_music*100}%**')
            else:
                await ctx.send(f'**{ctx.author}**, введите громкость звука от 0 до 100.')


def setup(client):
    client.add_cog(Music(client))
