#!/usr/bin/python

from __future__ import print_function
import sys
import string
import operator as op

'''A simple terminal based chess application. This isnt complete however should
give you an idea as to how I would complete the rest of the program. You can however
run the program and move the pawns, there is clearly much left to do to complete the program
but for the sake of time I figured this would be enough.'''

'''To move a and named PawnL1 to location squareA5 you would type both of 
those names into the console when prompted.'''


ALPHABET = string.lowercase[:8]
OPERATOR_MAP = {'black':op.sub, 'white': op.add}
PLAYERS = {'PLAYER_1': None, 'PLAYER_2': None}
PIECE_MOVES = {
				'Pawn': {
					'Regular': [(0,1)], 
					'Attack': [(1, 1), (-1, 1)],
					'Initial': [(0, 2)]
				},
				'Rook': {
					'Regular': []
				},
				'Knight': {
					'Regular': []
				},
				'Bishop': {
					'Regular': []
				},
				'Queen': {
					'Regular': []
				},
				'King': {
					'Regular': []
				}
			}


class Player(object):
	'''The player class, players become associated with Pieces.'''

	def __init__(self, name, color):
		self.name = name
		self.color = color

	def __str__(self):
		return '{}'.format(self.name)

	def __repr__(self):
		return 'Player({})'.format(self.name)


class Piece(object):
	'''The base class for chess Pieces. They have location tuples, and types to 
	associate them with their corresponding moves from the PIECE_MOVES dict. They are all
	also subclassed because as the program develops it will be easier to differentiate their
	functionality.'''

	def __init__(self, name, owner, location, piece_type):
		self.name = name
		self.owner = owner
		self.location = location
		self.initial = True
		self.piece_type = piece_type
		self.moves = {}
		self.set_moves()

	def __repr__(self):	
		return '{}'.format(self.name)

	def get_moves(self, attack):
		'''Returns the available moves from the corresponding Piece. Since some Pieces
		like Pawns have different available moves depending on if the move is an attack
		or not, it takes an additional parameter.'''

		if all([attack, PIECE_MOVES[self.piece_type].get('Attack', False)]):
			return self.moves['attack']
		else:
			return self.moves['regular']

	def validate_move(self, x, y):
		'''Takes two values that act as the distance from the current location, and
		validates whether or not it exists on the Board.'''

		move = (self.location[0]+x, OPERATOR_MAP[self.owner.color](self.location[1], y))		
		if move in Board.squares:
			return move
		else:
			return False

	def set_moves(self):
		'''Adds moves to this pieces moves attribute. Because some moves have different moves available
		depending on if its attacking, or if its the first move of the game. This differentiates
		between them accordingly.'''

		self.moves['regular'] = [self.validate_move(x, y) for x, y in PIECE_MOVES[self.piece_type].get('Regular')]
		if self.initial:
			self.initial = False
			if PIECE_MOVES[self.piece_type].get('Initial', False):
				self.moves['regular'].extend([self.validate_move(x, y) for x, y in PIECE_MOVES[self.piece_type].get('Initial')])
		if PIECE_MOVES[self.piece_type].get('Attack', False):			
			self.moves['attack'] = [self.validate_move(x, y) for x, y in PIECE_MOVES[self.piece_type].get('Attack')]


