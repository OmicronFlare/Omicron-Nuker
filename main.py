# THIS WAS FULLY MADE BY omicron.nn IN DISCORD | ALL CREDITS TO HIM

import os
import discord
import ctypes
import asyncio
import concurrent.futures
from colorama import *
from pystyle import *
from colorama import Fore
import time as t
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor, as_completed


def clear():
    os.system("cls" if os.name=="nt" else "clear")

def title(title: str):
   ctypes.windll.kernel32.SetConsoleTitleW(title)


intro = """

 ▒█████   ███▄ ▄███▓  ██▓  ▄████▄  ██▀███   ▒█████   ███▄    █ 
▒██▒  ██▒▓██▒▀█▀ ██▒▒▓██▒ ▒██▀ ▀█ ▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ 
▒██░  ██▒▓██    ▓██░▒▒██▒ ▒▓█    ▄▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒
▒██   ██░▒██    ▒██ ░░██░▒▒▓▓▄ ▄██▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒
░ ████▓▒░▒██▒   ░██▒░░██░░▒ ▓███▀ ░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░
░ ▒░▒░▒░ ░ ▒░   ░  ░ ░▓  ░░ ░▒ ▒  ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
  ░ ▒ ▒░ ░  ░      ░░ ▒ ░   ░  ▒    ░▒ ░ ▒   ░ ▒ ▒░ ░ ░░   ░ ▒░
░ ░ ░ ▒  ░      ░   ░ ▒ ░ ░         ░░   ░ ░ ░ ░ ▒     ░   ░ ░ 
    ░ ░         ░     ░   ░ ░        ░         ░ ░           ░ 
                 ╭───────────────────────────────╮
                 │          Press Enter          │
                 ╰───────────────────────────────╯


"""
Anime.Fade(Center.Center(intro), Colors.green_to_cyan, Colorate.Diagonal, interval=0.025, enter=True)


mainlogo = """
╭────────────────────────────────────────────────────────────────╮
│                     Omicron Nuker Commands                     │
│                           prefix : -                           │
│                           omicron.nn                           │
╰────────────────────────────────────────────────────────────────╯
"""

commandos = """

╔══════════════════════════════════════════════════════════════╗
║ cdelete                 | Delete all channels                ║
║ ccreate <name> <amount> | Create Channels                    ║
║ spam <message> <amount> | Sends message to all channels      ║
║ croles <name> <amonunt> | Create roles                       ║
║ delroles                | Delete all roles                   ║
╚══════════════════════════════════════════════════════════════╝

"""

token = Write.Input(" Token > ", Colors.green_to_cyan)
prefix = "-"
intents = discord.Intents.all()
omicron = commands.Bot(command_prefix={prefix}, intents=intents)

@omicron.event
async def on_ready():
   print(f"{omicron.user.id} Connected")
   os.system("cls")
   print(Colorate.Diagonal(Colors.green_to_blue, Center.XCenter(mainlogo)))
   print(Colorate.Diagonal(Colors.green_to_blue, Center.XCenter(commandos)))
   print(Colorate.Diagonal(Colors.green_to_blue, Center.XCenter(f"{omicron.user.display_name} Connected")))


async def delete_channel(channel):
    try:
        await channel.delete()
    except Exception as e:
        print(f'Failed to delete channel {channel.name}: {e}')

@omicron.command()
@commands.has_permissions(manage_channels=True)
async def cdelete(ctx):
    guild = ctx.guild
    channels = guild.channels

    # Create a list of tasks to delete channels concurrently
    tasks = [delete_channel(channel) for channel in channels]
    
    # Await all tasks
    await asyncio.gather(*tasks)

    # Create a new channel after all deletions
    new_channel = await guild.create_text_channel('omicron-nuked')

@cdelete.error
async def cdelete_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print(f"{Fore.LIGHTRED_EX} Bot without permissions.")

#######################################################################################

async def create_channel(guild, name, index):
    channel_name = f"{name}"  # Append a number to the channel name for uniqueness
    try:
        await guild.create_text_channel(channel_name)
    except Exception as e:
        print(f' {Fore.LIGHTRED_EX}Failed to create channel {channel_name}: {e}')

@omicron.command()
@commands.has_permissions(manage_channels=True)  # Ensure the user has permission to manage channels
async def ccreate(ctx, name: str, amount: int):
    if amount <= 0:
        print(f" {Fore.LIGHTRED_EX}Provide positive number.")
        return

    # Create channels using asyncio.gather
    tasks = [create_channel(ctx.guild, name, i) for i in range(amount)]
    await asyncio.gather(*tasks)

    print(f" {Fore.LIGHTGREEN_EX} Created {amount} channels.")

@ccreate.error
async def ccreate_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print(f" {Fore.LIGHTRED_EX} No permissions.")
    elif isinstance(error, commands.BadArgument):
        print(f" {Fore.LIGHTRED_EX} Provide valid number")

#######################################################################################

def send_message(channel, message):
    """Sends a message to the specified channel."""
    asyncio.run_coroutine_threadsafe(channel.send(message), omicron.loop)

@omicron.command()
@commands.has_permissions(send_messages=True)  # Ensure the user has permission to send messages
async def spam(ctx, message: str, amount: int):
    """Sends a specified message a certain number of times in all text channels."""
    if amount <= 0:
        print(f' {Fore.LIGHTRED_EX}Please specify a positive number of messages to send.')
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for channel in ctx.guild.text_channels:
            tasks = [executor.submit(send_message, channel, message) for _ in range(amount)]
            for task in concurrent.futures.as_completed(tasks):
                task.result()  # This will raise any exceptions that occurred

    print(f' {Fore.LIGHTGREEN_EX}Sent the message "{message}" {amount} times in all text channels.')
    t.sleep(10)
    os.system("cls")

@spam.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print(f' {Fore.LIGHTRED_EX}You do not have permission to send messages.')
        t.sleep(10)
        os.system("cls")
    elif isinstance(error, commands.BadArgument):
        print(f' {Fore.LIGHTRED_EX}Please provide a valid number for the amount of messages to send.')


#######################################################################################

async def create_role(guild, role_name):
    """Function to create a role in an async context."""
    try:
        role = await guild.create_role(name=role_name)
        return role, None  # Return the role and no error
    except discord.Forbidden:
        return None, "I do not have permission to create roles."
    except discord.HTTPException as e:
        return None, f"Failed to create role {role_name}: {e}"

@omicron.command()
@commands.has_permissions(manage_roles=True)  # Ensure the user has permission to manage roles
async def croles(ctx, name: str, amount: int):
    """Creates roles with the specified name and amount."""
    if amount <= 0:
        print(Fore.LIGHTRED_EX + "Amount must be greater than 0.")
        return

    created_roles = []

    for i in range(amount):
        role_name = f"{name}"  # Create unique role names
        result, error_message = await create_role(ctx.guild, role_name)  # Await role creation directly
        if error_message:
            print(Fore.LIGHTRED_EX + error_message)
        else:
            created_roles.append(result)

    print(Fore.LIGHTGREEN_EX + f"Successfully created {len(created_roles)} roles.")

@croles.error
async def croles_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        print(Fore.LIGHTRED_EX + "You do not have permission to use this command.")
    elif isinstance(error, commands.BadArgument):
        print(Fore.LIGHTRED_EX + "Please provide a valid number for the amount.")
    else:
        print(Fore.LIGHTRED_EX + f"An error occurred: {error}")

omicron.run(token)
