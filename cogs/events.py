import discord
from discord.ext import commands

class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print (f"Logged on as MrSphericalBot - {self.client.user.id}\nDiscord.py Version: {discord.__version__}")     
        await self.client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=f's.help', url='https://www.youtube.com/c/%D0%9C%D0%B8%D1%81%D1%82%D0%B5%D1%80%D0%A1%D1%84%D0%B5%D1%80%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9'))

def setup(client):
    client.add_cog(events(client))