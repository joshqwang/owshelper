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
    cur_channel = message.channel.name
    command = message.content.lower()
    if "who asked" in command:
        if message.author.id == 415981659297677347:
            await message.channel.send("No one fucking asked but im a human being ")
            await message.channel.send("with an opinion and evidence to back it up, and ")
            await message.channel.send("the soldiers of the revolutionary war and the civil war and the world wars all fought ")
            await message.channel.send("so that I had the right to free speech and thus the right to state "
            await message.channel.send("that opinion and the evidence I have even when no one fucking asked."
            await message.channel.send("And I know what you're going to say right after I finish sending this hammer of logic straight to your senses,"
            await message.channel.send("you miserable little fucktwat, you're going to say \"who tf asked?\" ")
            await message.channel.send("like you've reached the pinnacle of comedy. I would call you a fucking clown"
            await message.channel.send("but clowns are either funny or scary and you're neither and you'll never be either in the eyes of anyone.")
            await message.channel.send("And despite all that you might say")
            await message.channel.send("and despite your constant regurgitation of the overused sassy 'comeback'")
            await message.channel.send("you will not amount to anything and you disgrace the ancestors of your lineage ")
            await message.channel.send("who fought hard so that you and I can stand here and say whatever we like without no one fucking asking.")
            await message.channel.send("Shut the fuck up and go back to the storm drain where your mother abandoned you. ")
            await message.channel.send("Because she didn't 'ask' for a disrespectful midgetwit to be the next in her family tree. ")
            await message.channel.send("So for her sake and your ancestors' sake and for my sake don't ever fucking again sarcastically ask \"who tf asked\". ")
            await message.channel.send("Because guess what fucker, no one asked for you to say that, and unlike me, no one respects you. So stfu.")
    if guild in all_stories:
        game = all_stories[guild]

    if command == 'ows help':
        temp_message = 'Available commands:\n help - displays this menu\n start - starts a story\n current - displays the current story\n end - ends any current stories'
        await message.channel.send(temp_message)

    elif command == 'ows start':
      if guild in all_stories:
          del all_stories[guild]
      all_stories[guild] = Story()
      game = all_stories[guild]
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
      del all_stories[guild]

    elif command[:3] == 'ows':
        await message.channel.send('Sorry, I didn\'t recognize that command. Try ows help for a list of commands.')

    elif guild in all_stories:
        if cur_channel == game.channel:
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
async def add_to_story(game,message):
     game.story += ' ' + message.content
     if message.author.display_name in (game.contributors):
       game.contributors[message.author.display_name] += 1
     else:
       game.contributors[message.author.display_name] = 1
     await message.add_reaction('\N{THUMBS UP SIGN}')
client.run(TOKEN)
