# bot.py
import os

import discord

TOKEN = os.getenv('DISCORD_TOKEN')

class Story:
    def __init__(self):
      self.story = ''
      self.channel = ''
      self.contributors = {}
   

client = discord.Client()
all_stories = {}
#{guild_name: (story, ongoing, channel, contributors)}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
      return

    

    if message.content == 'ows help':
        temp_message = 'Available commands:\n help - displays this menu\n start - starts a story\n current - displays the current story\n end - ends any current stories'
        await message.channel.send(temp_message)

    elif message.content == 'ows start':

      if message.guild.name in all_stories:
          del all_stories[message.guild.name]
      all_stories[message.guild.name] = Story()

      await start_game(all_stories[message.guild.name],message)


    elif message.content == 'ows current':
      if not message.guild.name in all_stories:
        await message.channel.send('There is not an ongoing story right now!')
      else:
        await disp_current(all_stories[message.guild.name], message)

    elif message.content == 'ows end':
      if not message.guild.name in all_stories:
        await message.channel.send('There is not an ongoing story right now!')
      elif all_stories[message.guild.name].story == '':
        await message.channel.send('Ended the story.')
        del all_stories[message.guild.name]
      else:
        contributors_items = list((all_stories[message.guild.name].contributors).items())
        contributors_items.sort(key = lambda x : x[1], reverse = True)
        contributors_message = ''
        for key in contributors_items:
          contributors_message += key[0] + " - " + str(key[1]) + " contributions \n"
        await message.channel.send('Your story is: ' + all_stories[message.guild.name].story +  '\n\nThe top contributors in this story were:\n' + contributors_message)
        del all_stories[message.guild.name]

    elif message.content[:3] == 'ows':
        await message.channel.send('Sorry, I didn\'t recognize that command. Try ows help for a list of commands.')

    elif message.guild.name in all_stories and message.channel.name == all_stories[message.guild.name].channel:
      all_stories[message.guild.name].story += ' ' + message.content
      if message.author.display_name in (all_stories[message.guild.name].contributors):
       all_stories[message.guild.name].contributors[message.author.display_name] += 1
      else:
       all_stories[message.guild.name].contributors[message.author.display_name] = 1
      await message.add_reaction('\N{THUMBS UP SIGN}')

async def start_game(game, message):
    if game.channel != '':
       await message.channel.send('Ending a story in other channel!')

    game.channel = message.channel.name
    await message.channel.send('Starting a story!')
async def disp_current(game, message):
     
     if game.story == '':
        await message.channel.send('The current story is empty.')
     else:
        await message.channel.send('Your current story is: ' + game.story)

client.run(TOKEN)
