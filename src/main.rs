use rayon::prelude::*;
use std::fs;
use std::path::Path;
use std::process::exit;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

mod download_names;
mod download_passwords;
mod download_user_agents;
mod first_launch;

mod mail_generator;
mod name_generator;
mod password_generator;
mod secure_password_generator;
mod user_agent_generator;

mod send_payload;

fn main() {
    if !Path::new("./resources/first_names.txt").exists()
        || !Path::new("./resources/last_names.txt").exists()
        || !Path::new("./resources/user_agents.txt").exists()
        || !Path::new("./resources/passwords.txt").exists()
    {
        println!("Important files not found, expecting this to be a first launch, downloading...");
        first_launch::first_launch();
    } else {
        if !Path::new("./config.json").exists() {
            println!("Config file not found, creating...");
            exit(0);
        }
        if !Path::new("./resources/email_domains.txt").exists() {
            println!("Email domains file not found, please download it and place it in the resources folder");
            exit(0);
        }
        if !Path::new("./resources/words.txt").exists() {
            println!(
                "Words file not found, please download it and place it in the resources folder"
            );
            exit(0);
        }
        println!("All files found");

        let config_content =
            fs::read_to_string("./config.json").expect("Failed to read config file");
        let config: serde_json::Value =
            serde_json::from_str(&config_content).expect("Failed to parse config file");

        let url = config["url"].as_str().expect("Invalid URL in config");
        let sleep_timer_ms = config["sleep_timer_ms"]
            .as_u64()
            .expect("Invalid sleep_timer_ms in config");

        let user = config["user"]
            .as_str()
            .expect("Invalid user reference in config");

        let password = config["password"]
            .as_str()
            .expect("Invalid password reference in config");

        let email_generator = Arc::new(Mutex::new(
            mail_generator::EmailGenerator::new().expect("Failed to initialize EmailGenerator"),
        ));
        let password_generator = Arc::new(Mutex::new(
            password_generator::PasswordGenerator::new()
                .expect("Failed to initialize PasswordGenerator"),
        ));
        let user_agent_generator = Arc::new(Mutex::new(
            user_agent_generator::UserAgentGenerator::new()
                .expect("Failed to initialize UserAgentGenerator"),
        ));

        (0..10).into_par_iter().for_each(|_| {
            let email_generator = Arc::clone(&email_generator);
            let password_generator = Arc::clone(&password_generator);
            let user_agent_generator = Arc::clone(&user_agent_generator);

            loop {
                let mail = email_generator.lock().unwrap().generate_email();
                let pw = password_generator.lock().unwrap().password();
                let ua = user_agent_generator.lock().unwrap().user_agent();

                let data = serde_json::json!({
                    user: mail,
                    password: pw,
                    "user_agent": ua
                });

                match send_payload::send_payload(url, &data) {
                    Ok(response) => println!("{}, {}:{}", response, mail, pw),
                    Err(e) => println!("Failed to send payload: {:?}", e),
                }

                thread::sleep(Duration::from_millis(sleep_timer_ms));
            }
        });
    }
}
