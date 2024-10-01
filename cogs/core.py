import discord
import os
from discord.ext import commands


class core(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


   # cmd: List Extensions
  @commands.command(hidden=True)
  @commands.has_permissions(administrator=True)
  async def listextensions(ctx):
    ext_list = ''
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        ext_list+=f'{filename[:-3]}\n'
      await ctx.send(ext_list)
     
     
   # cmd: Load Extension
  @commands.command(hidden=True)
  @commands.has_permissions(administrator=True)
  async def enable(self, ctx, extension):
    await ctx.send(f'Succesfully enabled {extension}!')
    self.bot.load_extension(f'cogs.{extension}')

     
   # cmd: Disable Extension
  @commands.command(hidden=True)
  @commands.has_permissions(administrator=True)
  async def disable(self, ctx, extension):
    await ctx.send(f'Succesfully disabled {extension}')
    self.bot.unload_extension(f'cogs.{extension}')

     
   # cmd: Ping Pong!
  @commands.command(hidden=True)  
  async def ping(ctx):
    await ctx.send(f'{ctx.message.author.mention} Pong :) !')
  ########### End Of Commands #############

def setup(bot):
  bot.add_cog(core(bot))