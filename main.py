# imports
import os
from webserver import app
import discord
from replit import db
from discord.ext import commands
from pretty_help import PrettyHelp

# instantiate client
bot = commands.Bot(
  command_prefix=commands.when_mentioned_or(','),
  activity=discord.Game(name=",help"),
  status=discord.Status.idle,
  help_command = PrettyHelp(color=discord.Colour.gold()))


# event: On Server Join
@bot.event
async def on_guild_join(guild):
  db[str(guild.id)] = {
    'levels': {
      'users': {},
      'settings': {
        'lvl_roles': False,
        'roles' : None,
        'setup' : False
      }
    },
    'moderation': {
      'settings': {
        'muted_role': 'Muted'
      }
    }
  }


# Nilla Wafers
@bot.command(hidden=True, aliases=['nw'])
async def nillawafers(ctx):
  await ctx.send('https://cdn.discordapp.com/attachments/934179877710614561/934890380082679808/v09044g40000c5199mbc77ubkfeosl40.mov')


# load extensions
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


# run client
def run():

  bot.loop.create_task(app.run_task('0.0.0.0'))
  bot.run(os.environ['BOT_TOKEN'])
  
run()



'''  - - - USEFUL LINKS - - -
https://cog-creators.github.io/discord-embed-sandbox/
'''