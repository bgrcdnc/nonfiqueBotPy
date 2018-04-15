import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random

def token():
	tokfile=open("token","r")
	return tokfile.read()

PREFIX = ">"

client = Bot(description="Just a bot by nonfique#1781", command_prefix=PREFIX, pm_help = True)

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

@client.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await client.say(random.choice(choices))

@client.command(help="pong", description="pong")
async def ping(*args):
	await client.say(":ping_pong: Pong!")

@client.command(help="Says 'tamam'", description="Says 'tamam'", pass_context=True)
async def tamam(ctx, *args):
	await client.delete_message(ctx.message)
	await client.say("tamam")

@client.command(help = "Shows userid of the tagged user (see '" + PREFIX + "help userid' for usage)", description = PREFIX + "userid <user> | Shows userid of the tagged user")
async def userid(*args):
	if not args[0].startswith('<@!'):
		return
	userid = args[0]
	await client.say(userid[3:-1])

@client.command(help = "TODO afk command", description = PREFIX + "afk | will eventually be afk command")
async def afk(*args):
	await client.say("SOON :tm:")


@client.command(help = "Deletes messages. (see '" + PREFIX + "help sil' for usage)", description = PREFIX + "sil <(int)number of messages> <user=None> | Deletes messages according to given arguments", pass_context=True)
async def sil(ctx, *args):
	WAIT_TIME = 2
	msgorg = ctx.message
	channel = msgorg.channel
	msgs = [msgorg]
	nom = 0
	nom_e = False
	user = None
	if len(args) == 1:
		try:
			nom = int(args[0])
		except ValueError:
			nom_e = True
	elif len(args) == 2:
		try:
			nom = int(args[0])
		except ValueError:
			nom_e = True
		user = args[1]
		user = user[3:-1]
	if nom < 1 or nom_e == True:
		await client.delete_message(msgorg)
		msgout = await client.say('**>** **Error#1:** Number of messages to be deleted needs to be specified in the first argument as an *integer*')
		await asyncio.sleep(WAIT_TIME)
		await client.delete_message(msgout)
		return
	elif nom > 25:
		nom = 25
	counter = 0
	async for msg in client.logs_from(channel, limit=25, before=msgorg):
		if msg.author == client.user and msg.content.startswith('**>**'):
			continue
		if user is not None:
			if type(user) is str:
				if msg.author.id == user:
					user = msg.author
					msgs.append(msg)
					counter+=1
			else:
				if msg.author == user:
					msgs.append(msg)
					counter+=1
		else:
			msgs.append(msg)
			counter+=1
		if(counter >= nom):
			break
	try:
		await client.delete_messages(msgs)
	except discord.errors.ClientException:
		pass
	if counter > 0:
		output = '**>** **Success:** Deleted ' + str(counter) + ' messages'
		if user is not None:
			output += ' from **' + user.nick + '**'
	else:
		output = '**>** **Error#2:** Could not find any message to delete'
		await client.delete_message(msgorg)
	msgout = await client.say(output)
	await asyncio.sleep(WAIT_TIME)
	await client.delete_message(msgout)

@client.command(help="test, really", description="test, really", pass_context=True)
async def test(ctx, *args):
	await client.say("Testing...")
	
client.run(token())