import json
import numpy as np
import os
import pandas as pd
from pathlib import Path
from random import choice, choices

DIR_PATH = Path(__file__).parent
np.random.seed(42)


def random_pic():
    """Return a random picture path from the sample_data/pics directory"""
    pics_dir = os.path.join(DIR_PATH, "profile_pics")
    pics = os.listdir(pics_dir)
    return os.path.join(pics_dir, choice(pics))


def generate_email(first_name: str, last_name: str, domain: str = "example.com") -> str:
    """
    Generate an email address based on the first and last name.

    Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        domain (str): Domain for the email address. Default is "example.com".

    Returns:
        str: A generated email address.
    """
    email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
    return email


def generate_username(first_name: str, last_name: str) -> str:
    """
    Generate a username based on the first and last name.

    Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.

    Returns:
        str: A generated username.
    """
    username = f"{first_name.lower()}.{last_name.lower()}"
    return username


def generate_password(length: int = 12) -> str:
    """
    Generate a random password of specified length.

    Args:
        length (int): Length of the password. Default is 12.

    Returns:
        str: A randomly generated password.
    """
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    password = ''.join(choices(characters, k=length))
    return password


def generate_phone_number(country: str) -> str:
    """
    Generate a random phone number based on the country code.

    Args:
        country (str): Country code ('PL' for Poland, 'US' for United States).

    Returns:
        str: A randomly generated phone number.
    """
    country_decoder_dict = {"Poland": "PL", "United States": "US", "PL": "PL", "US": "US"}
    phone_details_dict = {
        "PL": {
            "length": 9,
            "prefix": "+48",
        },
        "US": {
            "length": 10,
            "prefix": "+1",
        }
    }
    
    if country not in country_decoder_dict:
        raise ValueError(f"Unsupported country code. Supported codes are: {list(country_decoder_dict.keys())}")
    
    country_code = country_decoder_dict[country]
    phone_details = phone_details_dict[country_code]
    number = ''.join(choices('0123456789', k=phone_details['length']))
    
    return f"{phone_details['prefix']}{number}"

def generate_users(n: int) -> dict:
    """
    Generate `n` users with first and last names sampled from a Polish names dataset.

    Args:
        n (int): Number of users to generate.

    Returns:
        dict: A dictionary with keys 'first_name' and 'last_name'.
    """
    # Default list of Cities in Poland
    cities = ["Warszawa", "Kraków", "Łódź", "Wrocław", "Poznań", "Gdańsk", "Szczecin", "Bydgoszcz", "Lublin", "Białystok"]
    
    # Load datasets
    first_names_path = os.path.join(DIR_PATH, "sample_data", "imiona.txt")
    last_names_m_path = os.path.join(DIR_PATH, "sample_data", "nazwiska_meskie.txt")
    last_names_f_path = os.path.join(DIR_PATH, "sample_data", "nazwiska_zenskie.txt")
    first_names_df = pd.read_csv(first_names_path)
    last_names_m_df = pd.read_csv(last_names_m_path)
    last_names_f_df = pd.read_csv(last_names_f_path)
    
    # Sample first names and determine value counts for each gender
    generated_users = first_names_df.sample(n=n, weights="LICZBA_WYSTĄPIEŃ")
    generated_users["IMIĘ_PIERWSZE"] = generated_users["IMIĘ_PIERWSZE"].str.capitalize()
    gender_counts = generated_users["PŁEĆ"].value_counts().to_dict()
    
    # Sample last names and assign them to generated users
    generated_last_names_m = last_names_m_df.sample(n=gender_counts["MĘŻCZYZNA"], weights="Liczba")
    generated_last_names_f = last_names_f_df.sample(n=gender_counts["KOBIETA"], weights="Liczba")
    generated_users.loc[generated_users["PŁEĆ"] == "MĘŻCZYZNA", "last_name"] = generated_last_names_m["Nazwisko aktualne"].str.capitalize().values
    generated_users.loc[generated_users["PŁEĆ"] == "KOBIETA", "last_name"] = generated_last_names_f["Nazwisko aktualne"].str.capitalize().values
    
    # Select and rename columns
    generated_users = generated_users[["IMIĘ_PIERWSZE", "last_name"]]
    generated_users.rename(
        columns={
            "IMIĘ_PIERWSZE": "first_name",
            "last_name": "last_name",
        }, 
        inplace=True,
    )
    
    # Assign random cities and generate phone numbers
    generated_users["country"] = "Poland"
    generated_users["city"] = choices(cities, k=n)
    generated_users["phone_number"] = generated_users["country"].apply(generate_phone_number)
    
    # Generate usernames, emails, and passwords
    generated_users["username"] = generated_users.apply(lambda row: generate_username(row["first_name"], row["last_name"]), axis=1)
    generated_users["email"] = generated_users.apply(lambda row: generate_email(row["first_name"], row["last_name"]), axis=1)
    generated_users["password"] = generated_users.apply(lambda row: generate_password(), axis=1)
    
    # Assign random profile pictures
    generated_users["profile_picture"] = [random_pic() for _ in range(n)]
    
    # Write to JSON file
    json_path = os.path.join(DIR_PATH, "sample_data", "generated_users.json")
    with open(json_path, "w") as f:
        json.dump(generated_users.to_dict(orient="records"), f, indent=4)
    
    return generated_users.to_dict(orient="records")
