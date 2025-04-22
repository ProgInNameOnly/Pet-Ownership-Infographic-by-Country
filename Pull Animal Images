import requests
import os
import shutil

# Configuration
API_KEY = "YOUR_API"  # Replace with your Pexels API key
ANIMALS = ["cat", "dog", "fish", "bird"]
OUTPUT_DIR = r"C:\Users\tdent\Desktop\Plotly_Figure_Friday\Week 16"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_one_image(query, api_key, output_dir):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "per_page": 1,
        "page": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error for '{query}': {response.status_code}")
        return

    data = response.json()
    photos = data.get("photos", [])
    if not photos:
        print(f"No images found for '{query}'.")
        return

    img_url = photos[0]["src"]["original"]
    img_response = requests.get(img_url, stream=True)
    if img_response.status_code == 200:
        img_name = f"{query}.jpg"
        img_path = os.path.join(output_dir, img_name)
        with open(img_path, "wb") as f:
            shutil.copyfileobj(img_response.raw, f)
        print(f"Downloaded: {img_name}")
    else:
        print(f"Failed to download image for '{query}'")

# Run the script
if __name__ == "__main__":
    for animal in ANIMALS:
        download_one_image(animal, API_KEY, OUTPUT_DIR)
