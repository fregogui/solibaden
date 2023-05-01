import math
import random

from maps import load_map
from playground import MapT, Round, get_map_id


def naive_resolver(original_map: MapT) -> int:
    current_round = Round(map=original_map)
    print(current_round)

    moves = []
    while current_round.is_blocked is False:
        move = current_round.random_move
        print(move)
        moves.append(move)
        _map = current_round.move(move)
        current_round = Round(map=_map)
        print(current_round)
    print(f"Finished with {current_round.ball_count}")
    return current_round.ball_count


class BlockedException(Exception):
    pass


def random_resolver(original_map: MapT, max_iteration: int):
    starting_round = Round(map=original_map)
    current_round = starting_round
    best_result = math.inf
    iteration = 0
    round_by_id = {starting_round.id: starting_round}
    moves = None
    while best_result != 1 or iteration > max_iteration:
        ball_count, round_by_id, moves = _resolver(current_round, round_by_id)
        iteration += 1
        best_result = min(ball_count, best_result)
        if iteration % 1000:
            print(f"Iteration {iteration}, best result {best_result}")
    print(moves)
    return moves


def _resolver(current_round: Round, round_by_id: dict[str, Round]):
    moves = []
    while current_round.is_blocked is False:
        move = current_round.random_move()
        moves.append(move)
        if move is None:
            return current_round.ball_count, round_by_id

        _map = current_round.move(move)
        map_id = get_map_id(_map=_map)
        current_round = round_by_id.get(map_id)
        if current_round is None:
            current_round = Round(map=_map)
            round_by_id[map_id] = current_round

    return current_round.ball_count, round_by_id, moves
