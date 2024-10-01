import discord
from discord.ext import commands


# Admin Protection
class Sinner(commands.Converter):

  async def convert(self, ctx, argument):

    argument = await commands.MemberConverter().convert(ctx, argument)
    permission = argument.guild_permissions.administrator

    if not permission:
      return argument

    else:
      raise commands.BadArgument("You cannot punish other staff members")


# Muted Role Check
class Redeemed(commands.Converter):

  async def convert(self, ctx, argument):

    argument = await commands.MemberConverter().convert(ctx, argument)
    muted = discord.utils.get(ctx.guild.roles, name="Muted")

    if muted in argument.roles: 
      return argument 

    else:
      raise commands.BadArgument("The user was not muted.")
      
      
# Handles Mute setup
async def mute(ctx, user, reason):
  role = discord.utils.get(ctx.guild.roles, name="Muted")

  if not role:
    try:
      muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
      for channel in ctx.guild.channels: 
        await channel.set_permissions(muted, send_messages=False, read_message_history=True, read_messages=True)

    except discord.Forbidden:
      return await ctx.send("I have no permissions to make a muted role") 

    await user.add_roles(muted) 
    await ctx.send(f"{user.mention} has been sent to hell for {reason}")

  else:
    await user.add_roles(role) 
    await ctx.send(f"{user.mention} has been sent to hell for {reason}")
      


class Moderation(commands.Cog):
  """Commands used to moderate your guild"""
  
  def __init__(self, bot):
    self.bot = bot
  
  async def __error(self, ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send(error)
  
  # cmd: Ban
  @commands.command(aliases=["banish"])
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, user: Sinner=None, reason=None):
    """Ban users from the server"""
    
    if not user: 
      return await ctx.send("You must specify a user")
    
    try: 
      await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
      await ctx.send(f"{user.mention} was cast out for {reason}.")

    except discord.Forbidden:
      return await ctx.send("Are you trying to ban someone higher than the bot")


  # cmd: Softban
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def softban(self, ctx, user: Sinner=None, reason=None):
    """Temporarily restricts access to server"""
    
    if not user: 
      return await ctx.send("You must specify a user")
    
    try: 
      await ctx.guild.ban(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
      await ctx.guild.unban(user, "Temporarily Banned")
    except discord.Forbidden:
      return await ctx.send("Are you trying to soft-ban someone higher than the bot?")
  

  # cmd: Mute
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def mute(self, ctx, user: Sinner, reason=None):
    """Restricts user from talking in all channels"""

    await mute(ctx, user, reason or "treason") 
  

  # cmd: Kick
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, user: Sinner=None, reason=None):
    """Kicks user from server"""

    if not user:
      return await ctx.send("You must specify a user")
    
    try: 
      await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 

    except discord.Forbidden:
      return await ctx.send("Are you trying to kick someone higher than the bot?")


  # cmd: Purge
  @commands.command(aliases=['clean', 'clear', 'delete'])
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, limit: int):
    """Bulk deletes messages"""
    
    await ctx.channel.purge(limit=limit + 1) 
    await ctx.send(f"Bulk deleted `{limit}` messages", delete_after=4) 
  

  # cmd: Unmute
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unmute(self, ctx, user: Redeemed):
    """Unmutes a muted user"""

    await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
    await ctx.send(f"{user.mention} has been unmuted")
  

  # cmd: Block
  @commands.command(aliases=['restrict'])
  @commands.has_permissions(ban_members=True)
  async def block(self, ctx, user: Sinner=None):
    """
    Blocks a user from chatting in current channel.
       
    Similar to mute but instead of restricting access
    to all channels it restricts in current channel.
    """
                
    if not user: 
      return await ctx.send("You must specify a user")
                
    await ctx.set_permissions(user, send_messages=False) 
  

  # cmd: Unblock
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unblock(self, ctx, user: Sinner=None):
    """Unblocks a user from current channel"""
                
    if not user:
      return await ctx.send("You must specify a user")
    
    await ctx.set_permissions(user, send_messages=True) 
                
                
def setup(bot):
  bot.add_cog(Moderation(bot))