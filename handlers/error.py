import config
import settings
import asyncio

import datetime
import discord
from discord.ext import commands

class error(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title = ':warning: | О нет, произошла ошибка в команде!',
                description = f'<a:768563657390030971:1041076662546219168> **Команда не найдена или введена неправильно!**',
                color = 0xDB0F0F
            )
            embed.set_footer(icon_url = self.client.user.avatar.url, text = f'{self.client.user.name} | Все права защищены')
            await ctx.send(embed=embed, delete_after=5)
        if isinstance(error, commands.errors.MissingPermissions):
            embed = discord.Embed(
                title = '🕹 | Недостаточно прав!',
                description = "<a:768563657390030971:1041076662546219168> **У вас не хватает прав для использование этой команды!**",
                color = discord.Color.red()
            )
            embed.set_footer(icon_url = self.client.user.avatar.url, text = f'{self.client.user.name} | Все права защищены')
            await ctx.send(embed = embed, delete_after=5)
        if isinstance(error, commands.errors.CommandInvokeError):
            embed = discord.Embed(
                title = '🐞 | Ошибка!',
                description = "<a:768563657390030971:1041076662546219168> **Произошла техническая неполадка в коде, данные об баге были отправлены разработчику.**",
                color=discord.Color.red()
            )
            embed.set_footer(icon_url = self.client.user.avatar.url, text = f'{self.client.user.name} | Все права защищены')
            await ctx.send(embed = embed, delete_after=5)
        if isinstance(error, commands.CommandInvokeError):
            logs = self.client.get_channel(settings.channels.bugs)
            embed = discord.Embed(
                title = "🧿 |  Баг",
                description = f'''**• Время:** {datetime.datetime.now()}
                **• Баг:** ```{error}```
                **• Канал:** <#{ctx.message.channel.id}> - {ctx.message.channel.id}
                **• Автор:** <@{ctx.author.id}> - {ctx.author.id}
                **• Сообщение:** `{ctx.message.content}`
                **• Полное Сообщение:** ```{ctx.message}```''',
                color = 0xdaab39
            )
            embed.set_footer(icon_url = self.client.user.avatar.url, text = f'{self.client.user.name} | Все права защищены')
            await logs.send(embed=embed)

async def setup(client):
    await client.add_cog(error(client))