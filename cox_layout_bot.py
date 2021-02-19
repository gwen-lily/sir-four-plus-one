# cox_layout_bot.py
import discord
import asyncio
import os
import pathlib
import re
from dotenv import load_dotenv
from discord.ext import commands
from typing import List, Union

from boss_rotations import *

REACTION_TIMEOUT = 15   # seconds

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = 680211088729571560

COMMAND_PREFIX = r'.'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

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

# proposed letters used to denote CoX boss rooms
IDIOSYNCRATIC_LETTERS_DICT = {
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
open_shamans = 'You have the open shamans layout'
closed_shamans = 'You have the multi-entry shamans layout'
cm_tekton = 'You have CM Tekton'
cm_shamans = 'You have CM Shamans'
cm_vanguards = 'You have CM Vanguards'
cm_mystics = 'You have CM Mystics'
cm_muttadile = 'You have CM Muttadiles'
boulder = 'You have a chance to redemption the final boulder'

room_layouts_dir = pathlib.Path(r'room_layouts')


async def add_bot_reactions(msg: discord.Message, emojis: Union[str, discord.Emoji, list]):

    if isinstance(emojis, list):
        for emoji in emojis:
            await msg.add_reaction(emoji)

    else:
        await msg.add_reaction(emojis)


async def choose_emoji(msg: discord.Message, emojis: Union[str, discord.Emoji, list],
                       allowed_users: Union[discord.Member, list] = None):

    def check_author(reaction, author) -> bool:
        condition_one = reaction.message.author != author

        if isinstance(allowed_users, list):
            condition_two = author in allowed_users

        elif isinstance(allowed_users, discord.Member):
            condition_two = author == allowed_users

        else:
            condition_two = True

        return condition_one and condition_two

    await add_bot_reactions(msg, emojis)

    try:
        react, user = await bot.wait_for('reaction_add', timeout=REACTION_TIMEOUT, check=check_author)
        return react.emoji

    except asyncio.TimeoutError:
        await msg.clear_reactions()


async def create_rotations_embed(rots: List[list]) -> (discord.Embed, list):
    RotationsEmbed = discord.Embed(
        Title='Possible rotations',
        description='React with the corresponding emoji',
        colour=discord.Colour.dark_purple()
    )

    guild = bot.get_guild(GUILD_ID)
    emojis = []

    for r in rots:
        rot_repr = '-'.join(r)
        rot_emoji = discord.utils.get(guild.emojis, name=r[0])
        RotationsEmbed.add_field(name=rot_emoji, value=rot_repr, inline=False)
        emojis.append(rot_emoji)

    return RotationsEmbed, emojis


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user.name} has connected to {guild.name} {guild.id}!')


@bot.command(name='rot', aliases=['r'],
             help='''
             BOSS           SHORT CODE [idiosyncratic|conventional]
             Tekton         t
             Vasa           v
             Guardians      g
             Mystics        [y|m]
             Shamans        s
             Muttadiles     m
             Vanguards      [n|v]
             Vespula        [e|v]

             ROOMS          SHORT CODE
             fsccs pcpsf    fscc
             scpfc cspsf    scpf
             scspf ccspf    scsp
             sfccs pcpsf    sfcc

             examples:
             {}rot tmg sfcc
             {}rot ytmg scpf
             '''.format(COMMAND_PREFIX, COMMAND_PREFIX))
