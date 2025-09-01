import json
import pandas as pd
import glob
import os

# Paths
input_path = r"C:\Users\ADMIN\Desktop\spotify-wrapped\data\raw"      # where your JSON files are
output_path = r"C:\Users\ADMIN\Desktop\spotify-wrapped\data\spotify_cleaned.csv"

# Collect ALL JSON files in that folder
all_files = glob.glob(os.path.join(input_path, "*.json"))

dfs = []
for file in all_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        
        # Add a column to identify source (music/podcast)
        if "music" in file.lower():
            df["source"] = "music"
        elif "podcast" in file.lower():
            df["source"] = "podcast"
        else:
            df["source"] = "unknown"
        
        dfs.append(df)

# Merge all into one DataFrame
spotify_df = pd.concat(dfs, ignore_index=True)

# Convert msPlayed → minutesPlayed (rounded to 2 decimals)
spotify_df["minutesPlayed"] = (spotify_df["msPlayed"] / 60000).round(2)

# Save cleaned dataset
spotify_df.to_csv(output_path, index=False)

print(f"✅ Cleaned data saved at {output_path}")
print(f"📊 Total records: {len(spotify_df)}")
print("📂 Sources included:", spotify_df['source'].unique())