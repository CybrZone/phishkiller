use crate::create_config;
use crate::download_names;
use crate::download_passwords;
use crate::download_user_agents;

pub fn first_launch() {
    download_names::names();
    download_user_agents::user_agents();
    download_passwords::passwords();
    create_config::create_config_file();
}
