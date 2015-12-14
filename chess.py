#!/usr/bin/python

import string
import operator as op
from __future__ import print_function

ALPHABET = string.lowercase[:8]
OPERATOR_MAP  = {'black':op.add, 'white': op.sub}
PLAYERS = {'PLAYER_1': None, 'PLAYER_2': None}

# TODO Make Board use class instead of instance. Change getter and setter
# methods to actual properties where possible. 
# create moves config
# write check board state method to dteermine if game is over. 
# create if name equals main, with sys.close(). In order to use
# raw_input to start the game. 

'''A simple interface for a chess application.'''



class Square(object):

	def __init__(self, name, square_id, piece = None):
		self.square_id = square_id
		self.name = name
		self.piece = piece
	
	def __str__(self):
		return 'square {}'.format(self.name)

	def __repr__(self):
		if self.piece:
			return '{:^10}'.format(self.piece)
		else:
			return '{:^10}'.format(self.name)

	def get_name(self):
		return self.piece.name or self.name

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

	def __init__(self, name=None, owner=None, location=None, moves = None):
		self.name = name
		self.owner = owner
		self.location = location
		self.moves = moves or {}
		self.set_moves()


	def __str__(self):
		return '{}'.format(self.name)

	def __repr__(self):
	# 	# return 'Piece({},{},{})'.format(self.name, self.owner, self.moves)
		return '{}'.format(self.name)

	def get_moves(self):
		pass

	def validate_move(self, x, y):
		# TODO figure out string index wrap around issue.
		try:
			move = '{}{}'.format(ALPHABET[self.location[0]+x], OPERATOR_MAP[self.owner.color](self.location[1], y))
			if move in Board.squares:
				return move
			else:
				return False
		except IndexError:
			return False


	def set_moves(self):

		self.moves['regular'] = [self.validate_move(0, 1),]
		# self.moves['attack'] = [self.validate_move(1, 1), self.validate_move(-1, 1)]

	def get_location(self, board):
		
		for row in board:
			for square in row:
				if square.piece == self:
					return square


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

	def __init__(self):
		'''create a chess board with pieces positioned for a new game
        row ordering is reversed from normal chess representations
        but corresponds to a top left screen coordinate 
        '''
         
		self.board = []
		self.player_one_pieces = None
		self.player_two_pieces = None

		for i in range(8, 0, -1):
			row = []
			for index, letter in enumerate(ALPHABET):
				row.append(Square(square_id=(index, i), name='square{}{}'.format(letter, i)))
				Board.squares.append('{}{}'.format(letter, i))
			self.board.append(row)
		
        
	def __str__(self):
		return '\n'.join(str(square) for square in self.board)
	
	def __repr__(self):
		return 'Board({})'.format(self.board)

	def reset_board(self):
		
		for row in self.board:
			for square in row:
				square.piece = None

		PLAYERS['PLAYER_1'] = Player('Levi', 'white')
		PLAYERS['PLAYER_2'] = Player('Fernanda', 'black')
		self.__set_pawns(self.board[1], PLAYERS['PLAYER_1'], 7)
		self.__set_pawns(self.board[6], PLAYERS['PLAYER_2'], 2)
		self.__set_other_pieces(self.board[0], PLAYERS['PLAYER_1'], 8)
		self.__set_other_pieces(self.board[7], PLAYERS['PLAYER_2'], 1)


	def __set_pawns(self, row, player, row_num):
	
		return [square.update(Pawn('{}{}{}'.format('PAWN', player.name[0].upper(), i), player, (i, row_num))) for i, square in enumerate(row)]

	def __set_other_pieces(self, row, player, row_num):		

		pieces = 	 [
				Rook('{}{}{}'.format('ROOK', player.name[0].upper(), 0), player, (0, row_num)),
				Knight('{}{}{}'.format('KNIGHT', player.name[0].upper(), 0), player, (1, row_num)),
				Bishop('{}{}{}'.format('BISHOP', player.name[0].upper(), 0), player, (2, row_num)),
				Queen('{}{}'.format('QUEEN', player.name[0].upper()), player, (3, row_num)),
				King('{}{}'.format('KING', player.name[0].upper()), player, (4, row_num)),
				Bishop('{}{}{}'.format('BISHOP', player.name[0].upper(), 1), player, (5, row_num)),
				Knight('{}{}{}'.format('KNIGHT', player.name[0].upper(), 1), player, (6, row_num)),
				Rook('{}{}{}'.format('ROOK', player.name[0].upper(), 1), player, (7, row_num)),
				]

		return [square.update(pieces[i]) for i, square in enumerate(row)]

	def __validate_piece(self, piece_name, player):

		for row in self.board:
			for square in row:
				if (square.get_name(), square.get_owner()) == (piece_name, player):
					return square					
		else:
			return False

	def __validate_location(self, location, player, valid_piece):

		for row in self.board:
			for square in row:
				if all([square.get_name() == location, square.get_owner() != player, square in valid_piece.piece.get_moves()]):
					return square
		else:
			return False

	def __validate(self, player, piece_name, location):
		
		context = {}
		valid_piece =  self.__validate_piece(piece_name, player)
		if not valid_piece:
			context['message'] = 'Please select a valid piece.'
			return context
		
		valid_location = self.__validate_location(location, player, valid_piece)
		if not valid_location:
			context['message'] = 'Please select a valid location.'
			return context

		context['validated_piece'] = valid_piece
		context['validated_location'] = valid_location
		return context
		
	def move(self, player, piece_name, location):
		
		validated_vals =  self.__validate(player, piece_name, location)
		if 'message' in validated_vals:
			return validated_vals['message']
		else:
			print('\n\nMoved {} to {}.\n\n'.format(validated_vals['validated_piece'].piece, validated_vals['validated_location']))
			validated_vals['validated_location'].piece = validated_vals['validated_piece'].piece
			validated_vals['validated_location'].piece.set_moves()
			validated_vals['validated_piece'].piece = None
			return self.__check_state() or '\n\n\n{}\n\n\n'.format(self.board) 


	def __check_state(self):
		# return message if it's game over, otherwise return False.
		pass


