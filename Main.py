import discord
from discord.ext import commands
import asyncio
import inspect
import time
from itertools import cycle
import os

bot = commands.Bot(command_prefix = "d")
status = ["testing the bot", "dhelp"]

async def change_status():
  await bot.wait_until_ready()
  msgs = cycle(status)
  
  while not bot.is_closed:
    current_status = next(msgs)
    await bot.change_presence(game=discord.Game(name=current_status))
    await asyncio.sleep(5)

@bot.event
async def on_ready():
	print('Logged in as')
	print("User name:", bot.user.name)
	print("User id:", bot.user.id)
	print('---------------')
	
def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497"
    
@bot.command(pass_context=True)
async def ping(ctx):
    """Pings the bot and gets a response time."""
    pingtime = time.time()
    pingms = await bot.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await bot.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def mute(ctx, user: discord.Member, *, arg):
	if arg is None:
		await bot.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await bot.add_roles(user, role)
	embed = discord.Embed(title="Mute", description=" ", color=0xFFA500)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def unmute(ctx, user: discord.Member, *, arg):
	if arg is None:
		await bot.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await bot.remove_roles(user, role)
	embed = discord.Embed(title="Unmute", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, arg):
	if arg is None:
		await bot.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await bot.kick(user)
	embed = discord.Embed(title="Kick", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
  
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, arg):
	if arg is None:
		await bot.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await bot.ban(user)
	embed = discord.Embed(title="Ban", description=" ", color=0xFF0000)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	server = ctx.message.server
	embed = discord.Embed(title="Warn", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
	await bot.send_message(user, "You have been warned for: {}".format(reason))
	await bot.send_message(user, "from: {} server".format(server))
	
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addrank(ctx, *, name = None):
	author = ctx.message.author
	server = ctx.message.server
	role = discord.utils.get(ctx.message.server.roles, name=name)
	await bot.create_role(server, name=name)
	await bot.say("the role has been created :thumbsup:")
	
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def delrank(ctx, *, role_name):
  role = discord.utils.get(ctx.message.server.roles, name=role_name)
  if role:
    try:
      await bot.delete_role(ctx.message.server, role)
      await bot.say("The role {} has been deleted!".format(role.name))
    except discord.Forbidden:
      await bot.say("Missing Permissions to delete this role!")
  else:
    await bot.say("The role doesn't exist!")

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await bot.add_roles(user, role)
    text = await bot.say(f'{author.mention} I have added the {role.name} role to a user {user.name}'.format(role.name))
    await bot.delete_message(ctx.message)
    await asyncio.sleep(5)
    await bot.delete_message(text)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await bot.remove_roles(user, role)
    text = await bot.say(f'{author.mention} I have remove the {role.name} role to a user {user.name}'.format(role.name))
    await bot.delete_message(ctx.message)
    await asyncio.sleep(5)
    await bot.delete_message(text)

@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True, kick_members=True)
async def giverole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await bot.add_roles(user, role)
    text = await bot.say(f'{author.mention} I have added the {role.name} role to a user {user.name}'.format(role.name))
    await bot.delete_message(ctx.message)
    await asyncio.sleep(5)
    await bot.delete_message(text)
	
@bot.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
    res = eval(command)
    if inspect.isawaitable(res):
        await bot.say(await res)
    else:
    	await bot.say(res)
	
bot.loop.create_task(change_status())
bot.run(os.environ['BOT_TOKEN'])
