import requests
import os

# List of countries
countries = [
    "USA", "Argentina", "UK", "Australia", "Turkey", "Belgium", "Sweden", "Brazil", "Spain",
    "Canada", "South Korea", "Russia", "Czech Republic", "China", "Poland", "France",
    "Netherlands", "Germany", "Mexico", "Hong Kong", "Japan", "Italy"
]

# Mapping of country names to their ISO 3166-1 alpha-2 codes
country_codes = {
    "USA": "us",
    "Argentina": "ar",
    "UK": "gb",
    "Australia": "au",
    "Turkey": "tr",
    "Belgium": "be",
    "Sweden": "se",
    "Brazil": "br",
    "Spain": "es",
    "Canada": "ca",
    "South Korea": "kr",
    "Russia": "ru",
    "Czech Republic": "cz",
    "China": "cn",
    "Poland": "pl",
    "France": "fr",
    "Netherlands": "nl",
    "Germany": "de",
    "Mexico": "mx",
    "Hong Kong": "hk",
    "Japan": "jp",
    "Italy": "it"
}

# Output directory
output_dir = r"YOUR_DIRECTORY"
os.makedirs(output_dir, exist_ok=True)

# Base URL for Flagpedia CDN
base_url = "https://flagcdn.com/w2560"

# Download each flag
for country in countries:
    code = country_codes.get(country)
    if code:
        url = f"{base_url}/{code}.png"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(output_dir, f"{country.replace(' ', '_')}.png")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {country}")
        else:
            print(f"Failed to download: {country} (HTTP {response.status_code})")
    else:
        print(f"No ISO code found for: {country}")
