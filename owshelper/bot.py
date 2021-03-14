# bot.py
import os

import discord

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

contributors = {}
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
    global contributors
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
        contributors_items = list(contributors.items())
        contributors_items.sort(key = lambda x : x[1], reverse = True)
        contributors_message = ''
        for key in contributors_items:
          contributors_message += key[0] + " - " + str(key[1]) + " contributions \n"
        await message.channel.send('Your story is: ' + current_story +  '\n\nThe top contributors in this story were:\n' + contributors_message)

      current_story = ''
      ongoing_story = False
      current_channel = ''
      contributors = {}

    elif ongoing_story == True and message.channel.name == current_channel:
      current_story += message.content + ' '
      if message.author.display_name in contributors:
        contributors[message.author.display_name] += 1
      else:
        contributors[message.author.display_name] = 1
      await message.add_reaction('\N{THUMBS UP SIGN}')

    	

client.run(TOKEN)