async def rot(ctx, boss_shortcode: str, room_shortcode: str):

    try:
        possible_rotations = boss_rotation_shortcode_decoder(boss_shortcode)
        assert len(possible_rotations) > 0

    except AssertionError as E:
        ctx.send(f'{E}')
        raise E

    bosses = None

    if len(possible_rotations) == 1:
        bosses = possible_rotations[0]

    else:
        PossibleRotationsEmbed, possible_rotation_emojis = await create_rotations_embed(possible_rotations)

        EmbedMessage = await ctx.send(embed=PossibleRotationsEmbed)
        chosen_emoji = await choose_emoji(msg=EmbedMessage, emojis=possible_rotation_emojis,
                                          allowed_users=ctx.message.author)

        rotation_index = possible_rotation_emojis.index(chosen_emoji)
        bosses = possible_rotations[rotation_index]

    special = False

    if len(bosses) == 3:    # 3c2p
        boss1, boss2, boss3 = bosses
        rooms_image = room_layouts_dir.joinpath(''.join(['3c2p ', room_shortcode, '.png']))
        await ctx.send(file=discord.File(rooms_image))

        if room_shortcode == 'fscc':
            if 'vespula' in [boss3]:
                await ctx.send(vespula_bad_entry)
                special = True

            if 'shamans' in [boss1, boss2]:
                await ctx.send(cm_shamans)
                special = True

            elif 'shamans' in [boss3]:
                await ctx.send(open_shamans)
                special = True

            if 'muttadiles' in [boss1, boss2]:
                await ctx.send(cm_muttadile)
                special = True

            await ctx.send(boulder)
            special = True

        elif room_shortcode == 'scpf':
            if 'muttadiles' in [boss1, boss3]:
                await ctx.send(no_zgs_needed)
                special = True

            elif 'muttadiles' in [boss2]:
                await ctx.send(cm_muttadile)
                special = True

            if 'mystics' in [boss1]:
                await ctx.send(cm_mystics)
                special = True

            if 'shamans' in [boss2]:
                await ctx.send(cm_shamans)
                special = True

            elif 'shamans' in [boss1, boss3]:
                await ctx.send(closed_shamans)
                special = True

            if 'vespula' in [boss1]:
                await ctx.send(vespula_bad_entry)
                special = True

            elif 'vespula' in [boss3]:
                await ctx.send(vespula_good_entry)
                special = True

        elif room_shortcode == 'scsp':
            if 'muttadiles' in [boss3]:
                await ctx.send(no_zgs_needed)
                special = True

            if 'vespula' in [boss1, boss3]:
                await ctx.send(vespula_bad_entry)
                special = True

            elif 'vespula' in [boss2]:
                await ctx.send(vespula_good_entry)
                special = True

            if 'shamans' in [boss1, boss2]:
                await ctx.send(open_shamans)
                special = True

            elif 'shamans' in [boss3]:
                await ctx.send(closed_shamans)
                special = True

            await ctx.send(boulder)
            special = True

        elif room_shortcode == 'sfcc':
            if 'muttadiles' in [boss2]:
                await ctx.send(no_zgs_needed)
                special = True

            if 'mystics' in [boss2]:
                await ctx.send(cm_mystics)
                special = True

            if 'tekton' in [boss1]:
                await ctx.send(cm_tekton)
                special = True

            if 'vanguards' in [boss1]:
                await ctx.send(cm_vanguards)
                special = True

            if 'vespula' in [boss2]:
                await ctx.send(vespula_bad_entry)
                special = True

            elif 'vespula' in [boss3]:
                await ctx.send(vespula_good_entry)
                special = True

            if 'shamans' in [boss2]:
                await ctx.send(closed_shamans)
                special = True

            elif 'shamans' in [boss3]:
                await ctx.send(open_shamans)
                special = True

            await ctx.send(boulder)
            special = True

    elif len(bosses) == 4:      # 4c1p
        boss1, boss2, boss3, boss4 = bosses
        rooms_image = room_layouts_dir.joinpath(''.join(['4c1p ', room_shortcode, '.png']))
        await ctx.send(file=discord.File(rooms_image))

        if room_shortcode == 'sccf':
            if 'shamans' in [boss1, boss4]:
                await ctx.send(cm_shamans)
                special = True

            elif 'shamans' in [boss2]:
                await ctx.send(closed_shamans)

            if 'muttadiles' in [boss2]:
                await ctx.send(no_zgs_needed)
                special = True

            elif 'muttadiles' in [boss1, boss4]:
                await ctx.send(cm_muttadile)
                special = True

            if 'tekton' in [boss3]:
                await ctx.send(cm_tekton)
                special = True

            if 'vanguards' in [boss3]:
                await ctx.send(cm_vanguards)
                special = True

            if 'vespula' in [boss2]:
                await ctx.send(vespula_good_entry)
                special = True

        elif room_shortcode == 'scpf':

            if 'shamans' in [boss1]:
                await ctx.send(cm_shamans)
                special = True

            elif 'shamans' in [boss2, boss3]:
                await ctx.send(closed_shamans)
                special = True

            elif 'shamans' in [boss4]:
                await ctx.send(open_shamans)
                special = True

            if 'muttadiles' in [boss1]:
                await ctx.send(cm_muttadile)
                special = True

            elif 'muttadiles' in [boss2, boss3]:
                await ctx.send(no_zgs_needed)
                special = True

            if 'vespula' in [boss2]:
                await ctx.send(vespula_good_entry)
                special = True

            elif 'vespula' in [boss3, boss4]:
                await ctx.send(vespula_bad_entry)
                special = True

            if 'mystics' in [boss3]:
                await ctx.send(cm_mystics)

            await ctx.send(boulder)
            special = True

    else:
        await ctx.send(f'rotation not recognized {ctx.content}')
        special = True

    if not special:
        await ctx.send(no_special_characteristics)


if __name__ == '__main__':
    bot.run(TOKEN)
    bot.change_presence(activity='type !help rot for help', status='type !help rot for help')
