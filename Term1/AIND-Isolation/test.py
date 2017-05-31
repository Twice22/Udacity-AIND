        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self), (-1, -1)
        
        best_pos = (-1,-1)
        best_score = float("-inf") if maximizing_player else float("inf")
        
        for move in game.get_legal_moves():
            new_game = game.forecast_move(move)
            score, pos = self.minimax(new_game, depth - 1, not maximizing_player, strr+strr)

            if (maximizing_player and score > best_score) or ((not maximizing_player) and score < best_score):
                best_pos = new_game.get_player_location(self)
                best_score = score

        return best_score, best_pos


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

# good heurestic
def heurestic7(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_moves = game.get_legal_moves(game.get_opponent(player))

    return float(1/(len(opp_moves)+1))

# good heurestic
def heurestic4(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    intersection = set(my_moves).intersection(opp_moves)

    authorized_moves = len(my_moves) - len(intersection)

    return float(len(my_moves) + len(intersection) - len(opp_moves))

def heurestic3(game, player):

    def longestPath(game, player):
        maxPathLength = 0;
        my_moves = game.get_legal_moves(player)
        opp_moves = game.get_legal_moves(game.get_opponent(player))

        for move in my_moves:
            new_game = game.forecast_move(move)
            pathLength = longestPath(new_game, player) + 1
            if pathLength > maxPathLength:
                maxPathLength = pathLength
            if move in opp_moves:
                maxPathLength += 1
        return maxPathLength

    if (len(game.get_blank_spaces()) <= game.width*game.height/4):
        my_longestPath = longestPath(game, player)
        #opp_longestPath = longestPath(game, game.get_opponent(player))

        return float(my_longestPath) # - opp_longestPath)
    else:
        return heurestic1(game, player)


def heurestic1(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(my_moves - opp_moves)