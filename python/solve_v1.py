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

    def get_side_at_location(self, location: Location) -> Side:
        return self.mapping[location]


@dataclass
class Cube:
    faces: dict[Side, Colour]
    orientation: Orientation

    def get_colour_at_location(self, location: Location) -> Colour:
        return self.faces[self.orientation.get_side_at_location(location)]

    def get_faces(self) -> dict[Side, Colour]:
        return self.faces

    def get_orientation(self) -> Orientation:
        return self.orientation


@dataclass
class Tray:
    cubes: list[Cube]
    cube_order: tuple[int, ...]

    def add_cube(self, c: Cube) -> None:
        self.cubes.append(c)

    def get_cubes(self) -> list[Cube]:
        return self.cubes

    def get_cubes_order(self) -> tuple[int, ...]:
        return self.cube_order

    def get_layout(self) -> str:
        cubes_order = self.get_cubes_order()
        cubes = self.get_cubes()
        layout = f"Cube order: {[c + 1 for c in cubes_order]}\n"

        for v in visible_locations:
            layout += f"{v.name}: {[cube.get_colour_at_location(v) for cube in self.get_cubes()]}\n"

        for idx, cube_num in enumerate(cubes_order):
            cube = cubes[idx]
            layout += f"Cube {cube_num + 1}:\n"
            # layout += f"Faces {cube.get_faces()}\n"
            for v in visible_locations:
                layout += (
                    f"{v.name}: {cube.get_colour_at_location(v).name} "
                    f"({cube.get_orientation().get_side_at_location(v).name})\n"
                )

        return layout

    def get_num_cubes(self) -> int:
        return len(self.cubes)

    def is_solved(self) -> bool:
        """
        The puzzle is solved when one of each colour is shown alone each side
        of the tray.
        """

        for visible_location in visible_locations:
            if not len(
                set(
                    [
                        cube.get_colour_at_location(visible_location)
                        for cube in self.get_cubes()
                    ]
                )
            ) == len(self.get_cubes()):
                return False

        return True

    def pop_cube(self) -> Cube:
        return self.cubes.pop()


visible_locations = [
    Location.TOP,
    Location.FRONT,
    Location.BOTTOM,
    Location.BACK,
]


cubes = [
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


cube_orientations: list[Orientation] = [
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


cube_order_permutations = [
    permutation for permutation in permutations(range(len(cubes)), len(cubes))
]


def add_next_cube(t: Tray, checked_combinations: int, winning_combinations: int) -> tuple[int, int]:
    cube_number = t.get_cubes_order()[t.get_num_cubes()]

    for orientation in cube_orientations:
        t.add_cube(
            Cube(
                faces=cubes[cube_number],
                orientation=orientation,
            )
        )
        checked_combinations += 1

        if t.get_num_cubes() == len(t.get_cubes_order()):
            if t.is_solved():
                winning_combinations += 1
                print(
                    f"{winning_combinations} winning combinations found "
                    f"from {checked_combinations} checked combinations"
                )
                # print(t.get_layout())
                # print("")
        else:
            checked_combinations, winning_combinations = add_next_cube(t, checked_combinations, winning_combinations)

        t.pop_cube()

    return checked_combinations, winning_combinations


max_combinations = len(cube_order_permutations) * (
    len(cube_orientations) ** len(cubes)
)
print(f"Checking {max_combinations} combinations...")

checked_combinations = 0
winning_combinations = 0

for cube_order in cube_order_permutations:
    t = Tray(cubes=[], cube_order=cube_order)
    checked_combinations, winning_combinations = add_next_cube(
        t, checked_combinations, winning_combinations
        )

print(
    f"Finished. Checked {checked_combinations} combinations, found "
    f"{winning_combinations} winning combinations"
)
