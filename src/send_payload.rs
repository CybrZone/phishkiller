use reqwest::{blocking::Client, StatusCode};
use serde_json::Value;
use std::error::Error;

pub fn send_payload(url: &str, data: &Value) -> Result<StatusCode, Box<dyn Error>> {
    let client = Client::new();
    let response = client.post(url).json(data).send()?;

    Ok(response.status())
}
