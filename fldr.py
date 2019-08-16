################################################################################################################
# S T A R T ####################################################################################################
################################################################################################################
#page.start


import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import User
import json
import socket
import ast
import random
import urllib.request
import re
import asyncio
import datetime
import string
import os
import typing


################################################################################################################
# C O N F I G S ################################################################################################
################################################################################################################
#page.configs


ConfigLocation = './ignore/config.json' # Specify config.json location
r=open(ConfigLocation,"r") # Open the config file
data=json.load(r) # Turn it into a dictionary (Python JSON)
ConfigJSON=list(data.values()) # Turn JSON into list
PREFIX=ConfigJSON[0] # Prefix
TOKEN=ConfigJSON[1] # Bot token
GAME=ConfigJSON[2] # Previous set game - It's stored so that on bot restart it sets its game automatically

FilterLocation = './ignore/filter.txt' # Specify location of fitler.txt
with open(FilterLocation, "r") as fil:
    fil=fil.read()
    filter=fil.split("\n") # Take every newline and add it to an array
    try:
        filter.remove('') # Using try/except to avoid crashes caused by '' or ' ' not existing
    except Exception:
        pass

    try:
        filter.remove(' ')
    except Exception:
        pass


################################################################################################################
# D I S C O R D P Y ############################################################################################
################################################################################################################
#page.discordpy


client = commands.Bot(command_prefix=PREFIX, case_insensitive=True)
client.remove_command('help') # Discordpy comes with default help command so we scrap that to use our own.


################################################################################################################
# C O N S T A N T S ############################################################################################
################################################################################################################
#page.constants


burntID = 246297096595046401 # Burnt
teoID = 425762097503141898 # Teo
ptinosqID = 313021770321887233 # Burnt alt
bananaID = 135169858689171456 # Banana
BotStuffChannel = 611665344079200344 # THIS IS THE DEV SERVER CHANNEL
upvoteEmoji = '⬆️'
downvoteEmoji = '⬇️'
toolsEmoji = ":tools:"
successEmoji = ":white_check_mark:"
failEmoji = ":no_entry:"
bookEmoji = ":book:"
warningEmoji = ":name_badge: "


################################################################################################################
# H O S T N A M E ##############################################################################################
################################################################################################################
#page.hostname


BOTPC = "UNKNOWN PC" # Default
if socket.gethostname() == 'EC2AMAZ-96PQUE8':
    BOTPC = "Amazon Web Server" #AWS - Main bot is hosted here
elif socket.gethostname() == 'DESKTOP-8M1K2G7':
    BOTPC = "Burnt's laptop"
elif socket.gethostname()== 'DESKTOP-F34TDET':
    BOTPC = "Burnt's RTX Workstation - Big fleks"
elif socket.gethostname()== 'DESKTOP-6AT5I43':
    BOTPC = "Max's laptop"
else:
    BOTPC= socket.gethostname()

"""Add your own PC by doing:

elif socket.gethostname()== 'yourpcname':
    BOTPC = "X's computer"

open cmd, type `py` and then do this:
import socket
print(socket.gethostname())
>>OUTPUTS THE NAME

Copy paste that output into the elif and add it under the last elif.
"""


################################################################################################################
# E V E N T S ##################################################################################################
################################################################################################################
#page.events


@client.event
async def on_message(message):

    """
    There is not ctx with most events.
    message.content turns it into a readable string.

    Example:
    await message.channel.send("message.content")
    This will just repeat whatever the user says.
    """

    await client.process_commands(message) # ALWAYS PUT THIS AFTER ON_MESSAGE OR IT WON'T PROCESS ANY COMMANDS.

@client.event
async def on_ready():

    await client.change_presence(activity=discord.Game(name=GAME)) # Set game to whatever is in JSON file.
    ch = client.get_channel(BotStuffChannel) # Get channel from channel ID
    await ch.send(f"Deployed on \n```{str(datetime.datetime.now())}```\n\nServer: {BOTPC}") # Send the time deployed and the PC
    print('We have logged in as {0.user}'.format(client)) # Print info to console

@client.event
async def on_command_completion(ctx): # Discordpy builtin that detects commands being run https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.on_command_completion

    try: # Catches errors
        with open("commandCount.txt", "r+") as txtFile:
            value = txtFile.read() # Read whatever is in txt
            if value.isdigit() != True: # If it's empty or a word e.g None , make it 0
                value = 0
            NewValue = int(value)+1

        with open("commandCount.txt", "w") as txtFile2:
            txtFile2.write(str(NewValue))

        return True

    except Exception as e:
        print(f"Error with EVENT on_command_completion - {e}")

        return False


################################################################################################################
# C O M M A N D S ##############################################################################################
################################################################################################################
#page.commands


@client.command()
async def ping(ctx):
    """
    Tinos 13/08/2019

    Returns with bot ping in ms

    """

    await ctx.message.channel.send(f'Pong: {int(round(client.latency, 3) * 1000)} ms')


@client.command(aliases=["kiss"])
async def smooch(ctx, member: typing.Union[discord.Member, int, str] = None):
    """
    Max 15/08/2019

    Mentioning a member will cause bot to respond with @command_author gave @mentioned_user a smooch! How romantic!

    """

    Sender = ctx.message.author.mention
    await ctx.message.channel.send(f"{Sender} gave {member.mention} a smooch! How romantic!")


