import json
import csv
import os

def format_time(seconds):
    hours = abs(seconds) // 3600
    minutes = (abs(seconds) % 3600) // 60
    secs = abs(seconds) % 60
    if hours > 0:
        return f"{hours}:{minutes:02}:{secs:02}"
    else:
        return f"{minutes}:{secs:02}"

json_path = input("Specify the path to the chat JSON file: ").strip()
release_timestamp = int(input("Specify release_timestamp (in seconds): "))

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

csv_rows = []

# Parsing strings
for item in data:
    if item.get("action_type") != "add_chat_item":
        continue

    name = item["author"]["name"]
    message = item["message"]
    timestamp = item["timestamp"]

    time_in_seconds = round(timestamp / 1e6) - release_timestamp

    # Remove messages before release_timestamp
    if time_in_seconds < 0:
        continue

    time_text = format_time(time_in_seconds)

    csv_rows.append({
        "author": name,
        "message": message,
        "timestamp": int(timestamp),
        "time_in_seconds": time_in_seconds,
        "time_text": time_text
    })

# Insert empty first row with rel_timestamp + 1
csv_rows.insert(0, {
    "author": "",
    "message": "",
    "timestamp": (release_timestamp + 1) * 1_000_000,
    "time_in_seconds": 0,
    "time_text": "0:00"
})

# Save in CSV
output_path = os.path.splitext(os.path.basename(json_path))[0] + ".csv"

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "message", "timestamp", "time_in_seconds", "time_text"])
    writer.writeheader()
    writer.writerows(csv_rows)

print(f"CSV file saved successfully as {output_path}")
