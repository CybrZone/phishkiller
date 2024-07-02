use rand::seq::SliceRandom;
use rand::Rng;

fn is_leap_year(year: i32) -> bool {
    (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
}

fn generate_birthday() -> (String, String, String) {
    let mut rng = rand::thread_rng();
    let year = rng.gen_range(1950..2025);
    let month = rng.gen_range(1..13);
    let day = match month {
        2 => {
            if is_leap_year(year) {
                rng.gen_range(1..30)
            } else {
                rng.gen_range(1..29)
            }
        }
        4 | 6 | 9 | 11 => rng.gen_range(1..31),
        _ => rng.gen_range(1..32),
    };

    (day.to_string(), month.to_string(), year.to_string())
}

pub fn birthday() -> String {
    let patterns = [
        "dd-mm-yyyy",
        "dd-mm-yy",
        "yyyy-mm-dd",
        "yy-mm-dd",
        "mm-dd-yyyy",
        "mm-dd-yy",
        "mm-yyyy",
        "dd-mm",
        "mm-dd",
        "mm-yy",
        "yyyy",
        "yy",
    ];
    let pattern = *patterns.choose(&mut rand::thread_rng()).unwrap();
    let (day, month, year) = generate_birthday();

    match pattern {
        "dd-mm-yyyy" => format!("{:02}{:02}{}", day, month, year),
        "dd-mm-yy" => format!("{:02}{:02}{}", day, month, &year[2..]),
        "yyyy-mm-dd" => format!("{}{:02}{:02}", year, month, day),
        "yy-mm-dd" => format!("{:02}{:02}{}", &year[2..], month, day),
        "mm-dd-yyyy" => format!("{:02}{:02}{}", month, day, year),
        "mm-dd-yy" => format!("{:02}{:02}{}", month, day, &year[2..]),
        "mm-yyyy" => format!("{:02}{}", month, year),
        "dd-mm" => format!("{:02}{:02}", day, month),
        "mm-dd" => format!("{:02}{:02}", month, day),
        "mm-yy" => format!("{:02}{}", month, &year[2..]),
        "yyyy" => format!("{}", year),
        "yy" => format!("{}", &year[2..]),
        _ => unreachable!(),
    }
}
