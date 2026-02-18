import gdown
import zipfile
import os

# Replace with your Google Drive file ID
file_id = "1ciyCZn_LOs0Vw-5mzmTnFaqyHpuVhAsT"
output = "data/lung_data.zip"

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Download
url = f"https://drive.google.com/uc?id={file_id}"
print("Downloading dataset...")
gdown.download(url, output, quiet=False)

# Extract
print("Extracting dataset...")
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall("data/")

print("Dataset ready in 'data/' folder")
