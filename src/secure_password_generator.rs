use rand::rngs::OsRng;
use rand::Rng;
use rand::RngCore;

pub fn generate_password() -> String {
    let char_pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_.";

    let mut rng = OsRng;

    let passphrase_length = rng.gen_range(14..38);
    let mut passphrase = String::new();
    for _ in 0..passphrase_length {
        let index = rng.next_u32() as usize % char_pool.len();
        passphrase.push(char_pool.chars().nth(index).unwrap());
    }

    passphrase
}
