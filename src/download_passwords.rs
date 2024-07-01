use rand::seq::SliceRandom;
use rand::thread_rng;
use reqwest::Url;
use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};

#[tokio::main]
async fn download_password_file() -> Result<(), Box<dyn std::error::Error>> {
    println!("Downloading password file");
    let url = Url::parse(
        "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
    )?;
    let response = reqwest::get(url).await?;

    let password_file_path = "./resources/passwords.txt";
    let mut password_file = File::create(&password_file_path)?;

    let content = response.bytes().await?;
    password_file.write_all(&content)?;

    Ok(())
}

fn shuffle_passwords() -> io::Result<()> {
    let password_file_path = "./resources/passwords.txt";

    let file = File::open(&password_file_path)?;
    let reader = BufReader::new(file);
    let mut passwords: HashSet<String> = reader.lines().filter_map(io::Result::ok).collect();

    let mut passwords_vec: Vec<_> = passwords.drain().collect();
    let mut rng = thread_rng();
    passwords_vec.shuffle(&mut rng);

    let mut file = File::create(&password_file_path)?;
    for password in passwords_vec {
        writeln!(file, "{}", password)?;
    }

    Ok(())
}

pub fn passwords() {
    download_password_file().expect("Error downloading password file");
    shuffle_passwords().expect("Error shuffling password file");
}
