from typing import List, Tuple

ALLOWED_CONVENTIONAL_LETTERS = [
	't',
	'v',
	'g',
	'm',
	's',
]

ROTATION_ONE = 'tvgmsmvv'
ROTATION_TWO = 'tmgvsvvm'
FULL_ROTATIONS = [ROTATION_ONE, ROTATION_TWO]

ROTATION_ONE_LONG = [
	'tekton',
	'vasa',
	'guardians',
	'mystics',
	'shamans',
	'muttadiles',
	'vanguards',
	'vespula'
]

ROTATION_TWO_LONG = [
	'tekton',
	'muttadiles',
	'guardians',
	'vespula',
	'shamans',
	'vasa',
	'vanguards',
	'mystics'
]

FULL_ROTATIONS_LONG = {
	ROTATION_ONE: ROTATION_ONE_LONG,
	ROTATION_TWO: ROTATION_TWO_LONG,
}


def walk_rotation(rotation: str, start: int, length: int, reverse: bool = False) -> Tuple[str, List[str]]:
	"""
	Traverse a rotation given start point, number of bosses, and direction.

	:param rotation: 8-char str containing the conventional shortcodes for a full chamberx of xeric boss rotation.
	:param start: The index of the first room in the scouted rotation in the full rotation.
	:param length: The number of combat bosses in the scouted rotation.
	:param reverse: If true, traverse the rotation counter-clockwise, else traverse clockwise.
	:return: scouted_rotation: A str walking a given rotation, length, and reverse setting.
	"""
	offset = len(rotation)
	start = offset + start
	end = start - length if reverse else start + length
	delta = -1 if reverse else 1

	full_rotation_wrapped = ''.join(rotation * 3)
	full_rotation_wrapped_long = []

	for i in range(3):
		for e in FULL_ROTATIONS_LONG[rotation]:
			full_rotation_wrapped_long.append(e)

	scouted_rotation = full_rotation_wrapped[start:end:delta]
	scouted_rotation_long = full_rotation_wrapped_long[start:end:delta]

	return scouted_rotation, scouted_rotation_long


def find_all_char_indices(s: str, ch: str) -> List[int]:
	return [i for i, letter in enumerate(s) if letter == ch]


def boss_rotation_shortcode_decoder(rot: str):

	# sanitize input
	# chars = [c for c in rot.replace("\'", '')[::-1]] if "\'" in rot else [c for c in rot]
	chars = [c for c in rot]
	bosses = len(chars)

	assert all(c in ALLOWED_CONVENTIONAL_LETTERS for c in chars)
	assert 3 <= bosses <= 5

	possible_rotations = []

	for full_rotation in FULL_ROTATIONS:
		possible_starting_rooms = find_all_char_indices(full_rotation, chars[0])

		for sr in possible_starting_rooms:
			for direction in [False, True]:
				scout_short, scout_long = walk_rotation(full_rotation, sr, bosses, direction)

				if rot == scout_short:
					possible_rotations.append(scout_long)

	return possible_rotations


if __name__ == '__main__':
	print(boss_rotation_shortcode_decoder('mtmgv'))
