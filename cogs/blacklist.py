import discord
from discord.ext import commands

bans = [
       972546611685261312, # atom bot
       962808419998388234, # Сфер-помощник
       954046288104685568, # sevaatom
       489082344159051786, # atomseva
       932611419197816832, # Военкомат
       933030522186264596, # BigSmoke
       932541542219006013, # Walter_FS
       821762235243954216, # kjkszpj
       858376307321733130] # valik505🇾🇪

class blacklist(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):


        if member.id not in bans:
            return
        else:
            await member.ban(reason="Многократные нарушения правил, угрозы, превышения полномочий.")
            
            notify = self.client.get_user(678632704874381334)
            embed = discord.Embed(
                title = "🎱 |  Авто-Бан",
                description = f"Пользователь {member} попытался зайти на сервер!",
                color = 0xc01919
            )
            await notify.send(embed=embed)


        


def setup(client):
    client.add_cog(blacklist(client))