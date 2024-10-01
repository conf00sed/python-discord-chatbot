import discord
from replit import db
from discord.ext import commands
from collections import OrderedDict
from operator import getitem



class Levels(commands.Cog):
  """Commands used for user level information"""

  def __init__(self, bot):
    self.bot = bot
    self.lvl_roles = False
    self.roles = None
    self.setup_complete = False


  # event: On Member Join
  @commands.Cog.listener()
  async def on_member_join(self, member):
    
    users = db[f'{member.guild.id}']['levels']['users']
    await self.update_data(users, member)
    
    db[f'{member.guild.id}']['levels']['users'] = users


  # event: On Message
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot == False:

      try:
        users = db[f'{message.author.guild.id}']['levels']['users']

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(users, message.author, message)
        
        db[f'{message.author.guild.id}']['levels']['users'] = users
      except KeyError:
        db[str(message.author.guild.id)] = {
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
        
        
  ## func: Update User Data
  async def update_data(self, users, user):
    if not f'{user.id}' in users:
      users[f'{user.id}'] = {}
      users[f'{user.id}']['experience'] = 0
      users[f'{user.id}']['level'] = 1

  ## func: Add Experience
  async def add_experience(self, users, user, exp):
    users[f'{user.id}']['experience'] += exp

  ## func: Level Up Algorithm
  async def level_up(self, users, user, message):
    
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 3.5))

    if lvl_start < lvl_end:
      users[f'{user.id}']['level'] = lvl_end
      await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}!')

      ## Level Roles Logic
#      if self.lvl_roles:
#        if users[f'{user.id}']['level'] == 5:
#          await user.add_roles(self.roles['level 5'])
#        elif users[f'{user.id}']['level'] == 10:
#          await user.add_roles(self.roles['level 10'])
#        elif users[f'{user.id}']['level'] == 15:
#          await user.add_roles(self.roles['level 15'])
#        elif users[f'{user.id}']['level'] == 20:
#          await user.add_roles(self.roles['level 20'])
#        elif users[f'{user.id}']['level'] == 25:
#          await user.add_roles(self.roles['level 25'])


  # cmd: Config Level Roles 
  @commands.has_permissions(administrator=True)
  @commands.command(aliases=['lr'], hidden=True)
  async def levelroles(self, ctx, setting=None):
    """ Configure level roles (WIP) """
    
    if str(setting).lower() in ['true', 'enable', 'on']:
      self.lvl_roles = True
      await ctx.send(f'Level Autoroles set to: `{self.lvl_roles}`') 
      
    elif str(setting).lower() in ['disable', 'off', 'false']:
      self.lvl_roles = False
      await ctx.send(f'Level Autoroles set to: `{self.lvl_roles}`')
      
    else:
      await ctx.send('Please use `enable` or `disable`')


  # cmd: Get Level
  @commands.command()
  async def level(self, ctx, member: discord.Member = None):
    """ Get user level """

    users = db[f'{ctx.guild.id}']['levels']['users']

    
    if member == None:
      id = ctx.message.author.id
      lvl = users[str(id)]['level']

      await ctx.send(f'{ctx.message.author.mention} you are at level {lvl}!')

    else:
      id = member.id
      db[f'{member.guild.id}']['levels']['users'] = users
      lvl = users[str(id)]['level']
      
      await ctx.send(f'{member} is at level {lvl}!') 
      await ctx.message.add_reaction('✅')


  # cmd: Give Experience
  @commands.has_permissions(administrator=True)
  @commands.command()
  async def givexp(self, ctx, exp, member:discord.Member=None):
    """ Give a user experience """

    if member == None:
      member = ctx.message.author

    users = db[f'{ctx.guild.id}']['levels']['users']
    await self.add_experience(users, member, int(exp))
    await ctx.message.add_reaction('✅')
  

  # cmd: Take Away Experience
  @commands.has_permissions(administrator=True)
  @commands.command()
  async def takexp(self, ctx, exp, member:discord.Member=None):
    """ Take away experience from a user """

    if member == None:
      member = ctx.message.author

    users = db[f'{ctx.guild.id}']['levels']['users']
    await self.add_experience(users, member, int(exp)*-1)
    await ctx.message.add_reaction('✅')


  #cmd: Leaderboard
  @commands.command()
  async def leaderboard(self, ctx, x=10):
    """ Displays highest leveled users in the server """

    users = db[f'{ctx.guild.id}']['levels']['users']
    ordered = OrderedDict(sorted(users.items(), key = lambda x: getitem(x[1], 'experience'), reverse=True))

    em = discord.Embed(title = f'**Highest leveled members in** {ctx.guild.name}', color=discord.Colour.gold())
    index = 1
    for userid in ordered:
      # member = discord.utils.get(ctx.guild.members, id=int(userid))
      member = await self.bot.fetch_user(userid)
      em.add_field(name = f'{index}: {member}' , value = f'{users[str(member.id)]["experience"]}', inline=False)
      
      if index == x:
        break
      else:
        index += 1
      
    await ctx.send(embed=em)
    await ctx.message.add_reaction('✅')



def setup(bot):
  bot.add_cog(Levels(bot))