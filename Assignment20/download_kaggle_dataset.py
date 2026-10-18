# Download the complete Kaggle TMDB 5000 Movie Dataset.
# Requires Kaggle API credentials configured on the machine.
#
# Kaggle source:
# https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
#
# Run:
#   pip install kaggle
#   python download_kaggle_dataset.py
#
# Then replace the sample file with the downloaded tmdb_5000_movies.csv.

from pathlib import Path
import subprocess
import zipfile

target = Path("data")
target.mkdir(exist_ok=True)

subprocess.run([
    "kaggle", "datasets", "download",
    "-d", "tmdb/tmdb-movie-metadata",
    "-p", str(target)
], check=True)

zip_path = target / "tmdb-movie-metadata.zip"
if zip_path.exists():
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(target)
    zip_path.unlink()

print("Complete Kaggle dataset downloaded into data/.")
