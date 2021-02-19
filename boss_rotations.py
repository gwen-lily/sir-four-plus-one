from typing import List, Tuple

# typical letters used to denote CoX boss rooms
CONVENTIONAL_LETTERS = [
	't',
	'v',
	'g',
	'm',
	's',
]

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

IDIOSYNCRATIC_LETTERS = list(IDIOSYNCRATIC_LETTERS_DICT.keys())


def is_idiosyncratic(s: str) -> bool:
	"""Returns true if a shortcode unamibuously makes use of the idiosyncratic short codes"""
	identifier_letters = set(IDIOSYNCRATIC_LETTERS) - set(CONVENTIONAL_LETTERS)
	return any(il in s for il in identifier_letters)


def idiosyncratic_to_conventional_shortcode(s: str) -> str:
	s_prime = [IDIOSYNCRATIC_LETTERS_DICT[ch][0:1] for ch in s]
	return ''.join(s_prime)


ROTATION_ONE = 'tvgysmne'
ROTATION_TWO = 'tmgesvny'
FULL_ROTATIONS = [ROTATION_ONE, ROTATION_TWO]

ROTATION_ONE_LONG = [IDIOSYNCRATIC_LETTERS_DICT[ch] for ch in ROTATION_ONE]
ROTATION_TWO_LONG = [IDIOSYNCRATIC_LETTERS_DICT[ch] for ch in ROTATION_TWO]

FULL_ROTATIONS_LONG = {
	ROTATION_ONE: ROTATION_ONE_LONG,
	idiosyncratic_to_conventional_shortcode(ROTATION_ONE): ROTATION_ONE_LONG,
	ROTATION_TWO: ROTATION_TWO_LONG,
	idiosyncratic_to_conventional_shortcode(ROTATION_TWO): ROTATION_TWO_LONG
}


def is_valid_rotation(rot: str) -> bool:
	"""Only works with idiosyncratic definition, really simple function"""

	assert is_idiosyncratic(rot) or True    # TODO: Catch rots that don't double up but don't contain identifier char

	for rotation in FULL_ROTATIONS:

		rotation_wrapped = ''.join(rotation * 3)
		rotation_wrapped_reverse = rotation_wrapped[::-1]

		if rot in rotation_wrapped or rot in rotation_wrapped_reverse:
			return True

	return False


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
	chars = [c for c in rot]
	bosses = len(chars)
	possible_rotations = []

	assert 3 <= bosses <= 5
	assert all(c in CONVENTIONAL_LETTERS for c in chars) or all(c in IDIOSYNCRATIC_LETTERS for c in chars)

	# Return unambiguous validated rotation if the input matches these conditions
	if is_idiosyncratic(rot) and is_valid_rotation(rot):
		possible_rotations.append([IDIOSYNCRATIC_LETTERS_DICT[ch] for ch in rot])
		return possible_rotations

	# Else, work with ambiguity, and at this point it must be conventional otherwise the input was wrong

	for full_rotation in FULL_ROTATIONS:
		conventional_rotation = idiosyncratic_to_conventional_shortcode(full_rotation)
		possible_starting_rooms = find_all_char_indices(conventional_rotation, chars[0])

		for sr in possible_starting_rooms:
			for direction in [False, True]:
				scout_short, scout_long = walk_rotation(conventional_rotation, sr, bosses, direction)

				if rot == scout_short:
					possible_rotations.append(scout_long)

	return possible_rotations


if __name__ == '__main__':
	# print(boss_rotation_shortcode_decoder('mtmgv'))
	inp = 'vsvs'

	print(idiosyncratic_to_conventional_shortcode(inp))
	print(boss_rotation_shortcode_decoder(inp))
