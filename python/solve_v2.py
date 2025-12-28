#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
from itertools import permutations


class Colour(Enum):
    BLUE = "Blue"
    GREEN = "Green"
    RED = "Red"
    YELLOW = "Yellow"


class Side(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class Location(Enum):
    TOP = "Top"
    BOTTOM = "Bottom"
    FRONT = "Front"
    BACK = "Back"
    LEFT = "Left"
    RIGHT = "Right"


@dataclass
class Orientation:
    mapping: dict[Location, Side]


@dataclass
class Cube:
    faces: dict[Side, Colour]
    orientation: Orientation


@dataclass
class Tray:
    cubes: list[Cube]
    cube_order: tuple[int, ...]

    def get_layout(self) -> str:
        layout = f"Cube order: {[c + 1 for c in self.cube_order]}\n"

        for v in VISIBLE_LOCATIONS:
            layout += f"{v.name}: {[cube.faces[cube.orientation.mapping[v]] for cube in self.cubes]}\n"

        for idx, cube_num in enumerate(self.cube_order):
            cube = self.cubes[idx]
            layout += f"Cube {cube_num + 1}:\n"
            for v in VISIBLE_LOCATIONS:
                layout += (
                    f"{v.name}: {cube.faces[cube.orientation.mapping[v]].name} "
                    f"({cube.orientation.mapping[v].name})\n"
                )

        layout += "\n"

        return layout

    def is_solved(self) -> bool:
        for visible_location in VISIBLE_LOCATIONS:
            if (
                not len(
                    set(
                        [
                            cube.faces[
                                cube.orientation.mapping[visible_location]
                            ]
                            for cube in self.cubes
                        ]
                    )
                )
                == 4
            ):
                return False

        return True


VISIBLE_LOCATIONS = [
    Location.TOP,
    Location.FRONT,
    Location.BOTTOM,
    Location.BACK,
]


CUBES = [
    {
        Side.ONE: Colour.GREEN,
        Side.TWO: Colour.BLUE,
        Side.THREE: Colour.RED,
        Side.FOUR: Colour.YELLOW,
        Side.FIVE: Colour.YELLOW,
        Side.SIX: Colour.RED,
    },
    {
        Side.ONE: Colour.YELLOW,
        Side.TWO: Colour.YELLOW,
        Side.THREE: Colour.GREEN,
        Side.FOUR: Colour.YELLOW,
        Side.FIVE: Colour.RED,
        Side.SIX: Colour.BLUE,
    },
    {
        Side.ONE: Colour.RED,
        Side.TWO: Colour.RED,
        Side.THREE: Colour.GREEN,
        Side.FOUR: Colour.BLUE,
        Side.FIVE: Colour.GREEN,
        Side.SIX: Colour.YELLOW,
    },
    {
        Side.ONE: Colour.RED,
        Side.TWO: Colour.GREEN,
        Side.THREE: Colour.BLUE,
        Side.FOUR: Colour.GREEN,
        Side.FIVE: Colour.BLUE,
        Side.SIX: Colour.YELLOW,
    },
]


CUBE_ORIENTATIONS: list[Orientation] = [
    # 5 & 6 on sides
    Orientation(
        {
            Location.TOP: Side.ONE,
            Location.FRONT: Side.TWO,
            Location.BOTTOM: Side.THREE,
            Location.BACK: Side.FOUR,
            Location.RIGHT: Side.FIVE,
            Location.LEFT: Side.SIX,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.TWO,
            Location.FRONT: Side.THREE,
            Location.BOTTOM: Side.FOUR,
            Location.BACK: Side.ONE,
            Location.RIGHT: Side.FIVE,
            Location.LEFT: Side.SIX,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.THREE,
            Location.FRONT: Side.FOUR,
            Location.BOTTOM: Side.ONE,
            Location.BACK: Side.TWO,
            Location.RIGHT: Side.FIVE,
            Location.LEFT: Side.SIX,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FOUR,
            Location.FRONT: Side.ONE,
            Location.BOTTOM: Side.TWO,
            Location.BACK: Side.THREE,
            Location.RIGHT: Side.FIVE,
            Location.LEFT: Side.SIX,
        }
    ),
    #
    Orientation(
        {
            Location.TOP: Side.ONE,
            Location.FRONT: Side.FOUR,
            Location.BOTTOM: Side.THREE,
            Location.BACK: Side.TWO,
            Location.RIGHT: Side.SIX,
            Location.LEFT: Side.FIVE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FOUR,
            Location.FRONT: Side.THREE,
            Location.BOTTOM: Side.TWO,
            Location.BACK: Side.ONE,
            Location.RIGHT: Side.SIX,
            Location.LEFT: Side.FIVE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.THREE,
            Location.FRONT: Side.TWO,
            Location.BOTTOM: Side.ONE,
            Location.BACK: Side.FOUR,
            Location.RIGHT: Side.SIX,
            Location.LEFT: Side.FIVE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.TWO,
            Location.FRONT: Side.ONE,
            Location.BOTTOM: Side.FOUR,
            Location.BACK: Side.THREE,
            Location.RIGHT: Side.SIX,
            Location.LEFT: Side.FIVE,
        }
    ),
    # 1 & 3 on the sides
    Orientation(
        {
            Location.TOP: Side.SIX,
            Location.FRONT: Side.TWO,
            Location.BOTTOM: Side.FIVE,
            Location.BACK: Side.FOUR,
            Location.RIGHT: Side.ONE,
            Location.LEFT: Side.THREE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.TWO,
            Location.FRONT: Side.FIVE,
            Location.BOTTOM: Side.FOUR,
            Location.BACK: Side.SIX,
            Location.RIGHT: Side.ONE,
            Location.LEFT: Side.THREE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FIVE,
            Location.FRONT: Side.FOUR,
            Location.BOTTOM: Side.SIX,
            Location.BACK: Side.TWO,
            Location.RIGHT: Side.ONE,
            Location.LEFT: Side.THREE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FOUR,
            Location.FRONT: Side.SIX,
            Location.BOTTOM: Side.TWO,
            Location.BACK: Side.FIVE,
            Location.RIGHT: Side.ONE,
            Location.LEFT: Side.THREE,
        }
    ),
    #
    Orientation(
        {
            Location.TOP: Side.SIX,
            Location.FRONT: Side.FOUR,
            Location.BOTTOM: Side.FIVE,
            Location.BACK: Side.TWO,
            Location.RIGHT: Side.THREE,
            Location.LEFT: Side.ONE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FOUR,
            Location.FRONT: Side.FIVE,
            Location.BOTTOM: Side.TWO,
            Location.BACK: Side.SIX,
            Location.RIGHT: Side.THREE,
            Location.LEFT: Side.ONE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FIVE,
            Location.FRONT: Side.TWO,
            Location.BOTTOM: Side.SIX,
            Location.BACK: Side.FOUR,
            Location.RIGHT: Side.THREE,
            Location.LEFT: Side.ONE,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.TWO,
            Location.FRONT: Side.SIX,
            Location.BOTTOM: Side.FOUR,
            Location.BACK: Side.FIVE,
            Location.RIGHT: Side.THREE,
            Location.LEFT: Side.ONE,
        }
    ),
    # 2 & 4 on the sides
    Orientation(
        {
            Location.TOP: Side.ONE,
            Location.FRONT: Side.SIX,
            Location.BOTTOM: Side.THREE,
            Location.BACK: Side.FIVE,
            Location.RIGHT: Side.TWO,
            Location.LEFT: Side.FOUR,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.SIX,
            Location.FRONT: Side.THREE,
            Location.BOTTOM: Side.FIVE,
            Location.BACK: Side.ONE,
            Location.RIGHT: Side.TWO,
            Location.LEFT: Side.FOUR,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.THREE,
            Location.FRONT: Side.FIVE,
            Location.BOTTOM: Side.ONE,
            Location.BACK: Side.SIX,
            Location.RIGHT: Side.TWO,
            Location.LEFT: Side.FOUR,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FIVE,
            Location.FRONT: Side.ONE,
            Location.BOTTOM: Side.SIX,
            Location.BACK: Side.THREE,
            Location.RIGHT: Side.TWO,
            Location.LEFT: Side.FOUR,
        }
    ),
    #
    Orientation(
        {
            Location.TOP: Side.ONE,
            Location.FRONT: Side.FIVE,
            Location.BOTTOM: Side.THREE,
            Location.BACK: Side.SIX,
            Location.RIGHT: Side.FOUR,
            Location.LEFT: Side.TWO,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.FIVE,
            Location.FRONT: Side.THREE,
            Location.BOTTOM: Side.SIX,
            Location.BACK: Side.ONE,
            Location.RIGHT: Side.FOUR,
            Location.LEFT: Side.TWO,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.THREE,
            Location.FRONT: Side.SIX,
            Location.BOTTOM: Side.ONE,
            Location.BACK: Side.FIVE,
            Location.RIGHT: Side.FOUR,
            Location.LEFT: Side.TWO,
        }
    ),
    Orientation(
        {
            Location.TOP: Side.SIX,
            Location.FRONT: Side.ONE,
            Location.BOTTOM: Side.FIVE,
            Location.BACK: Side.THREE,
            Location.RIGHT: Side.FOUR,
            Location.LEFT: Side.TWO,
        }
    ),
]


CUBE_ORDER_PERMUTATIONS = [
    (0, 1, 2, 3),
    (0, 1, 3, 2),
    (0, 2, 1, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
    (0, 3, 2, 1),
    (1, 0, 2, 3),
    (1, 0, 3, 2),
    (1, 2, 0, 3),
    (1, 2, 3, 0),
    (1, 3, 0, 2),
    (1, 3, 2, 0),
    (2, 0, 1, 3),
    (2, 0, 3, 1),
    (2, 1, 0, 3),
    (2, 1, 3, 0),
    (2, 3, 0, 1),
    (2, 3, 1, 0),
    (3, 0, 1, 2),
    (3, 0, 2, 1),
    (3, 1, 0, 2),
    (3, 1, 2, 0),
    (3, 2, 0, 1),
    (3, 2, 1, 0),
]


def add_next_cube(t: Tray, combinations: int) -> int:
    cube_number = t.cube_order[len(t.cubes)]

    for orientation in CUBE_ORIENTATIONS:
        t.cubes.append(
            Cube(
                faces=CUBES[cube_number],
                orientation=orientation,
            )
        )
        combinations += 1

        if len(t.cubes) == 4:
            if t.is_solved():
                # print(f"Solved. Checked: {combinations} combinations:")
                print(t.get_layout())
        else:
            combinations = add_next_cube(t, combinations)

        t.cubes.pop()

    return combinations


combinations = 0
for cube_order in CUBE_ORDER_PERMUTATIONS:
    t = Tray(cubes=[], cube_order=cube_order)
    combinations = add_next_cube(t, combinations)

print(f"Finished. Checked {combinations} combinations")
