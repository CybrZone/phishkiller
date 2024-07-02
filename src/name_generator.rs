use rand::Rng;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

pub struct NameGenerator {
    first_names: Vec<String>,
    last_names: Vec<String>,
}

impl NameGenerator {
    pub fn new(first_names_file: &str, last_names_file: &str) -> io::Result<Self> {
        let first_names = Self::read_names_from_file(first_names_file)?;
        let last_names = Self::read_names_from_file(last_names_file)?;

        Ok(Self {
            first_names,
            last_names,
        })
    }

    fn read_names_from_file(filename: &str) -> io::Result<Vec<String>> {
        let path = Path::new(filename);
        let file = File::open(path)?;
        let reader = io::BufReader::new(file);

        let mut names = Vec::new();
        for line in reader.lines() {
            let line = line?;
            names.push(line);
        }

        Ok(names)
    }

    pub fn generate_name(&self) -> (String, String) {
        let mut rng = rand::thread_rng();
        let first_name = rng.gen_range(0..self.first_names.len());
        let last_name = rng.gen_range(0..self.last_names.len());

        (
            self.first_names[first_name].clone(),
            self.last_names[last_name].clone(),
        )
    }

    pub fn name(&self) -> (String, String) {
        let mut rng = rand::thread_rng();
        let variant = rng.gen_range(0..3);
        let (first_name, last_name) = self.generate_name();
        let names = match variant {
            0 => (first_name.clone(), last_name.clone()),
            1 => (first_name.clone()[..1].to_string(), last_name.clone()),
            2 => (first_name.clone(), last_name.clone()[..1].to_string()),
            _ => unreachable!(),
        };

        if rand::random() {
            (names.0, names.1)
        } else {
            (names.1, names.0)
        }
    }
}
