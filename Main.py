import discord
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import os

client = commands.Bot(command_prefix=("/"))
status = ["testing the bot", "/help"]

async def change_status():
  await client.wait_until_ready()
  msgs = cycle(status)
  
  while not client.is_closed:
    current_status = next(msgs)
    await client.change_presence(game=discord.Game(name=current_status))
    await asyncio.sleep(5)
    
player = {}	

@client.event
async def on_ready():
	print('Logged in as')
	print("User name:", client.user.name)
	print("User id:", client.user.id)
	print('---------------')
    
@client.command(pass_context=True)
async def ping(ctx):
    """Pings the bot and gets a response time."""
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def mute(ctx, user: discord.Member, *, arg):
	if arg is None:
		await client.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await client.add_roles(user, role)
	embed = discord.Embed(title="Mute", description=" ", color=0xFFA500)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await client.say(embed=embed)
	
@client.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def unmute(ctx, user: discord.Member, *, arg):
	if arg is None:
		await client.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await client.remove_roles(user, role)
	embed = discord.Embed(title="Unmute", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await client.say(embed=embed)

@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, arg):
	if arg is None:
		await client.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await client.kick(user)
	embed = discord.Embed(title="Kick", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await client.say(embed=embed)
  
@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, arg):
	if arg is None:
		await client.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await client.ban(user)
	embed = discord.Embed(title="Ban", description=" ", color=0xFF0000)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await client.say(embed=embed)
	
@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await clieng.say("please say a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	server = ctx.message.server
	embed = discord.Embed(title="Warn", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await client.say(embed=embed)
	await client.send_message(user, "You have been warned for: {}".format(reason))
	await client.send_message(user, "from: {} server".format(server))
	
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addrank(ctx, *, name = None):
	author = ctx.message.author
	server = ctx.message.server
	role = discord.utils.get(ctx.message.server.roles, name=name)
	await client.create_role(server, name=name)
	await client.say("the role has been created :thumbs_up:")
	
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def delrank(ctx, *, role_name):
  role = discord.utils.get(ctx.message.server.roles, name=role_name)
  if role:
    try:
      await client.delete_role(ctx.message.server, role)
      await client.say("The role {} has been deleted!".format(role.name))
    except discord.Forbidden:
      await client.say("Missing Permissions to delete this role!")
  else:
    await client.say("The role doesn't exist!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await client.add_roles(user, role)
    text = await client.say(f'{author.mention} I have added the {role.name} role to a user {user.name}'.format(role.name))
    await client.delete_message(ctx.message)
    await asyncio.sleep(5)
    await client.delete_message(text)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await client.remove_roles(user, role)
    text = await client.say(f'{author.mention} I have remove the {role.name} role to a user {user.name}'.format(role.name))
    await client.delete_message(ctx.message)
    await asyncio.sleep(5)
    await client.delete_message(text)

@client.command(pass_context=True)
@commands.has_permissions(ban_members=True, kick_members=True)
async def giverole(ctx, user: discord.Member = None, *, name = None):
    author = ctx.message.author
    role = discord.utils.get(ctx.message.server.roles, name=name)
    await client.add_roles(user, role)
    text = await client.say(f'{author.mention} I have added the {role.name} role to a user {user.name}'.format(role.name))
    await client.delete_message(ctx.message)
    await asyncio.sleep(5)
    await client.delete_message(text)
	
client.loop.create_task(change_status())
client.run(os.environ['BOT_TOKEN'])