@client.command(aliases=["stats"])
async def statistics(ctx):
    """
    Max 15/08/2019

    Returns number of times a command has been used.

    """

    with open("commandCount.txt", "r+") as txtFile:
        value = txtFile.read()
    await ctx.message.channel.send(f"This bot has run {value} commands!")


@client.command(name="8ball")
async def _ball(ctx, question = None):
    """
    Max 15/08/2019

    Generates random reply stored in array questionResponses. Only accepts one or more args.

    """

    noArgsResponses = [
        "Hey! Give me something to work with here!",
        "Stop wasting my time, I'm a busy bot!",
        "Please, input a question, I beg of you."
    ]

    if question == None:
        await ctx.message.channel.send(f"{random.choice(noArgsResponses)}")

    else:
        questionResponses = [
            "I'd say so.",
            "Absolutely.",
            "No doubt in my mind.",
            "It depends on what you feel in your heart!",
            "Not sure, what do you think I am? A magic 8 ball?",
            "Ask me again when I get a work ethic.",
            "Dear gosh no, never.",
            "I wouldn't advise it.",
            "I'd say no, but ask BananaFalls."
        ]
        await ctx.message.channel.send(f"{random.choice(questionResponses)}")

@client.command(aliases=["game","setgame"])
async def play(ctx,*, ProvidedGame=None):
    """
    Burnt 13/08/2019

    Sets bot's playing status to provided argument(s)

    """

    if await check_if_moderator(ctx):
        try:
            if ProvidedGame==None:
                raise "No game provided" # If no command is given, just break the damn thing before it does more damage.

            await client.change_presence(activity=discord.Game(name=ProvidedGame))
            with open(ConfigLocation, 'r') as file:
                 json_data = json.load(file)
                 json_data["game"] = ProvidedGame

            with open(ConfigLocation, 'w') as file:
                json.dump(json_data, file, indent=2)

            await ctx.message.channel.send(f"Now playing {ProvidedGame}")

        except Exception as e:
            print(f"Error with COMMAND play -  {e}")
            await ctx.message.channel.send(f"Usage:\n`{PREFIX}play GAME HERE`")

    else:
        await ctx.message.channel.send("This command is only available to moderators.")

@client.command()
async def hello(ctx):
    """
    Burnt 13/08/2019

    Very simple command that just makes bot respond with Hello!

    """

    await ctx.message.channel.send("Hello!")


@client.command(aliases=["eval","e"])
async def evaluate(ctx, *, cmd):
    if await check_if_dev(ctx):
        f"""
        Burnt 13/08/2019

        Evaluate provided code

        Usage:
        -evaluate ```py
        #code here
        ```

        DO NOT TOUCH DO NOT TOUCH DO NOT TOUCH
        """
        try:
            fn_name = "_eval_expr"

            cmd = cmd.strip("` ")
            cmd = cmd.strip("py")

            # add a layer of indentation
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n{cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
        except Exception as uwuowo:
            await ctx.message.channel.send(uwuowo)
    else:
        await ctx.message.channel.send("This command is made only accessible to the bot developers.")


################################################################################################################
# F U N C T I O N S ############################################################################################
################################################################################################################
#page.functions


def insert_returns(body):
    """
    Burnt 13/08/2019

    Provides functionality to evaluated code

    DO NOT TOUCH DO NOT TOUCH DO NOT TOUCH
    """

    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

async def check_if_moderator(ctx):
    """
    Burnt 13/08/2019

    Checks if provided ctx author has roles called moderators or server management

    Usage: if await check_if_moderator(ctx):

    """

    ismod=False
    for role in ctx.message.author.roles:
        if role.name.lower() == "moderators":
            ismod=True

        elif role.name.lower() == "server management":
            ismod=True

    return ismod

async def check_if_dev(ctx):
    """
    Burnt 13/08/2019

    Checks if provided ctx author has roles called moderators or server management

    Usage: if await check_if_dev(ctx):

    """

    if ctx.message.author.id == burntID or ctx.message.author.id == ptinosqID or ctx.message.author.id == bananaID or ctx.message.author.id == teoID:
        return True

    else:
        return False


################################################################################################################
# E N D ########################################################################################################
################################################################################################################
#page.end

client.run(TOKEN)# THIS MUST ALWAYS BE THE ON THE LAST LINE

"""
INFO

Every section of the bot code is split using
##############
# N A M E  ###
##############
#examplehere

The examplehere is so that you can easily navigate to that section. Just do ctrl+f and type:
page.

This'll cycle you through all the sections so when the bot ends up having 1k+ lines of code, it's easy to go from start to functions

Please keep commands under the commands section etc.

Let people know when you're importing something new since we might need to install it with pip

USEFUL SHIT TO COPY PASTE

await ctx.message.channel.send("message here")

--------------------

@client.command()
async def command(ctx):

async def example(ctx, member: typing.Union[discord.Member, int, str] = None): # Takes discord member argument as user ID, @mention or username#1234

ctx.message.author.mention # Mention the command author

example = client.get_channel(idHere) # Get channel using an ID

Using three quotation marks allows you to multi line comment or multi line string. Just assign it to a variable.
"""
