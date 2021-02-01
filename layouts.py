import re
from typing import List

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

east, north, west, south = 0, 1, 2, 3


class Room:

	def __init__(self, enter: int, leave: int):
		self.enter = enter
		self.leave = leave
		self.rotation = (leave - enter) % 4

class FarmingRoom(Room):

	def __init__(self, enter: int, leave: int):
		super().__init__(enter, leave)

class ScavengerRoom(Room):

	def __init__(self, enter: int, leave: int):
		super().__init__(enter, leave)

	def potential_boulder_redemption(self):
		return True if self.rotation == 3 else False

class PuzzleRoom(Room):

	def __init__(self, enter: int, leave: int, puzzle: str = None):
		self.puzzle = puzzle
		super().__init__(enter, leave)

	def is_cm(self):
		if self.puzzle in ['crabs']:
			pass

		elif self.puzzle in ['ice demon', 'thieving']:
			return True if self.rotation == 2 else False

class CombatRoom(Room):

	def __init__(self, enter: int, leave: int, boss: str = None):
		self.boss = boss
		super().__init__(enter, leave)

	def is_cm(self):
		if self.boss in ['tekton', 'vasa', 'guardians', 'vanguards']:
			return True if self.enter == 0 and self.leave == 2 else False

		elif self.boss in ['shamans', 'muttadiles']:
			return True if self.enter == 2 and self.leave == 0 else False

		elif self.boss in ['mystics']:
			return True if self.enter == 1 and self.leave == 0 else False

		elif self.boss in ['vespula']:
			return True if self.enter == 3 and self.leave == 0 else False

	def muttadile_bell_lure(self):
		return True if self.rotation == 3 else False

	def vespula_annoying_layout(self):
		return True if self.rotation == 3 else False

	def vespula_normal_layout(self):
		return True if self.rotation == 1 else False

	def cm_tile_entry(self):
		return True if self.enter in [2, 3] and not self.rotation == 2 else False


class Layout:

	def __init__(self, rooms: List[Room]):




def generate_layouts():
	fscc = Layout([
		FarmingRoom(0, 3),
		ScavengerRoom(1, 0),
		CombatRoom(2, 0),
		CombatRoom(2, 0),
		ScavengerRoom(2, 1),
		PuzzleRoom(0, 3),
		CombatRoom(1, 2),
		PuzzleRoom(0, 1),
		ScavengerRoom(3, 2),
		FarmingRoom(0, 3)
	])