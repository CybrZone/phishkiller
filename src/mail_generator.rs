use rand::{self, seq::SliceRandom, Rng};
use std::fs::File;
use std::io::{BufRead, BufReader};

use crate::birthday_generator;
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

    let sec1type = *["first_name", "last_name", "word"].choose(rng).unwrap();
    let sec2type = *["number", "birthday", ".", "_", "-"].choose(rng).unwrap();
    let sec3type = *["first_name", "last_name", "word", ""].choose(rng).unwrap();
    let sec4type = *["number", "birthday", ""].choose(rng).unwrap();

    let mut sec1 = match sec1type {
        "first_name" => name_generator.name().0.to_lowercase(),
        "last_name" => name_generator.name().1.to_lowercase(),
        _ => words.choose(rng).unwrap().to_owned(),
    };

    let mut sec2 = match sec2type {
        "number" => rng.gen_range(0..=999).to_string(),
        "birthday" => birthday_generator::birthday(),
        _ => sec2type.to_string(),
    };

    let mut sec3 = match sec3type {
        "first_name" => name_generator.name().0.to_lowercase(),
        "last_name" => name_generator.name().1.to_lowercase(),
        "word" => words.choose(rng).unwrap().to_owned(),
        _ => sec3type.to_string(),
    };

    let mut sec4 = match sec4type {
        "number" => rng.gen_range(0..=999).to_string(),
        "birthday" => birthday_generator::birthday(),
        _ => sec4type.to_string(),
    };

    if rng.gen_bool(0.5) {
        sec1.get_mut(0..1).unwrap().make_ascii_uppercase();
    }

    if domain == "gmail.com" || domain == "googlemail.com" {
        sec2 = sec2.replace('_', "").replace('-', "");
        sec3 = sec3.replace('_', "").replace('-', "");
        sec4 = sec4.replace('_', "").replace('-', "");
    }

    let mut mail = format!("{}{}{}{}", sec1, sec2, sec3, sec4);

    while !mail.chars().last().unwrap().is_alphanumeric() {
        mail.pop();
    }

    mail.push('@');
    mail.push_str(domain.to_string().as_str());

    mail = mail.replace(' ', "");

    mail
}
