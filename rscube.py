from kociemba import solve
import time
from lookups import *

class MyCube(object):

	def __init__(self):
		self._colors = [] # list of colors to match against
		self._cube_colors = [[None for i in range(9)] for j in range(6)]  # letter for corresponding face_color for each site on cube
		self.solveto_name = 'Solid Cube'  # string representing cube solve to pattern
		self._solve_string = None  # instructions to solve cube

		self.orientation = 'UFD'  # current orientation of the cube, Upface, gripper A Face, gripper B Face

	@property
	def orientation(self):
		return self._orientation

	@orientation.setter
	def orientation(self, val):
		self._orientation = val

	@property
	def solveto_name(self):
		return self._solveto_name

	@solveto_name.setter
	def solveto_name(self, name):
		self._solveto_name = name
		self._solveto_pat = PATTERNS[name][1]
		print('Solveto pattern:{}'.format(self._solveto_pat))
		self.set_solve_string()

	def get_abs_site(self, site_r):
		"""
		Transposes site numbers given up_face rotation. Returns un-rotated site number given rotated site.
		"""
		return ROT_TABLE[UP_FACE_ROT[self._orientation]][site_r - 1]

	def set_solve_string(self):
		"""
		Sets and returns the solve string from kociemba
		"""
		if self.get_cube_def() == self._solveto_pat:
			self._solve_string = None
		else:
			self._solve_string = solve(self.get_cube_def(), self._solveto_pat)
		print('Solve string:{}'.format(self._solve_string))  # debug
		return self._solve_string
		#print('Solve string:{}'.format(self._solve_string))  # debug
		#self._solve_string = "R' D2 R' U2 R F2 D B2 U' R F' U R2 D L2 D' B2 R2 B2 U' B2" # debug

	def set_cube_colors(self):
		"""
		Sets each site to letter representing face color
		"""
		for f in range(6):
			for s in range(9):
				break
				#self._cube_colors[f][s] = FACES_STR[self._face_colors.index(self._match_colors[f][s])]
		#print self._cube_colors # debug

	def get_cube_def(self):
		"""
		Returns cube_def in the form UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
		"""
		return 'RLLDUUDDURLULRULLDFBFFFFFFFDUUUDDRRLURRDLRDRLBBBBBFBBB'  # debug
		#return ''.join(str(site) for sitelist in self._cube_colors for site in sitelist)

	def get_up_face(self):
		"""
		Returns string representing current up face
		"""
		return FACES_STR[FACE_POSITION[self._orientation][U]]

	def get_up_rot(self):
		"""
		Returns current rotation of up_face
		"""
		return UP_FACE_ROT[self._orientation]

	def set_orientation(self, gripper, dir):
		"""
		Updates cube orientation given a gripper and direction it twisted
		"""
		if gripper == 'A':
			self.orientation = NEW_ORIENTATION_TWISTA[self.orientation][dir]
		elif gripper == 'B':
			self.orientation = NEW_ORIENTATION_TWISTB[self.orientation][dir]
		print('New orientation: {}'.format(self.orientation))

	def get_moves_to_twist_face(self, face_to_move, to_gripper = None):
		"""
		Determines moves to twist face_to_move to gripper A or B depending on fewest moves.
		If gripper passed as arg, face_to_move will be positioned to input gripper.
		Returns ([moves], chosen gripper)
		"""
		moves = None
		o = self._orientation
		#print (o)

		# get current position of face to move
		face = FACE_POSITION[o].index(FACES[face_to_move])

		# get the moves to both gripper A and B so they can be compared
		moves_a = MOVES_TO_A[face].split(',')
		if moves_a[0] == '':
			moves_a = []
		moves_b = MOVES_TO_B[face].split(',')
		if moves_b[0] == '':
			moves_b = []

		# if a gripper was passed in as argument, move to that gripper
		if to_gripper == 'A':
			moves = moves_a
		elif to_gripper == 'B':
			moves = moves_b
		else:  # else pick the least number of moves
			if len(moves_a) <= len(moves_b):
				moves = moves_a  # moves to gripper A
				to_gripper = 'A'
			else:
				moves = moves_b  # moves to gripper B
				to_gripper = 'B'
		
		return moves, to_gripper
