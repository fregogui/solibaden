import csv
import hashlib
import random
import uuid
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import Any


@dataclass
class Coordinate:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


class DirectionEnum(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


@dataclass
class Row:
    is_valid: bool
    ball: bool
    pos: Coordinate


MapT = dict[Coordinate, Row]


@dataclass
class Move:
    pos: Coordinate
    direction: DirectionEnum

    def __hash__(self):
        return hash((hash(self.pos), hash(self.direction)))

    def __str__(self):
        return f"Move from (x,y)=({self.pos.x}, {self.pos.y}) to {self.direction}"


def bool_str(value: Any) -> str:
    return "1" if value else "0"


def get_map_id(_map: MapT) -> str:
    return hashlib.sha256(
        "-".join(
            [
                ":".join(
                    [
                        bool_str(row.ball),
                        bool_str(row.is_valid),
                        str(row.pos.x),
                        str(row.pos.y),
                    ]
                )
                for row in sorted(_map.values(), key=lambda row: (row.pos.x, row.pos.y))
            ]
        ).encode("utf-8")
    ).hexdigest()


@dataclass
class Round:
    map: MapT

    @cached_property
    def possible_moves(self) -> set[Move]:
        moves = set()
        for pos, row in self.map.items():
            if not row.is_valid or not row.ball:
                continue
            for direction in DirectionEnum:
                jumped_position, target_position = self.get_move_position(
                    pos, direction
                )
                target_row = self.map.get(target_position)
                jumped_row = self.map.get(jumped_position)
                if target_row is None or jumped_row is None:
                    continue
                if (
                    target_row.is_valid is True
                    and jumped_row.is_valid is True
                    and target_row.ball is False
                    and jumped_row.ball is True
                ):
                    moves.add(Move(pos=pos, direction=direction))
        return moves

    @staticmethod
    def get_move_position(
        origin: Coordinate, direction: DirectionEnum
    ) -> tuple[Coordinate, Coordinate]:
        jumped_position = None
        target_position = None
        if direction is DirectionEnum.UP:
            target_position = Coordinate(x=origin.x, y=origin.y - 2)
            jumped_position = Coordinate(x=origin.x, y=origin.y - 1)
        if direction is DirectionEnum.DOWN:
            target_position = Coordinate(x=origin.x, y=origin.y + 2)
            jumped_position = Coordinate(x=origin.x, y=origin.y + 1)
        if direction is DirectionEnum.LEFT:
            target_position = Coordinate(x=origin.x - 2, y=origin.y)
            jumped_position = Coordinate(x=origin.x - 1, y=origin.y)
        if direction is DirectionEnum.RIGHT:
            target_position = Coordinate(x=origin.x + 2, y=origin.y)
            jumped_position = Coordinate(x=origin.x + 1, y=origin.y)
        assert target_position is not None and jumped_position is not None
        return jumped_position, target_position

    def move(self, move: Move) -> MapT:
        if move not in self.possible_moves:
            raise ValueError
        new_map = {}
        jumped_position, target_position = self.get_move_position(
            move.pos, move.direction
        )
        for pos, row in self.map.items():
            if pos == jumped_position:
                new_map[pos] = Row(is_valid=True, ball=False, pos=pos)
            elif pos == target_position:
                new_map[pos] = Row(is_valid=True, ball=True, pos=pos)
            elif pos == move.pos:
                new_map[pos] = Row(is_valid=True, ball=False, pos=pos)
            else:
                new_map[pos] = Row(is_valid=row.is_valid, ball=row.ball, pos=row.pos)
        return new_map

    @property
    def is_blocked(self) -> bool:
        return len(self.possible_moves) == 0

    def random_move(self, excluded_moves: set[Move] | None = None) -> Move | None:
        if excluded_moves:
            possible_moves = list(self.possible_moves - excluded_moves)
        else:
            possible_moves = list(self.possible_moves)
        if not self.is_blocked and possible_moves:
            return random.choice(possible_moves)

    @cached_property
    def ball_count(self) -> int:
        ball_count = 0
        for row in self.map.values():
            if row.ball:
                ball_count += 1
        return ball_count

    @cached_property
    def id(self):
        return get_map_id(self.map)

    def __str__(self):
        return f"Map with id {self.id}: {self.ball_count} balls and {len(self.possible_moves)} possible moves"

