use rand::{self, seq::SliceRandom, Rng};
use std::fs::File;
use std::io::{BufRead, BufReader};

use crate::name_generator::NameGenerator;

pub struct EmailGenerator {
    email_domains: Vec<Domain>,
    words: Vec<String>,
    name_generator: NameGenerator,
}

struct Domain {
    name: String,
    weight: u32,
}

impl EmailGenerator {
    pub fn new() -> Result<Self, std::io::Error> {
        let contents = std::fs::read_to_string("./resources/email_domains.txt")
            .unwrap_or_else(|err| panic!("Failed to read email_domains.txt: {}", err));
        let email_domains: Vec<Domain> = contents
            .lines()
            .map(|line| {
                let parts: Vec<&str> = line.split_whitespace().collect();
                Domain {
                    name: parts[0].to_owned(),
                    weight: parts.get(1).and_then(|s| s.parse().ok()).unwrap_or(1),
                }
            })
            .collect();

        let file = File::open("./resources/words.txt").expect("Failed to open words.txt");
        let reader = BufReader::new(file);
        let words: Vec<String> = reader
            .lines()
            .map(|line| line.expect("Failed to read line"))
            .collect();

        let name_generator =
            NameGenerator::new("./resources/first_names.txt", "./resources/last_names.txt")
                .expect("Failed to initialize NameGenerator");

        Ok(Self {
            email_domains,
            words,
            name_generator,
        })
    }

    pub fn generate_email(&self) -> String {
        let mut rng = rand::thread_rng();
        generate_random_email(
            &self.email_domains,
            &mut rng,
            &self.name_generator,
            &self.words,
        )
    }
}

fn generate_random_email(
    email_domains: &[Domain],
    rng: &mut impl Rng,
    name_generator: &NameGenerator,
    words: &[String],
) -> String {
    let domain = email_domains
        .choose_weighted(rng, |item| item.weight)
        .unwrap()
        .name
        .to_owned();

    let variance = rng.gen_range(0..=1);
    let sec1type;
    let sec2type = *["1number", "2number", "4number", ".", "_", "-"]
        .choose(rng)
        .unwrap();
    let sec3type;
    let sec4type = *["1number", "2number", "4number", ""].choose(rng).unwrap();

    if variance == 0 {
        sec1type = *["first_name", "word"].choose(rng).unwrap();
        sec3type = *["last_name", "word"].choose(rng).unwrap();
    } else {
        sec1type = *["last_name", "word"].choose(rng).unwrap();
        sec3type = *["first_name", "word"].choose(rng).unwrap();
    }

    let sec1 = match sec1type {
        "first_name" => name_generator.generate_name().0.to_lowercase(),
        "last_name" => name_generator.generate_name().1.to_lowercase(),
        _ => words.choose(rng).unwrap().to_owned(),
    };

    let sec2 = match sec2type {
        "1number" => rng.gen_range(0..=9).to_string(),
        "2number" => rng.gen_range(10..=99).to_string(),
        "4number" => rng.gen_range(1950..=2024).to_string(),
        _ => sec2type.to_string(),
    };

    let sec3 = match sec3type {
        "first_name" => name_generator.generate_name().0.to_lowercase(),
        "last_name" => name_generator.generate_name().1.to_lowercase(),
        _ => words.choose(rng).unwrap().to_owned(),
    };

    let sec4 = match sec4type {
        "1number" => rng.gen_range(0..=9).to_string(),
        "2number" => rng.gen_range(10..=99).to_string(),
        "4number" => rng.gen_range(1950..=2024).to_string(),
        _ => String::new(),
    };

    format!("{}{}{}{}@{}", sec1, sec2, sec3, sec4, domain)
}
