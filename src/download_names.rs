use std::collections::HashSet;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use zip::ZipArchive;

#[tokio::main]
async fn downloaded_first_name_file() -> Result<(), Box<dyn std::error::Error>> {
    println!("Downloading first name file");
    let url = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip";
    let response = reqwest::get(url).await?;
    let names_dir = "./first_names";

    if Path::new(names_dir).exists() {
        fs::remove_dir_all(names_dir)?;
    }

    fs::create_dir_all(names_dir)?;

    let zip_path = Path::new(names_dir).join("first_names.zip");
    let mut zip_file = File::create(&zip_path)?;

    let content = response.bytes().await?;
    zip_file.write_all(&content)?;

    let file = File::open(&zip_path)?;
    let mut archive = ZipArchive::new(BufReader::new(file))?;
    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        let out_path = Path::new(names_dir).join(file.name());

        if file.name().ends_with('/') {
            fs::create_dir_all(&out_path)?;
        } else {
            if let Some(p) = out_path.parent() {
                if !p.exists() {
                    fs::create_dir_all(&p)?;
                }
            }
            let mut outfile = File::create(&out_path)?;
            io::copy(&mut file, &mut outfile)?;
        }
    }

    fs::remove_file(&zip_path)?;

    let readme_path = Path::new(names_dir).join("StateReadMe.pdf");
    if readme_path.exists() {
        fs::remove_file(readme_path)?;
    }

    Ok(())
}

#[tokio::main]
async fn downloaded_last_name_file() -> Result<(), Box<dyn std::error::Error>> {
    println!("Downloading last name file");
    let url = "https://www2.census.gov/topics/genealogy/2010surnames/names.zip";
    let response = reqwest::get(url).await?;
    let names_dir = "./last_names";

    if Path::new(names_dir).exists() {
        fs::remove_dir_all(names_dir)?;
    }

    fs::create_dir_all(names_dir)?;

    let zip_path = Path::new(names_dir).join("last_names.zip");
    let mut zip_file = File::create(&zip_path)?;

    let content = response.bytes().await?;
    zip_file.write_all(&content)?;

    let file = File::open(&zip_path)?;
    let mut archive = ZipArchive::new(BufReader::new(file))?;
    for i in 0..archive.len() {
        let mut file = archive.by_index(i)?;
        let out_path = Path::new(names_dir).join(file.name());

        if file.name().ends_with('/') {
            fs::create_dir_all(&out_path)?;
        } else {
            if let Some(p) = out_path.parent() {
                if !p.exists() {
                    fs::create_dir_all(&p)?;
                }
            }
            let mut outfile = File::create(&out_path)?;
            io::copy(&mut file, &mut outfile)?;
        }
    }

    fs::remove_file(&zip_path)?;

    let readme_path = Path::new(names_dir).join("Names_2010Census.xlsx");
    if readme_path.exists() {
        fs::remove_file(readme_path)?;
    }

    Ok(())
}

fn create_unique_first_names_file() -> io::Result<()> {
    println!("Creating unique first names file");
    let write_dir = Path::new("./resources");
    let read_dir = Path::new("./first_names");
    fs::create_dir_all(write_dir)?;
    let mut unique_names = HashSet::new();

    for entry in fs::read_dir(read_dir)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_file() {
            let file = File::open(&path)?;
            let reader = BufReader::new(file);

            for line in reader.lines() {
                let line = line?;
                let parts: Vec<&str> = line.split(',').collect();
                if parts.len() > 3 {
                    unique_names.insert(parts[3].to_string());
                }
            }
        }
    }

    let mut output_file = File::create(write_dir.join("first_names.txt"))?;
    for name in unique_names {
        writeln!(output_file, "{}", name)?;
    }

    if Path::new(read_dir).exists() {
        fs::remove_dir_all(read_dir)?;
    }

    Ok(())
}

fn create_unique_last_names_file() -> io::Result<()> {
    println!("Formatting last names file");
    let read_dir = Path::new("./last_names");
    let read_file = Path::new("Names_2010Census.csv");
    let read_file = read_dir.join(read_file);
    let write_dir = Path::new("./resources");
    let write_file = Path::new(write_dir).join("last_names.txt");

    let file = File::open(&read_file)?;
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().collect::<Result<_, _>>()?;

    let mut output_file = File::create(write_file)?;
    let mut unique_last_names = HashSet::new();
    for line in lines[1..lines.len() - 1].iter() {
        let name = line.split(',').next().unwrap();
        let capitalized_name = format!(
            "{}{}",
            name.chars().next().unwrap().to_uppercase(),
            &name[1..].to_lowercase()
        );
        unique_last_names.insert(capitalized_name);
    }

    for name in unique_last_names {
        writeln!(output_file, "{}", name)?;
    }

    if Path::new(read_dir).exists() {
        fs::remove_dir_all(read_dir)?;
    }

    Ok(())
}

pub fn names() {
    downloaded_first_name_file().expect("Error downloading name file");
    create_unique_first_names_file().expect("Error creating unique names file");
    downloaded_last_name_file().expect("Error downloading last name file");
    create_unique_last_names_file().expect("Error creating unique last names file");
}