class Pawn(Piece):
	'''The Pawn class.'''

	def __init__(self, name, owner, location, piece_type):		
		super(Pawn, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class King(Piece):
	'''The King class.'''

	def __init__(self, name, owner, location, piece_type):
		super(King, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class Queen(Piece):
	'''The Queen class.'''

	def __init__(self, name, owner, location, piece_type):
		super(Queen, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class Rook(Piece):
	'''The Rook class.'''

	def __init__(self, name, owner, location, piece_type):
		super(Rook, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class Bishop(Piece):
	'''The Bishop class.'''

	def __init__(self, name, owner, location, piece_type):
		super(Bishop, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class Knight(Piece):
	'''The Knight class.'''

	def __init__(self, name, owner, location, piece_type):
		super(Knight, self).__init__(name=name, owner=owner, location=location, piece_type=piece_type)


class Square(object):
	'''A square on the Board. can contain a Piece object. Since this is console based
	game. To make things visually easier to see, If it contains a piece it will display the
	Piece name on the Board, otherwise it will display its name.'''

	def __init__(self, name, square_id, piece=None):
		self.square_id = square_id
		self._name = name
		self.piece = piece

	def __repr__(self):
		return '{:^10}'.format(self.name)

	@property
	def name(self):
		'''Returns the piece name if it contains a piece,
		otherwise it returns its name.'''

		if self.piece:
			return self.piece.name
		else:
			return self._name

	@name.setter
	def name(self, val):
		'''Sets the name attribute.'''

		self._name = val


	def get_owner(self):
		'''Returns the owner of the piece if it
		contains a piece.'''

		if self.piece:
			return self.piece.owner
		else:
			return False

	def update(self, piece):
		self.piece = piece


class Board(object):
	'''The Board contains Squares. Since there can only be one Board, all
	attributes and methods are associated with the class instead of an instance
	of the class.'''

	squares = []
	square_ids = []
	contents = []
	turn = None
	result_message = None

	def __str__(self):
		return '\n'.join(str(square) for square in self.contents)	

	@classmethod
	def display_board(cls):
		'''Displays the Board to the console.'''

		print('\n{}\n'.format(cls()))

	@classmethod
	def reset_board(cls):
		'''Creates the Board and adds all the appropriate Square objects to it. 
		Creates a class attribute with all the valid square locations.
		Adds the Players to the appropriate Squares and checks state. The range is
		decramenting because the names it creates visually looks better when displaying the Board.'''

		for i in range(8, 0, -1):
			row = []
			for index, letter in enumerate(ALPHABET):
				row.append(Square(square_id=(index, i), name='square{}{}'.format(letter.upper(), i)))
				cls.squares.append((index, i))
			cls.contents.append(row)

		for row in cls.contents:
			for square in row:
				square.piece = None

		cls.turn = PLAYERS.get('PLAYER_1')
		cls.__set_pawns(cls.contents[1], PLAYERS.get('PLAYER_1'), 7)
		cls.__set_pawns(cls.contents[6], PLAYERS.get('PLAYER_2'), 2)
		cls.__set_other_pieces(cls.contents[0], PLAYERS.get('PLAYER_1'), 8)
		cls.__set_other_pieces(cls.contents[7], PLAYERS.get('PLAYER_2'), 1)
		cls.__check_state()

	@classmethod
	def __set_pawns(cls, row, player, row_num):
		'''Creates and adds Pawns to the row, and returns the updated row.'''

		return [square.update(Pawn('{}{}{}'.format('pawn', player.name[0].upper(), i), player, (i, row_num), 'Pawn')) for i, square in enumerate(row)]

	@classmethod
	def __set_other_pieces(cls, row, player, row_num):		
		'''Creates and adds the other pieces to the row, and returns the updated row.'''

		pieces = [
				Rook('{}{}{}'.format('rook', player.name[0].upper(), 0), player, (0, row_num), 'Rook'),
				Knight('{}{}{}'.format('knight', player.name[0].upper(), 0), player, (1, row_num), 'Knight'),
				Bishop('{}{}{}'.format('bishop', player.name[0].upper(), 0), player, (2, row_num), 'Bishop'),
				Queen('{}{}'.format('queen', player.name[0].upper()), player, (3, row_num), 'Queen'),
				King('{}{}'.format('king', player.name[0].upper()), player, (4, row_num), 'King'),
				Bishop('{}{}{}'.format('bishop', player.name[0].upper(), 1), player, (5, row_num), 'Bishop'),
				Knight('{}{}{}'.format('knight', player.name[0].upper(), 1), player, (6, row_num), 'Knight'),
				Rook('{}{}{}'.format('rook', player.name[0].upper(), 1), player, (7, row_num), 'Rook'),
				]

		return [square.update(pieces[i]) for i, square in enumerate(row)]

	@classmethod
	def __validate_piece(cls, piece_name, player):
		'''Checks to see if the Player trying to move a piece, actually owns
		that piece.'''

		for row in cls.contents:
			for square in row:
				if (square.name, square.get_owner()) == (piece_name, player):
					return square					
		else:
			return False

	@classmethod
	def __validate_location(cls, location, player, valid_piece):
		'''Checks the location the Player is trying to move a Piece to,
		and validates that the location exists, is empty, or that they dont own
		the Piece that occupies that square.'''

		for row in cls.contents:
			for square in row:
				if all([square.name == location, square.get_owner() != player, square.square_id in valid_piece.piece.get_moves(square.get_owner())]):
					return square
		else:
			return False

	@classmethod
	def __validate(cls, player, piece_name, location):
		'''Validates the Piece the Player is moving, and 
		the Location that the Player is moving it to. Returns an error 
		message if invalid.'''

		context = {}
		valid_piece = cls.__validate_piece(piece_name, player)
		if not valid_piece:
			context['message'] = '\nPlease select a valid piece.\n'
			return context
		
		valid_location = cls.__validate_location(location, player, valid_piece)
		if not valid_location:
			context['message'] = '\nPlease select a valid location.\n'
			return context

		context['validated_piece'] = valid_piece
		context['validated_location'] = valid_location
		return context
		
	@classmethod
	def __move(cls, player, piece_name, location):
		'''Attempts to move a Piece to a new location.
		Toggles the Player if the move is valid.
		Checks the state of the Board to determine if the game is over.'''

		validated_vals = cls.__validate(player, piece_name, location)
		if 'message' in validated_vals:
			print(validated_vals['message'])
			cls.__retry()
		else:
			print('\nMoved {} to {}.\n'.format(validated_vals['validated_piece'].piece.name, validated_vals['validated_location'].name))
			validated_vals['validated_location'].piece = validated_vals['validated_piece'].piece
			validated_vals['validated_location'].piece.location = validated_vals['validated_location'].square_id
			validated_vals['validated_location'].piece.set_moves()
			validated_vals['validated_piece'].piece = None
			cls.__toggle_player(player)
			cls.__check_state()

	@classmethod
	def __retry(cls):
		'''Restarts move for a Player if their attempted move 
		was not successful.'''

		piece, location = cls.__prompt_player()
		cls.__move(cls.turn, piece, location)

	@classmethod
	def __prompt_player(cls):
		'''Prompts a Player to enter the Piece they want to move, and 
		the location they would like to move it to.'''

		piece = raw_input('\n{}, enter the name of the piece you want to move: '.format(cls.turn))
		location = raw_input('\nNow enter then name of the location or piece you want to move it to: ')
		return piece, location

	@classmethod
	def __check_state(cls):
		'''Checks the state of the Board to determine if one of the criteria 
		is met for the game to be over. Or prompts the next Player to move.'''

		if any([cls.__is_checkmate(), cls.__is_draw()]):
			print('{}'.format(cls.result_message))
		else:
			if cls.__is_check():
				print('{}'.format(cls.result_message))
				cls.result_message = None
			cls.display_board()
			piece, location = cls.__prompt_player()
			cls.__move(cls.turn, piece, location)

	@classmethod
	def __toggle_player(cls, player):
		'''Toggles the Players turn.'''

		if player is PLAYERS.get('PLAYER_1'):
			cls.turn = PLAYERS.get('PLAYER_2')
		else:
			cls.turn = PLAYERS.get('PLAYER_1')

	@classmethod
	def __is_checkmate(cls):
		'''Checks board state to determine if checkmate and if so, sets the state dict to True and updates
		the result message to let the users know the end result of the game.'''
		pass

	@classmethod
	def __is_check(cls):
		'''Checks board state to determine if check and if so, sets the state dict to True and updates
		the result message to let the users know the end result, but continues on to the next turn.'''
		pass

	@classmethod
	def __is_draw(cls):
		'''Checks board state to determine if draw and if so, sets the state dict to True and updates
		the result message to let the users know the end result of the game.'''
		pass

def main():
	'''The main entry point for the game. Prompts the Players to 
	enter their names and resets the Board.'''

	player_1 = raw_input('\nPlayer 1, enter your name: ')
	player_2 = raw_input('\nPlayer 2, enter your name: ')

	PLAYERS['PLAYER_1'] = Player(player_1, 'black')
	PLAYERS['PLAYER_2'] = Player(player_2, 'white')
	Board.reset_board()


'''The below is for when the game is ran directly. It will exit the shell correctly
when the game is complete. As well as allow it to be callable from other programs, and be monitored 
for failure without custom rules.'''

if __name__ == '__main__':
	sys.exit(main())

