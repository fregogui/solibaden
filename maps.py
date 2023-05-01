import csv

from playground import Coordinate, MapT, Row


def load_map(file_path: str) -> MapT:
    _map = {}
    with open(file_path) as csvfile:
        row_count = 0
        for row in csv.reader(csvfile, delimiter=","):
            if not row or row[0] == "X":
                continue
            column_count = 0
            for cell in row[1:]:
                is_valid = cell != "0"
                ball = cell == "B"
                coordinate = Coordinate(x=column_count, y=row_count)
                _map[coordinate] = Row(is_valid=is_valid, ball=ball, pos=coordinate)
                column_count += 1
            row_count += 1
    return _map
