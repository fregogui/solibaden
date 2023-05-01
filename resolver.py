from maps import load_map
from playground import MapT, Round


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
