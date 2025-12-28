use itertools::{Itertools, Permutations};
use std::{
    collections::{HashMap, HashSet},
    hash::Hash,
    ops::Range,
};

#[derive(Hash, Eq, PartialEq, Debug)]
enum Colour {
    Blue,
    Green,
    Red,
    Yellow,
}

#[derive(Hash, Eq, PartialEq, Debug)]
enum Side {
    One,
    Two,
    Three,
    Four,
    Five,
    Six,
}

#[derive(Hash, Eq, PartialEq, Debug)]
enum Location {
    Top,
    Bottom,
    Front,
    Back,
    Left,
    Right,
}

const VISIBLE_LOCATIONS: [Location; 4] = [
    Location::Top,
    Location::Front,
    Location::Bottom,
    Location::Back,
];

#[derive(Debug)]
struct Orientation {
    mapping: HashMap<Location, Side>,
}

impl Orientation {
    pub fn new(m: HashMap<Location, Side>) -> Orientation {
        Orientation { mapping: m }
    }

    pub fn get_side_at_location(&self, location: &Location) -> &Side {
        &self.mapping[location]
    }
}

#[derive(Debug)]
struct Cube<'a> {
    faces: &'a HashMap<Side, Colour>,
    orientation: &'a Orientation,
}

impl Cube<'_> {
    pub fn new<'a>(faces: &'a HashMap<Side, Colour>, orientation: &'a Orientation) -> Cube<'a> {
        Cube { faces, orientation }
    }

    pub fn get_colour_at_location(&self, location: &Location) -> &Colour {
        &self.faces[self.orientation.get_side_at_location(location)]
    }

    pub fn get_faces(&self) -> &HashMap<Side, Colour> {
        &self.faces
    }

    pub fn get_orientation(&self) -> &Orientation {
        &self.orientation
    }
}

struct Tray<'a> {
    cubes: Vec<Cube<'a>>,
    cube_order: Vec<usize>,
    cube_orientations: &'a Vec<Orientation>,
    cube_faces: &'a Vec<HashMap<Side, Colour>>,
}

impl Tray<'_> {
    pub fn new<'a>(
        cubes: Vec<Cube<'a>>,
        cube_order: Vec<usize>,
        cube_orientations: &'a Vec<Orientation>,
        cube_faces: &'a Vec<HashMap<Side, Colour>>,
    ) -> Tray<'a> {
        Tray {
            cubes,
            cube_order,
            cube_orientations,
            cube_faces,
        }
    }

    pub fn add_cube<'a>(&'a mut self, c: Cube<'a>) {
        self.cubes.push(c);
    }

    pub fn get_cube(&self, i: usize) -> &Cube {
        self.cubes.get(i).unwrap()
    }

    pub fn get_cube_faces(&self) -> &Vec<HashMap<Side, Colour>> {
        self.cube_faces
    }

    pub fn get_cubes(&self) -> &Vec<Cube> {
        &self.cubes
    }

    pub fn get_cubes_order(&self) -> &Vec<usize> {
        &self.cube_order
    }

    pub fn get_cube_orientations(&self) -> &Vec<Orientation> {
        self.cube_orientations
    }

    pub fn get_layout(&self) -> String {
        let cubes_order = self.get_cubes_order();
        let cube_nums: Vec<usize> = cubes_order.iter().map(|x| x + 1).collect();
        let mut layout = String::from(format!("Cube order: {:?}\n", cube_nums));

        for v in VISIBLE_LOCATIONS {
            let colours: Vec<&Colour> = self
                .get_cubes()
                .iter()
                .map(|x| x.get_colour_at_location(&v))
                .collect();
            layout += format!("{:?}: {:?}\n", &v, colours).as_str()
        }

        for (idx, cube_num) in cubes_order.iter().enumerate() {
            let cube = self.get_cube(idx);
            layout += format!("Cube {}:\n", cube_num + 1).as_str();
            // layout += f"Faces {cube.get_faces()}\n"
            for v in VISIBLE_LOCATIONS {
                layout += format!("{:?}: {:?} ", &v, cube.get_colour_at_location(&v)).as_str(); // cube.get_colour_at_location(v).name
                layout +=
                    format!("({:?})\n", cube.get_orientation().get_side_at_location(&v)).as_str();
            }
        }

        return layout;
    }

    pub fn get_num_cubes(&self) -> usize {
        self.cubes.len()
    }

    pub fn is_solved(&self) -> bool {
        // The puzzle is solved when one of each colour is shown alone each side
        // of the tray.

        for visible_location in VISIBLE_LOCATIONS {
            let x: Vec<&Colour> = self
                .get_cubes()
                .iter()
                .map(|x| x.get_colour_at_location(&visible_location))
                .collect();

            let y = HashSet::<&Colour>::from_iter(x);

            if y.len() != self.get_cubes().len() {
                return false;
            }
        }

        true
    }

    pub fn pop_cube(&mut self) {
        self.cubes.pop().unwrap();
    }
}

