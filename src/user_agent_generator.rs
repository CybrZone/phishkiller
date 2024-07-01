use rand::seq::SliceRandom;
use std::io::Error;

pub struct UserAgentGenerator {
    user_agents: Vec<String>,
}

impl UserAgentGenerator {
    pub fn new() -> Result<Self, Error> {
        let user_agents = std::fs::read_to_string("./resources/user_agents.txt")?;
        let user_agents: Vec<String> = user_agents.lines().map(|line| line.to_string()).collect();
        Ok(Self { user_agents })
    }

    pub fn user_agent(&self) -> String {
        let mut rng = rand::thread_rng();
        let ua = self
            .user_agents
            .choose(&mut rng)
            .expect("No user agents available");
        String::from(ua)
    }
}
