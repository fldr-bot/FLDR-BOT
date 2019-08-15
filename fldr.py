filter=["faggot","nigger","fag","dyke","nigga","nibba","pornhub","redtube","xnxx","secretwordnooneknows"] # This is the filter - add any naughty words here, keep a testing word to test filter.
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
ConfigLocation = 'config.json' # Specify config.json location
r=open(ConfigLocation,"r") # open it
data=json.load(r) # turn it into json
ConfigJSON=list(data.values()) # turn json into list
PREFIX=ConfigJSON[0] #prefix
TOKEN=ConfigJSON[1] # bot token
GAME=ConfigJSON[2] # previous set game - It's stored so that on bot restart it sets it's game automatically
client = commands.Bot(command_prefix=PREFIX, case_insensitive=True)
client.remove_command('help') # Discordpy comes with default help command so we scrap that to use our own.

#Constants for ease of use further into the code
burntID = 246297096595046401 # burnt
teoID = 425762097503141898 # teo
ptinosqID = 313021770321887233 # burnt alt
bananaID = 135169858689171456 # banana
BotStuffChannel = 611665344079200344 # THIS IS THE DEV SERVER CHANNEL



#More constants for ease of use in code
upvoteEmoji = '⬆️'
downvoteEmoji = '⬇️'
toolsEmoji = ":tools:"
successEmoji = ":white_check_mark:"
failEmoji = ":no_entry:"
bookEmoji = ":book:"
warningEmoji = ":name_badge: "

#This basically logs where the bot is being run.
BOTPC = "UNKNOWN PC" # Default
if socket.gethostname() == 'EC2AMAZ-96PQUE8':
    BOTPC = "Amazon Web Server"
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

@client.event
async def on_message(message):
    #Do Stuff - THERE IS NO CTX WITH EVENTS.
    #message.content turns it into a readable string.

    """
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
async def on_command_completion(ctx): # discordpy builtin that detects commands being run https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.on_command_completion
    try:
        print(f"Ran command: {ctx.command.name}")
        with open("commandCount.txt", "r+") as txtFile: # r+ means read + other features
            value = txtFile.read() # read whatever is in there
            print(f"{value} - current value") # debugging
            if value.isdigit() != True: # if it's empty or a word e.g None
                value = 0
            NewValue = int(value)+1
        with open("commandCount.txt", "w") as txtFile2: # using w cos I don't wanna risk appending
            txtFile2.write(str(NewValue)) # over writes with +1
            print(f"{NewValue} - New value") # debugging
        return True
    except Exception as e:
        print(f"Error with txt Manager - {e}")
        return False

        #copy pasted from function, if this works we won't need the function any more.





#events will always go to top just to keep our stuff neat
#layout is functions (not cmds), events, cmds


async def check_if_moderator(ctx):
    #if await check_if_moderator(ctx): #use this for if statements.
    ismod=False # Default - will change if user is actually a mod.
    for role in ctx.message.author.roles:
        if role.name.lower() == "moderators": # Must be in lowercase!
            ismod=True
        elif role.name.lower() == "server management":
            ismod=True
    return ismod

async def check_if_dev(ctx): # Use this for commands that only we should have access to.
    #if await check_if_dev(ctx):
    if ctx.message.author.id == burntID or ctx.message.author.id == ptinosqID or ctx.message.author.id == bananaID or ctx.message.author.id == teoID: # If user ID is equal to one of ours.
        return True
    else:
        return False

@client.command()
async def ping(ctx):
    await ctx.message.channel.send(f'Pong: {int(round(client.latency, 3) * 1000)} ms') # This was copy pasted from StackOverflow I have no clue what it means or does.


@client.command(aliases=["kiss"])
async def smooch(ctx, member: typing.Union[discord.Member, int, str] = None):
    """
    By Max

    example: -smooch @user // -smooch userID // -smooch user#1234
    """
    Sender = ctx.message.author.mention

    await ctx.message.channel.send(f"{Sender} gave {member.mention} a smooch! How romantic!")


"""async def txt_management(ctx, command_name):
    #if await txt_management(ctx):
    try:
        with open("commandCount.txt", "r+") as txtFile: # r+ means read + other features
            value = txtFile.read() # read whatever is in there
            print(f"{value} - current value") # debugging
            if value.isdigit() != True: # if it's empty or a word e.g None
                value = 0
            NewValue = int(value)+1
        with open("commandCount.txt", "w") as txtFile2: # using w cos I don't wanna risk appending
            txtFile2.write(str(NewValue)) # over writes with +1
            print(f"{NewValue} - New value") # debugging
        return True
    except Exception as e:
        print(f"Error with txt Manager - {e}")
        return False

"""
@client.command(aliases=["stats"])
async def statistics(ctx):

    with open("commandCount.txt", "r+") as txtFile: # r+ means read + other features
        value = txtFile.read() # read whatever is in there

    await ctx.message.channel.send(f"This bot has run {value} commands!")



@client.command(name="8ball")
async def _ball(ctx, question = None):

    """
    By Max

    example: -8ball [question]
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

@client.command(aliases=["game"])
async def play(ctx,*, gamer=None):
    if await check_if_moderator(ctx): # Mod only command!
        try:
            if gamer==None:
                raise "err" # If no command is given, just break the damn thing before it does more damage.
            await client.change_presence(activity=discord.Game(name=gamer)) # set the game
            with open(ConfigLocation, 'r') as file: # Stores it into the config file
                 json_data = json.load(file)
                 json_data["game"] = gamer
            with open(ConfigLocation, 'w') as file:
                json.dump(json_data, file, indent=2)
            await ctx.message.channel.send(f"Now playing {gamer}")
        except Exception as e:
            print(f"Error with play {e}") # If it errors, it'll just print the error to console
            await ctx.message.channel.send(f"Usage:\n`{PREFIX}play GAME HERE`") # and show the user the correct usage
    else:
        await ctx.message.channel.send("This is a mod only command, sorry.")

@client.command()
async def hello(ctx):
    await ctx.message.channel.send("Hello!")

#EVALUATION CODE - IGNORE ALL OF THIS
def insert_returns(body):
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
@client.command()
async def evaluate(ctx, *, cmd):
    if await check_if_burnt(ctx):
        """
        -evaluate ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```

        remember the space between eavluate and ```
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
        await ctx.message.channel.send("This command is made only accessible to Burnt.")
#EVALUATION CODE END - OK YOU CAN STOP IGNORING

client.run(TOKEN)# THIS MUST ALWAYS BE THE ON THE LAST LINE

"""
USEFUL SHIT TO COPY PASTE

await ctx.message.channel.send("message here")

--------------------

@client.command()
async def command(ctx):

async def example(ctx, member: typing.Union[discord.Member, int, str] = None): # Takes discord member arguement as user ID, @mention or username#1234

ctx.message.author.mention # Mention the command author

example = client.get_channel(idHere) # Get channel using an ID

using three quotation marks allows you to multi line comment or multi line string. Just assign it to a variable.
"""
