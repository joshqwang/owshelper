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
    global all_stories
    if message.author == client.user:
      return
    guild = message.guild.name
    game = all_stories[guild]
    cur_channel = message.channel.name
    command = message.content.lower()

    if command == 'ows help':
        temp_message = 'Available commands:\n help - displays this menu\n start - starts a story\n current - displays the current story\n end - ends any current stories'
        await message.channel.send(temp_message)

    elif command == 'ows start':
      if guild in all_stories:
          del game
      game = Story()
      await start_game(game,message)

    elif command == 'ows current':
      if not guild in all_stories:
        await message.channel.send('There is not an ongoing story right now!')
      else:
        await disp_current(game, message)

    elif command == 'ows end':
      if not guild in all_stories:
        await message.channel.send('There is not an ongoing story right now!')
      else:
        await end_game(game, message)

    elif command[:3] == 'ows':
        await message.channel.send('Sorry, I didn\'t recognize that command. Try ows help for a list of commands.')

    elif guild in all_stories and cur_channel == game.channel:
        await add_to_story(game, message)

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
async def end_game(game, message):
      
      if game.story == '':
        await message.channel.send('Ended the story.')
        
      else:
        contributors_items = list((game.contributors).items())
        contributors_items.sort(key = lambda x : x[1], reverse = True)
        contributors_message = ''
        for key in contributors_items:
          contributors_message += key[0] + " - " + str(key[1]) + " contributions \n"
        await message.channel.send('Your story is: ' + game.story +  '\n\nThe top contributors in this story were:\n' + contributors_message)
      del game
async def add_to_story(game,message):
     game.story += ' ' + message.content
     if message.author.display_name in (game.contributors):
      game.contributors[message.author.display_name] += 1
     else:
      game.contributors[message.author.display_name] = 1
      await message.add_reaction('\N{THUMBS UP SIGN}')
client.run(TOKEN)
