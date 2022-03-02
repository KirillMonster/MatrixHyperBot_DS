import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from db import embed_color
ua = UserAgent()
HEADERS = {
    'User-Agent': ua.random
}

URL_FREE = 'https://www.epicgames.com/store/ru/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierFree&count=1000'

class EpicGames(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def freegames(self, ctx):
        HEADERS['User-Agent'] = ua.random
        response = requests.get(URL_FREE, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('li', class_='css-lrwy1y')
        games = []
        for item in items:
            if not item.find('div', class_='css-1h2ruwl').get_text(strip=True) in games:
                games.append(item.find('div', class_='css-1h2ruwl').get_text(strip=True))
        games = '\n'.join(games)
        await ctx.send(embed=discord.Embed(title='Бесплатные игры на сегодня', description=games, color=embed_color))
        
def setup(client):
    client.add_cog(EpicGames(client)) 