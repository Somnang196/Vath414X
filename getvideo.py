import requests
import os

# Path to your txt file containing MP4 links (one link per line)
txt_file = "link.txt"

# Folder where downloaded videos will be saved
output_folder = "gif"
os.makedirs(output_folder, exist_ok=True)

# Read links from the txt file
with open(txt_file, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# Download each video
for link in links:
    try:
        print(f"Downloading: {link}")
        response = requests.get(link, stream=True)
        response.raise_for_status()  # Check for HTTP errors

        # Get the filename from the URL
        filename = os.path.join(output_folder, link.split("/")[-1])

        # Write the content to a file
        with open(filename, "wb") as video_file:
            for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                video_file.write(chunk)

        print(f"Saved: {filename}\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {link}: {e}")
