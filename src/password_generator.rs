use crate::secure_password_generator;
use rand::seq::SliceRandom;
use rand::Rng;

pub struct PasswordGenerator {
    passwords: Vec<String>,
}

impl PasswordGenerator {
    pub fn new() -> Result<Self, std::io::Error> {
        let passwords = std::fs::read_to_string("./resources/passwords.txt")?;
        let passwords: Vec<String> = passwords.lines().map(|line| line.to_string()).collect();
        Ok(Self { passwords })
    }

    pub fn password(&self) -> String {
        let mut rng = rand::thread_rng();
        let num = rng.gen_range(1..=16);

        if num <= 15 {
            self.passwords
                .choose(&mut rng)
                .map_or_else(|| "".to_string(), |password| password.clone())
        } else {
            secure_password_generator::generate_password()
        }
    }
}