fn add_next_cube(mut tray: Tray, mut combinations: u32) -> u32 {
    let cube_number = tray.get_cubes_order()[tray.get_num_cubes()];

    let orientations = tray.get_cube_orientations().clone();
    for orientation in orientations {
        let x = &tray.get_cube_faces()[cube_number];
        tray.add_cube(Cube::new(x, orientation));
        combinations += 1;

        if tray.get_num_cubes() == tray.get_cubes_order().len() {
            if tray.is_solved() {
                // print(f"Solved. Checked: {combinations} combinations:")
                println!("{}", tray.get_layout());
                println!("");
            }
        } else {
            combinations = add_next_cube(tray, combinations);
        }

        tray.pop_cube();
    }

    return combinations;
}

fn main() {
    let cube_faces: Vec<HashMap<Side, Colour>> = Vec::from([
        HashMap::from([
            (Side::One, Colour::Green),
            (Side::Two, Colour::Blue),
            (Side::Three, Colour::Red),
            (Side::Four, Colour::Yellow),
            (Side::Five, Colour::Yellow),
            (Side::Six, Colour::Red),
        ]),
        HashMap::from([
            (Side::One, Colour::Yellow),
            (Side::Two, Colour::Yellow),
            (Side::Three, Colour::Green),
            (Side::Four, Colour::Yellow),
            (Side::Five, Colour::Red),
            (Side::Six, Colour::Blue),
        ]),
        HashMap::from([
            (Side::One, Colour::Red),
            (Side::Two, Colour::Red),
            (Side::Three, Colour::Green),
            (Side::Four, Colour::Blue),
            (Side::Five, Colour::Green),
            (Side::Six, Colour::Yellow),
        ]),
        HashMap::from([
            (Side::One, Colour::Red),
            (Side::Two, Colour::Green),
            (Side::Three, Colour::Blue),
            (Side::Four, Colour::Green),
            (Side::Five, Colour::Blue),
            (Side::Six, Colour::Yellow),
        ]),
    ]);

    let cube_orientations: Vec<Orientation> = Vec::from([
        // 5 & 6 on sides
        Orientation::new(HashMap::from([
            (Location::Top, Side::One),
            (Location::Front, Side::Two),
            (Location::Bottom, Side::Three),
            (Location::Back, Side::Four),
            (Location::Right, Side::Five),
            (Location::Left, Side::Six),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Two),
            (Location::Front, Side::Three),
            (Location::Bottom, Side::Four),
            (Location::Back, Side::One),
            (Location::Right, Side::Five),
            (Location::Left, Side::Six),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Three),
            (Location::Front, Side::Four),
            (Location::Bottom, Side::One),
            (Location::Back, Side::Two),
            (Location::Right, Side::Five),
            (Location::Left, Side::Six),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Four),
            (Location::Front, Side::One),
            (Location::Bottom, Side::Two),
            (Location::Back, Side::Three),
            (Location::Right, Side::Five),
            (Location::Left, Side::Six),
        ])),
        //
        Orientation::new(HashMap::from([
            (Location::Top, Side::One),
            (Location::Front, Side::Four),
            (Location::Bottom, Side::Three),
            (Location::Back, Side::Two),
            (Location::Right, Side::Six),
            (Location::Left, Side::Five),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Four),
            (Location::Front, Side::Three),
            (Location::Bottom, Side::Two),
            (Location::Back, Side::One),
            (Location::Right, Side::Six),
            (Location::Left, Side::Five),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Three),
            (Location::Front, Side::Two),
            (Location::Bottom, Side::One),
            (Location::Back, Side::Four),
            (Location::Right, Side::Six),
            (Location::Left, Side::Five),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Two),
            (Location::Front, Side::One),
            (Location::Bottom, Side::Four),
            (Location::Back, Side::Three),
            (Location::Right, Side::Six),
            (Location::Left, Side::Five),
        ])),
        // 1 & 3 on the sides
        Orientation::new(HashMap::from([
            (Location::Top, Side::Six),
            (Location::Front, Side::Two),
            (Location::Bottom, Side::Five),
            (Location::Back, Side::Four),
            (Location::Right, Side::One),
            (Location::Left, Side::Three),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Two),
            (Location::Front, Side::Five),
            (Location::Bottom, Side::Four),
            (Location::Back, Side::Six),
            (Location::Right, Side::One),
            (Location::Left, Side::Three),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Five),
            (Location::Front, Side::Four),
            (Location::Bottom, Side::Six),
            (Location::Back, Side::Two),
            (Location::Right, Side::One),
            (Location::Left, Side::Three),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Four),
            (Location::Front, Side::Six),
            (Location::Bottom, Side::Two),
            (Location::Back, Side::Five),
            (Location::Right, Side::One),
            (Location::Left, Side::Three),
        ])),
        //
        Orientation::new(HashMap::from([
            (Location::Top, Side::Six),
            (Location::Front, Side::Four),
            (Location::Bottom, Side::Five),
            (Location::Back, Side::Two),
            (Location::Right, Side::Three),
            (Location::Left, Side::One),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Four),
            (Location::Front, Side::Five),
            (Location::Bottom, Side::Two),
            (Location::Back, Side::Six),
            (Location::Right, Side::Three),
            (Location::Left, Side::One),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Five),
            (Location::Front, Side::Two),
            (Location::Bottom, Side::Six),
            (Location::Back, Side::Four),
            (Location::Right, Side::Three),
            (Location::Left, Side::One),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Two),
            (Location::Front, Side::Six),
            (Location::Bottom, Side::Four),
            (Location::Back, Side::Five),
            (Location::Right, Side::Three),
            (Location::Left, Side::One),
        ])),
        // 2 & 4 on the sides
        Orientation::new(HashMap::from([
            (Location::Top, Side::One),
            (Location::Front, Side::Six),
            (Location::Bottom, Side::Three),
            (Location::Back, Side::Five),
            (Location::Right, Side::Two),
            (Location::Left, Side::Four),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Six),
            (Location::Front, Side::Three),
            (Location::Bottom, Side::Five),
            (Location::Back, Side::One),
            (Location::Right, Side::Two),
            (Location::Left, Side::Four),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Three),
            (Location::Front, Side::Five),
            (Location::Bottom, Side::One),
            (Location::Back, Side::Six),
            (Location::Right, Side::Two),
            (Location::Left, Side::Four),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Five),
            (Location::Front, Side::One),
            (Location::Bottom, Side::Six),
            (Location::Back, Side::Three),
            (Location::Right, Side::Two),
            (Location::Left, Side::Four),
        ])),
        //
        Orientation::new(HashMap::from([
            (Location::Top, Side::One),
            (Location::Front, Side::Five),
            (Location::Bottom, Side::Three),
            (Location::Back, Side::Six),
            (Location::Right, Side::Four),
            (Location::Left, Side::Two),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Five),
            (Location::Front, Side::Three),
            (Location::Bottom, Side::Six),
            (Location::Back, Side::One),
            (Location::Right, Side::Four),
            (Location::Left, Side::Two),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Three),
            (Location::Front, Side::Six),
            (Location::Bottom, Side::One),
            (Location::Back, Side::Five),
            (Location::Right, Side::Four),
            (Location::Left, Side::Two),
        ])),
        Orientation::new(HashMap::from([
            (Location::Top, Side::Six),
            (Location::Front, Side::One),
            (Location::Bottom, Side::Five),
            (Location::Back, Side::Three),
            (Location::Right, Side::Four),
            (Location::Left, Side::Two),
        ])),
    ]);

    let cube_order_permutations: Vec<Vec<usize>> = (0..cube_faces.len())
        .permutations(cube_faces.len())
        .unique()
        .collect_vec();

    //let b = cube_order_permutations.unique();

    let max_combinations: usize =
        cube_order_permutations.len() * (cube_orientations.len().pow(cube_faces.len() as u32));

    println!("Checking {} combinations...", max_combinations);

    let mut combinations = 0;

    for cube_order in cube_order_permutations {
        let t = Tray::new(Vec::new(), cube_order, &cube_orientations, &cube_faces);
        combinations = add_next_cube(t, combinations);
    }

    println!("Finished. Checked {} combinations", combinations);
}
