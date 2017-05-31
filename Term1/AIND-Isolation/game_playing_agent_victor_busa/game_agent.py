"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
from math import fabs, sqrt

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

# my_moves - #opp_moves heuristic. this heuristic is reused in other
# heuristic. Because one usefull idea is to have a heuristic that changes
# overtime accordingly to the state of the board.
def id_improved(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(my_moves - opp_moves)

# the idea is to choose the longest path possible if nobody moves
# in the board. has the function is recursive and can take times to
# execute and that is doesn't make sense to search for the longestpath
# at the beginning. I decided to switch to longestPath function once
# the number of blank spaces remaining is less then 1/4 of the number
# of spaces in the game.
def longest(game, player):

    def longestPath(game, player):
        maxPathLength = 0;
        my_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))

        for move in my_moves:
            new_game = game.forecast_move(move)
            pathLength = longestPath(new_game, player) + 1
            if pathLength > maxPathLength:
                maxPathLength = pathLength
        return maxPathLength

    if (len(game.get_blank_spaces()) <= game.width*game.height/4):
        my_longestPath = longestPath(game, player)

        return float(my_longestPath)
    else:
        return heurestic1(game, player)

# advantage with epsilon = 1, the fact that I will prefer to be at a distance
# (1,1) from my opponent because I might block one of the move of my opponent 
# in the next move and the opponent cannot attack me. Also, when I cannot be
# at a distance of (1,1) of my opponent then epsilon = 0 and so the behaviour
# of my heuristic is exactly #my_moves - #opp_moves.
def tweaked_id_improved(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_loc = game.get_player_location(player)
    opp_loc = game.get_player_location(game.get_opponent(player))
    dist_player = tuple(map(lambda x, y: fabs(x - y), my_loc, opp_loc))
    epsilon = 3 if dist_player == (1,1) else 0

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(my_moves - opp_moves + epsilon)


# idea : change heuristic over time. At first we use id_improved heuristic
# after a certain number of square are already filled we'll switch to the
# open heuristic (#my_moves)
def switching(game, player):
    my_moves = game.get_legal_moves(player)

    if (len(game.get_blank_spaces()) <= game.width*game.height/4):
        return float(len(my_moves))
    else:
        return id_improved(game, player)

# attacking heuristic. The principle of this heuristic is to maximize the reverse
# of the number of moves of my opponent. hence the less moves my opponent can make
# the better it is for me, because the less my opponent is likely to move next.
# I add tweak. My player will prefer to be closer to the enemy and to chose among tie
# the one with higher number of my moves
def attacking(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # add epsilon if closer to enemy
    my_loc = game.get_player_location(player)
    opp_loc = game.get_player_location(game.get_opponent(player))
    epsilon2 = sqrt((my_loc[0]-opp_loc[0])*(my_loc[0]-opp_loc[0]) + (opp_loc[1]-opp_loc[1])*(opp_loc[1]-opp_loc[1]))/9

    # choosing among tie the one with higher number of my moves
    epsilon = len(game.get_legal_moves(player))/9

    return float(9/(len(opp_moves)+1) + epsilon + epsilon2)

# another heuristic
def tweaked2_id_improved(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    intersection = set(my_moves).intersection(opp_moves)

    authorized_moves = len(my_moves) - len(intersection)

    return float(len(my_moves) + len(intersection) - len(opp_moves))

# closer to center heuristic
def closer_to_center(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # idea : norm_dist_to_center is a normalised ( 0 < dist < 1) distance
    # the closer to the center we are the closer to 0 dist_current_pos_to_center is
    # and hence the closer to 1 the norm_dist_to_center is. hence I favor by less than
    # 1 point a move that go closer to the center. Why less than 1 ?
    # Because as the other computation (my_moves - opp_moves) are interger, norm_dsit_to_center
    # will only have influence for tie decision.
    my_loc = game.get_player_location(player)
    dist_to_center = sqrt((game.width/2)**2+(game.height/2)**2)
    dist_current_pos_to_center = sqrt( (game.width/2 - my_loc[0] )**2 + (game.height/2 - my_loc[1])**2 )
    norm_dist_to_center = dist_to_center/(dist_current_pos_to_center + dist_to_center)

    return float((my_moves - opp_moves)/(my_moves + opp_moves) + norm_dist_to_center)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    return attacking(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        mid = int(len(legal_moves)/2)
        best_pos = legal_moves[mid] if legal_moves else (-1, -1)
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                i = 0
                while True:
                    best_score, best_pos = getattr(self, self.method)(game, i)
                    i += 1
            else:
                best_score, best_pos = getattr(self, self.method)(game, 1)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_pos

        # Return the best move from the last completed search iteration
        return best_pos

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)
        
        best_pos = (-1,-1)
        best_score = float("-inf") if maximizing_player else float("inf")
        
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            score, pos = self.minimax(new_game, depth - 1, not maximizing_player)

            if (maximizing_player and score > best_score) or ((not maximizing_player) and score < best_score):
                best_pos = new_game.get_player_location(self)
                best_score = score

        return best_score, best_pos


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        if depth == 0:
            return self.score(game, self), (-1, -1)

        best_pos = (-1,-1)
        best_score = float("-inf") if maximizing_player else float("inf")

        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            score, pos = self.alphabeta(new_game, depth - 1, alpha, beta, not maximizing_player)

            if (maximizing_player and score > best_score):
                best_pos = new_game.get_player_location(self)
                best_score = score

                if best_score >= beta:
                    return best_score, best_pos

                alpha = max(alpha, best_score)

            elif ((not maximizing_player) and score < best_score):
                best_pos = new_game.get_player_location(self)
                best_score = score

                if best_score <= alpha:
                    return best_score, best_pos

                beta = min(alpha, best_score)

        return best_score, best_pos
