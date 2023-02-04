import discord
import settings
from discord.ext import commands

class Panel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(emoji='🔓', style=discord.ButtonStyle.green, label='Открыть', custom_id = "panel:open")
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        ch = interaction.channel
        name = ch.name.replace("closed", "ticket")
        await ch.edit(name=name)
        embed = discord.Embed(
            title="🥊 | Тикеты",
            description=f"<a:768563657390030971:1041076662546219168>  *Тикет открыт <@{interaction.user.id}>*",
            color=0x370acd
        )
        embed.set_footer(icon_url=settings.misc.avatar_url, text=settings.misc.footer)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(emoji = '🀄', style = discord.ButtonStyle.blurple, label = 'В архив', custom_id = "panel:archive")
    async def archive(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        ch = interaction.channel
        role = interaction.guild.get_role(settings.roles.archive_channels)
        if role in user.roles:
            category = discord.utils.get(interaction.guild.channels, name=settings.channels.ticket_archive)
            if len(category.channels) > 48:
                embed = discord.Embed(
                    title="📚 | Архив Каналов",
                    description="<a:768563657390030971:1041076662546219168> **Архив засорился!**",
                    color=0x674ea7
                )
                embed.set_footer(icon_url=settings.misc.avatar_url, text=settings.misc.footer)
                embed.set_image(url="https://media.tenor.com/r3t0LfS0dCwAAAAd/toilet-meme.gif")
                await interaction.response.edit_message(view=None, embed=embed)
            else:
                embed = discord.Embed(
                    title="📚 | Архив Каналов",
                    description="<a:768563657390030971:1041076662546219168> **Перемещение тикета в архив....**",
                    color=0x674ea7
                )
                embed.set_footer(icon_url=settings.misc.avatar_url, text=settings.misc.footer)
                await interaction.response.edit_message(view=None, embed=embed)
                await ch.edit(
                    sync_permissions=True,
                    category=category,
                    reason=f'Архивирование канала | {interaction.user.name}#{interaction.user.discriminator}'
                )
        else:
            await interaction.response.send_message(f'**У Вас отсутствует роль <@&{settings.roles.archive_channels}>!**', ephemeral=True)
    @discord.ui.button(emoji='⛔', style=discord.ButtonStyle.red, label='Удалить', custom_id = "panel:close")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        ch = interaction.channel
        role = interaction.guild.get_role(settings.roles.manage_tickets)
        if role in user.roles:
            await interaction.response.send_message('*Удаление тикета...*')
            await ch.delete()
        else:
            await interaction.response.send_message(f'**У Вас отсутствует роль <@&{settings.roles.manage_tickets}>!**', ephemeral=True)

class Close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🔒', style=discord.ButtonStyle.red, label='Закрыть', custom_id = "close:close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        ch = interaction.channel
        name = ch.name.replace("ticket", "closed")
        await ch.edit(name = name)
        embed = discord.Embed(
            title="🥊 | Тикеты",
            description=f"<a:768563657390030971:1041076662546219168>  *Тикет закрыт <@{interaction.user.id}>*",
            color=0x370acd
        )
        embed.set_footer(icon_url=settings.misc.avatar_url, text=settings.misc.footer)
        manage = discord.Embed(
            description="```Панель управления```"
        )
        await interaction.response.send_message(embeds=[embed, manage], view = Panel())
class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label = "Жалоба", emoji = "🥊", description = "Отправьте жалобу на нарушителя!"),
            discord.SelectOption(label = "Вопрос", emoji = "🔎", description = "Задайте вопрос")
        ]
        super().__init__(placeholder = "Выберите тему тикета",max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        tickets = discord.utils.get(guild.channels, name = settings.channels.tickets)
        tickets_count = discord.utils.get(guild.channels, id = settings.channels.tickets_count)
        flatten = [msg async for msg in tickets_count.history(limit=100)]
        msg = discord.utils.get(flatten, id = settings.misc.tickets_count)
        count = msg.content
        count = count[1:]
        count = int(f"1{count}")
        count = count + 1
        count = str(count)
        count = count[1:]
        count = str(f"0{count}")

        if self.values[0] == "Жалоба":
            topic = "Жалоба"
        elif self.values[0] == "Вопрос":
            topic = "Вопрос"

        await interaction.response.send_message('*Создание тикета.. Ожидайте.*', ephemeral=True)
        mods = guild.get_role(settings.roles.mods_tickets)

        ch = await guild.create_text_channel(
            name = f'ticket-{count}',
            category = tickets,
            topic = f"**Автор:** <@{interaction.user.id}>\n**Номер тикета:** {count}\n**Тема:** {topic}",
            reason = f"Открытие тикета | {interaction.user.name}#{interaction.user.discriminator}"
        )
        await ch.set_permissions(
            guild.default_role,
            view_channel=False,
            send_messages=False,
        )
        await ch.set_permissions(
            interaction.user,
            send_messages=True,
            read_message_history=True,
            read_messages=True
        )
        await ch.set_permissions(
            mods,
            send_messages=True,
            read_message_history=True,
            read_messages=True
        )
        await msg.edit(content = str(count))
        embed = discord.Embed(
            title="🥊 | Тикеты",
            description=f"*Поддержка скоро свяжется с вами.\nДля закрытия нажмите кнопку ниже.*\n*Информация для поддержки:*\n```Тема: {topic}```",
            color=0x370acd
        )
        embed.set_footer(icon_url = settings.misc.avatar_url, text = settings.misc.footer)
        await ch.send(f'Добро пожаловать, <@{interaction.user.id}>', embed=embed, view = Close())
class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Select())
class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(emoji='🎲', style=discord.ButtonStyle.green, label = 'Открыть тикет', custom_id = "persistent_view:create")
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(view = SelectView(), ephemeral = True)

class ticket(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role(1071141626866569286)
    async def ticket(self, ctx):
        embed = discord.Embed(
            title = "🥊 | Тикеты",
            description = "<a:768563657390030971:1041076662546219168> *У Вас есть вопрос или жалоба? По нажатии кнопки бот создаст тикет-канал, в котором вы начнёте разговор с представителем модерации.*",
            color = 0x370acd
        )
        embed.set_footer(icon_url=self.client.user.avatar.url, text=f'{self.client.user.name} | Все права защищены')
        await ctx.send(embed=embed, view = PersistentView())

async def setup(client):
    await client.add_cog(ticket(client))