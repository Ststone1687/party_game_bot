import discord
intents = discord.Intents.default()
intents.members = True
from discord.ext import commands
bot = commands.Bot(command_prefix='!',intents=intents)
from discord.utils import get
import json
import random
import time
import sys
import os
import asyncio
import math
import datetime

@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print(bot.user.id)
  print('------')

@bot.command()
async def load(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.load_extension(F'cmds.{File}')
  await message.channel.send("load成功")


@bot.command()
async def unload(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.unload_extension(F'cmds.{File}')
  await message.channel.send("unload成功")


@bot.command()
async def reload(message, File):
  if(message.author.id != 550907252970749952):
    return
  bot.reload_extension(F'cmds.{File}')
  await message.channel.send("reload成功")

for Filename in os.listdir("./cmds"):
	if Filename.endswith(".py"):
		bot.load_extension(F'cmds.{Filename[:-3]}')


bot.run("OTk3ODAzNjA0NjQxNTk5NDk4.Gzz2-F.BFw6OF6GcNW_CkrA5GvCkmVswTe3GG6XdSps9I")