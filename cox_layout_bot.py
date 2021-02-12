# cox_layout_bot.py
import discord
import os
import pathlib
import re
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

re_3c2p = re.compile(r'^([tvgysmne]{3})\s(fscc|scpf|scsp|sfcc)$', re.IGNORECASE)
re_4c1p = re.compile(r'^([tvgysmne]{4})\s(scpf|sccf)$', re.IGNORECASE)

dict_boss = {
	't': 'tekton',
	'v': 'vasa',
	'g': 'guardians',
	'y': 'mystics',
	's': 'shamans',
	'm': 'muttadiles',
	'n': 'vanguards',
	'e': 'vespula'
}

dict_3c2p_rooms = {
	'fscc': 'fsccs pcpsf',
	'scpf': 'scpfc cspsf',
	'scsp': 'scspf ccspf',
	'sfcc': 'sfccs pcpsf',
}

dict_4c1p_rooms = {
	'scpf': 'scpfc ccssf',
	'sccf': 'sccfc pscsf',
}

no_special_characteristics = 'There is nothing special about this rotation'
no_zgs_needed = 'You do not need to bring a ZGS for Muttadile'
vespula_good_entry = 'Enter vespula using the CM tile'
vespula_bad_entry = 'Enter vespula using the tile two further than the CM tile'
cm_tekton = 'You have CM Tekton'
boulder = 'You have a chance to redemption the final boulder'

room_layouts_dir = pathlib.Path(r'room_layouts')


@bot.event
async def on_ready():
	guild = discord.utils.get(bot.guilds, name=GUILD)
	# guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
	print(f'{bot.user.name} has connected to {guild.name} {guild.id}!')


@bot.command(name='rot',
             help='''
             BOSS           SHORT CODE
             Tekton         t
             Vasa           v
             Guardians      g
             Mystics        y
             Shamans        s
             Muttadiles     m
             Vanguards      n
             Vespula        e
             
             ROOMS          ROOM CODE
             fsccs pcpsf    fscc
             scpfc cspsf    scpf
             scspf ccspf    scsp
             sfccs pcpsf    sfcc
             
             examples:
             !rot tmg sfcc
             !rot ytmg scpf
             ''')
async def rot(ctx, bosses, rooms):
	if ctx.message.author == bot.user:
		return

	# text preparation
	bosses = bosses.lower()
	rooms = rooms.lower()
	special = False

	if len(bosses) == 3:    # 3c2p
		boss1, boss2, boss3 = [dict_boss[boss] for boss in bosses]
		rooms_image = room_layouts_dir.joinpath(''.join(['3c2p ', rooms, '.png']))
		await ctx.send(file=discord.File(rooms_image))

		if rooms == 'fscc':
			if 'vespula' in [boss3]:
				await ctx.send(vespula_bad_entry)   # improperly gave a no-zgs-needed message previously
				special = True

			await ctx.send(boulder)
			special = True

		elif rooms == 'scpf':
			if 'muttadiles' in [boss1, boss3]:
				await ctx.send(no_zgs_needed)
				special = True

			if 'vespula' in [boss1]:
				await ctx.send(vespula_bad_entry)
				special = True

			elif 'vespula' in [boss3]:
				await ctx.send(vespula_good_entry)
				special = True

		elif rooms == 'scsp':
			if 'muttadiles' in [boss3]:
				await ctx.send(no_zgs_needed)
				special = True

			if 'vespula' in [boss1, boss3]:
				await ctx.send(vespula_bad_entry)
				special = True

			elif 'vespula' in [boss2]:
				await ctx.send(vespula_good_entry)
				special = True

			await ctx.send(boulder)
			special = True

		elif rooms == 'sfcc':
			if 'muttadiles' in [boss2]:
				await ctx.send(no_zgs_needed)
				special = True

			if 'tekton' in [boss1]:
				await ctx.send(cm_tekton)
				special = True

			if 'vespula' in [boss2]:
				await ctx.send(vespula_bad_entry)

			elif 'vespula' in [boss3]:
				await ctx.send(vespula_good_entry)

			await ctx.send(boulder)
			special = True

	elif len(bosses) == 4:      # 4c1p
		boss1, boss2, boss3, boss4 = [dict_boss[boss] for boss in bosses]
		rooms_image = room_layouts_dir.joinpath(''.join(['4c1p ', rooms, '.png']))
		await ctx.send(file=discord.File(rooms_image))

		if rooms == 'scpf':
			if 'muttadiles' in [boss2, boss3]:
				await ctx.send(no_zgs_needed)
				special = True

			if 'vespula' in [boss2]:
				await ctx.send(vespula_good_entry)
				special = True

			elif 'vespula' in [boss3, boss4]:
				await ctx.send(vespula_bad_entry)
				special = True

			await ctx.send(boulder)
			special = True

		elif rooms == 'sccf':
			if 'muttadiles' in [boss2]:
				await ctx.send(no_zgs_needed)
				special = True

			if 'tekton' in [boss3]:
				await ctx.send(cm_tekton)
				special = True

			if 'vespula' in [boss2]:
				await ctx.send(vespula_good_entry)
				special = True

	else:
		await ctx.send(f'rotation not recognized {ctx.content}')
		special = True

	if not special:
		await ctx.send(no_special_characteristics)


if __name__ == '__main__':
	bot.run(TOKEN)
	bot.change_presence(activity='type !help rot for help', status='type !help rot for help')
