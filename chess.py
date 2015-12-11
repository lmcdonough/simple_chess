#!/usr/bin/python

import string

'''A simple interface for a chess application.'''



class Square(object):

	def __init__(self, name, piece = None):
		self.name = name
		self.piece = piece
	
	def __str__(self):
		return 'square {}'.format(self.name)

	def __repr__(self):
		if self.piece:
			return '{:^10}'.format(self.piece)
		else:
			return '{:^10}'.format(self.name)

	def update(self, piece):
		self.piece = piece

class Player(object):
	
	def __init__(self, name=None):
		self.name = name

	def __str__(self):
		return '{}'.format(self.name)

	def __repr__(self):
		return 'Player({})'.format(self.name)

class Piece(object):

	def __init__(self, name=None, owner=None, moves = None):
		self.name = name
		self.owner = owner
		self.moves = moves or {}

	def __str__(self):
		return '{}'.format(self.name)

	def __repr__(self):
	# 	# return 'Piece({},{},{})'.format(self.name, self.owner, self.moves)
		return '{}'.format(self.name)

	def move(self, square):
		pass
		# validate square to move to 
		# check if it's a square reachable by 
		# this piece, that it's an acceptable square.
		# check the state of the square, meaning
		# meaning if there is an existing piece there already
		# and what kind of piece is there. 
		# check who the owner of the piece is.
		# if not reachable:
			# return '{square} is not a valid move'.format(square)
		# if not square.piece:
			# square.piece = self.return_self()
			# self.square.piece = None
			# self.square = square
			# Board.check_state()
		# else:
			# if not square.piece.owner == self.owner
				# self.location = location
			# else:
				# if self.owner == 

	def get_location(self, board):
		
		for row in board:
			for square in row:
				if square.piece == self:
					return square




class Pawn(Piece):

	def __init__(self, name, owner, moves=None):
		super(Pawn, self).__init__(name=name, owner=owner, moves=moves)


	def move(self, location):
		pass


class King(Piece):

	def __init__(self, name, owner, moves=None):
		super(King, self).__init__(name=name, owner=owner, moves=moves)


class Queen(Piece):

	def __init__(self, name, owner, moves=None):
		super(Queen, self).__init__(name=name, owner=owner, moves=moves)


class Rook(Piece):

	def __init__(self, name, owner, moves=None):
		super(Rook, self).__init__(name=name, owner=owner, moves=moves)


class Bishop(Piece):

	def __init__(self, name, owner, moves=None):
		super(Bishop, self).__init__(name=name, owner=owner, moves=moves)


class Knight(Piece):

	def __init__(self, name, owner, moves=None):
		super(Knight, self).__init__(name=name, owner=owner, moves=moves)



class Board(object):

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
			for l in string.lowercase[:8]:
				row.append(Square(name='square{}{}'.format(l, i)))
			self.board.append(row)
		
        
	def __str__(self):
		return '\n'.join(str(square) for square in self.board)
	
	def __repr__(self):
		return 'Board({})'.format(self.board)

	def reset_board(self):
		
		for row in self.board:
			for square in row:
				square.piece = None

		player_1 = Player('Levi')
		player_2 = Player('Fernanda')
		self.__set_pawns(self.board[1], player_1)
		self.__set_pawns(self.board[6], player_2)
		self.__set_other_pieces(self.board[0], player_1)
		self.__set_other_pieces(self.board[7], player_2)


	def __set_pawns(self, row, player):
	
		return [square.update(Pawn('{}{}{}'.format('PAWN', player.name[0].upper(), i), player)) for i, square in enumerate(row)]

	def __set_other_pieces(self, row, player):		

		pieces = 	 [
				Rook('{}{}{}'.format('ROOK', player.name[0].upper(), 0), player),
				Knight('{}{}{}'.format('KNIGHT', player.name[0].upper(), 0), player),
				Bishop('{}{}{}'.format('BISHOP', player.name[0].upper(), 0), player),
				Queen('{}{}'.format('QUEEN', player.name[0].upper()), player),
				King('{}{}'.format('KING', player.name[0].upper()), player),
				Bishop('{}{}{}'.format('BISHOP', player.name[0].upper(), 1), player),
				Knight('{}{}{}'.format('KNIGHT', player.name[0].upper(), 1), player),
				Rook('{}{}{}'.format('ROOK', player.name[0].upper(), 1), player),
				]

		return [square.update(pieces[i]) for i, square in enumerate(row)]

	
	def move_piece(self, player, piece, location):
		
		pass



