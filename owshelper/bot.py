# bot.py
import os

import discord

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

contributors = {}

all_stories = {}
#{guild_name: (story, ongoing, channel, contributors)}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global all_stories
    global current_channel
    global contributors
    if message.author == client.user:
      return
    if not message.guild.name in all_stories:
          all_stories[message.guild.name] = ('', False,'', {})
    if message.content == 'ows start':
      
      if all_stories[message.guild.name][2] != '':
          await message.channel.send('Ending a story in other channel!')

      all_stories[message.guild.name] = ('', True, message.channel.name, {})
      await message.channel.send('Starting a story!')
    elif message.content == 'ows current':
     if all_stories[message.guild.name][1] == False:
        await message.channel.send('There is not an ongoing story right now!')
     elif all_stories[message.guild.name][0] == '':
        await message.channel.send('The current story is empty.')
     else:
        await message.channel.send('Your current story is: ' + all_stories[message.guild.name][0])

     

    elif message.content == 'ows end':
      if all_stories[message.guild.name][1] == False:
        await message.channel.send('There is not an ongoing story right now!')
      elif all_stories[message.guild.name][0] == '':
        await message.channel.send('Ended the story.')
      else:
        contributors_items = list(all_stories[message.guild.name][3].items())
        contributors_items.sort(key = lambda x : x[1], reverse = True)
        contributors_message = ''
        for key in contributors_items:
          contributors_message += key[0] + " - " + str(key[1]) + " contributions \n"
        await message.channel.send('Your story is: ' + all_stories[message.guild.name][0] +  '\n\nThe top contributors in this story were:\n' + contributors_message)

      all_stories[message.guild.name] = ('', False, '', {})

    elif all_stories[message.guild.name][1] == True and message.channel.name == all_stories[message.guild.name][2]:
      all_stories[message.guild.name] = (all_stories[message.guild.name][0] + message.content + ' ', all_stories[message.guild.name][1], all_stories[message.guild.name][2], all_stories[message.guild.name][3])
      if message.author.display_name in all_stories[message.guild.name][3]:
        temp_dict = all_stories[message.guild.name][3]
        temp_dict[message.author.display_name] += 1
        all_stories[message.guild.name] = (all_stories[message.guild.name][0], all_stories[message.guild.name][1], all_stories[message.guild.name][2], temp_dict)
      else:
        temp_dict = all_stories[message.guild.name][3]
        temp_dict[message.author.display_name] = 1
        all_stories[message.guild.name] = (all_stories[message.guild.name][0], all_stories[message.guild.name][1], all_stories[message.guild.name][2], temp_dict)
      await message.add_reaction('\N{THUMBS UP SIGN}')


client.run(TOKEN)
