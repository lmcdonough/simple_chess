#!/usr/bin/python

from __future__ import print_function
import sys
import string
import operator as op


ALPHABET = string.lowercase[:8]
OPERATOR_MAP = {'black':op.sub, 'white': op.add}
PLAYERS = {'PLAYER_1': None, 'PLAYER_2': None}

# create moves config

'''A simple interface for a chess application.'''

class Square(object):

	def __init__(self, name, square_id, piece = None):
		self.square_id = square_id
		self._name = name
		self.piece = piece

	def __repr__(self):
		return '{:^10}'.format(self.name)

	@property
	def name(self):
		if self.piece:
			return self.piece.name
		else:
			return self._name

	@name.setter
	def name(self, val):
		self._name = val


	def get_owner(self):
		if self.piece:
			return self.piece.owner
		else:
			return False

	def update(self, piece):
		self.piece = piece

class Player(object):
	
	def __init__(self, name, color):
		self.name = name
		self.color = color

	def __str__(self):
		return '{}'.format(self.name)

	def __repr__(self):
		return 'Player({})'.format(self.name)

class Piece(object):

	def __init__(self, name=None, owner=None, location=None, moves=None):
		self.name = name
		self.owner = owner
		self.location = location
		self.moves = moves or {}
		self.set_moves()

	def __repr__(self):	
		return '{}'.format(self.name)

	def get_moves(self, attack):
		if attack:
			return self.moves['attack']
		else:
			return self.moves['regular']

	def validate_move(self, x, y):

		move = (self.location[0]+x, OPERATOR_MAP[self.owner.color](self.location[1], y))		
		if move in Board.squares:
			return move
		else:
			return False

	def set_moves(self):

		self.moves['regular'] = [self.validate_move(0, 1),]


class Pawn(Piece):

	def __init__(self, name, owner, location, moves=None, initial=True):		
		self.initial = initial
		super(Pawn, self).__init__(name=name, owner=owner, location=location, moves=moves)

	def set_moves(self):

		self.moves['regular'] = [self.validate_move(0, 1),]
		if self.initial:
			self.moves['regular'].append(self.validate_move(0, 2))
			self.initial = False
		self.moves['attack'] = [self.validate_move(1, 1), self.validate_move(-1, 1)]


class King(Piece):

	def __init__(self, name, owner, location, moves=None):
		super(King, self).__init__(name=name, owner=owner, location=location, moves=moves)


class Queen(Piece):

	def __init__(self, name, owner, location, moves=None):
		super(Queen, self).__init__(name=name, owner=owner, location=location, moves=moves)


class Rook(Piece):

	def __init__(self, name, owner, location, moves=None):
		super(Rook, self).__init__(name=name, owner=owner, location=location, moves=moves)


class Bishop(Piece):

	def __init__(self, name, owner, location, moves=None):
		super(Bishop, self).__init__(name=name, owner=owner, location=location, moves=moves)


class Knight(Piece):

	def __init__(self, name, owner, location, moves=None):
		super(Knight, self).__init__(name=name, owner=owner, location=location, moves=moves)



class Board(object):

	squares = []
	square_ids = []
	contents = []
	turn = None

	def __str__(self):
		return '\n'.join(str(square) for square in self.contents)	

	@classmethod
	def display_board(cls):
		print('\n{}\n'.format(cls()))

	@classmethod
	def reset_board(cls):
		
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
	
		return [square.update(Pawn('{}{}{}'.format('pawn', player.name[0].upper(), i), player, (i, row_num))) for i, square in enumerate(row)]

	@classmethod
	def __set_other_pieces(cls, row, player, row_num):		

		pieces = 	 [
				Rook('{}{}{}'.format('rook', player.name[0].upper(), 0), player, (0, row_num)),
				Knight('{}{}{}'.format('knight', player.name[0].upper(), 0), player, (1, row_num)),
				Bishop('{}{}{}'.format('bishop', player.name[0].upper(), 0), player, (2, row_num)),
				Queen('{}{}'.format('queen', player.name[0].upper()), player, (3, row_num)),
				King('{}{}'.format('king', player.name[0].upper()), player, (4, row_num)),
				Bishop('{}{}{}'.format('bishop', player.name[0].upper(), 1), player, (5, row_num)),
				Knight('{}{}{}'.format('knight', player.name[0].upper(), 1), player, (6, row_num)),
				Rook('{}{}{}'.format('rook', player.name[0].upper(), 1), player, (7, row_num)),
				]

		return [square.update(pieces[i]) for i, square in enumerate(row)]

	@classmethod
	def __validate_piece(cls, piece_name, player):

		for row in cls.contents:
			for square in row:
				if (square.name, square.get_owner()) == (piece_name, player):
					return square					
		else:
			return False

	@classmethod
	def __validate_location(cls, location, player, valid_piece):

		for row in cls.contents:
			for square in row:
				if all([square.name == location, square.get_owner() != player, square.square_id in valid_piece.piece.get_moves(square.get_owner())]):
					return square
		else:
			return False

	@classmethod
	def __validate(cls, player, piece_name, location):
		
		context = {}
		valid_piece =  cls.__validate_piece(piece_name, player)
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
		
		validated_vals =  cls.__validate(player, piece_name, location)
		if 'message' in validated_vals:
			print(validated_vals['message'])
		else:
			print('\nMoved {} to {}.\n'.format(validated_vals['validated_piece'].piece.name, validated_vals['validated_location'].name))
			validated_vals['validated_location'].piece = validated_vals['validated_piece'].piece
			validated_vals['validated_location'].piece.location = validated_vals['validated_location'].square_id
			validated_vals['validated_location'].piece.set_moves()
			validated_vals['validated_piece'].piece = None
			cls.__check_state()

	@classmethod
	def __check_state(cls):
		# return message if it's game over, otherwise return False.

		cls.display_board()
		player = cls.turn
		piece = raw_input('\n{}, enter the name of the piece you want to move: '.format(cls.turn))
		location = raw_input('\nNow enter then name of the location or piece you want to move it to: ')
		cls.__toggle_player(player)
		cls.__move(player, piece, location)

	@classmethod
	def __toggle_player(cls, player):
		
		if player is PLAYERS.get('PLAYER_1'):
			cls.turn = PLAYERS.get('PLAYER_2')
		else:
			cls.turn = PLAYERS.get('PLAYER_1')


def main():
	player_1 = raw_input('\nPlayer 1, enter your name: ')
	player_2 = raw_input('\nPlayer 2, enter your name: ')

	PLAYERS['PLAYER_1'] = Player(player_1, 'black')
	PLAYERS['PLAYER_2'] = Player(player_2, 'white')
	Board.reset_board()


if __name__ == '__main__':
	sys.exit(main())

