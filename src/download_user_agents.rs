use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};
use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader, BufWriter, Write};

#[derive(Debug, Deserialize, Serialize)]
struct BrowserData {
    useragent: String,
    percent: f64,
    #[serde(rename = "type")]
    browser_type: String,
    system: String,
    browser: String,
    version: f64,
    os: String,
}

fn download_and_convert_user_agents() -> Result<(), Box<dyn Error>> {
    println!("Downloading user agents");
    let url = "https://raw.githubusercontent.com/fake-useragent/fake-useragent/main/src/fake_useragent/data/browsers.json";

    let client = Client::new();
    let response = client.get(url).send()?;

    let file = File::create("./resources/user_agents.txt")?;
    let mut writer = BufWriter::new(file);

    for line in BufReader::new(response).lines() {
        let line = line?;
        let browser_data: BrowserData = serde_json::from_str(&line)?;
        writeln!(writer, "{}", browser_data.useragent)?;
    }

    println!("User agents saved");

    Ok(())
}

pub fn user_agents() {
    if let Err(err) = download_and_convert_user_agents() {
        eprintln!("Failed to download and convert user agents: {}", err);
    }
}
