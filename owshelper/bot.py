# bot.py
import os

import discord

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

current_story = ''
ongoing_story = False
current_channel = ''

def reset_vars():
    global ongoing_story
    global current_story
    global current_channel
    
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global ongoing_story
    global current_story
    global current_channel
    if message.author == client.user:
      return
    
    if message.content == 'ows start':
      if current_channel != '':
          await message.channel.send('Ending a story in other channel!')

      current_story = ''
      ongoing_story = True
      current_channel = message.channel.name
      await message.channel.send('Starting a story!')
    elif message.content == 'ows current':
     if ongoing_story == False:
        await message.channel.send('There is not an ongoing story right now!')
      elif current_story == '':
        await message.channel.send('The current story is empty.')
      else:
        await message.channel.send('Your current story is: ' + current_story)

     

    elif message.content == 'ows end':
      if ongoing_story == False:
        await message.channel.send('There is not an ongoing story right now!')
      elif current_story == '':
        await message.channel.send('Ended the story.')
      else:
        await message.channel.send('Your story is: ' + current_story)

      current_story = ''
      ongoing_story = False
      current_channel = ''

    elif ongoing_story == True and message.channel.name == current_channel:
      current_story += message.content + ' '
      await message.add_reaction('\N{THUMBS UP SIGN}')

    	

client.run(TOKEN)
