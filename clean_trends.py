import csv
import json
import os
import sys


DATA_FOLDER = "data"
OUTPUT_FILE = os.path.join(DATA_FOLDER, "cleaned_trends.csv")
EXPECTED_COLUMNS = [
    "post_id",
    "title",
    "category",
    "score",
    "num_comments",
    "author",
    "collected_at",
]


def find_latest_json_file(data_folder):
    files = sorted(
        file_name for file_name in os.listdir(data_folder) if file_name.endswith(".json")
    )
    if not files:
        return None
    return os.path.join(data_folder, files[-1])


def load_records(file_path):
    with open(file_path, "r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)
    if isinstance(data, list):
        return data
    return []


def normalize_record(record):
    normalized = {}
    for column in EXPECTED_COLUMNS:
        normalized[column] = record.get(column)
    return normalized


def to_int(value):
    try:
        if value is None or value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def clean_records(records):
    seen_post_ids = set()
    cleaned = []

    for record in records:
        normalized = normalize_record(record)
        post_id = normalized["post_id"]

        if post_id in seen_post_ids:
            continue
        seen_post_ids.add(post_id)

        normalized["score"] = to_int(normalized["score"])
        normalized["num_comments"] = to_int(normalized["num_comments"])
        normalized["title"] = str(normalized["title"] or "").strip()
        normalized["author"] = str(normalized["author"] or "unknown").strip() or "unknown"

        category = normalized["category"]
        if category is None or str(category).strip() == "":
            continue

        normalized["category"] = str(category).strip()
        cleaned.append(normalized)

    return cleaned


def write_csv(records, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(records)


def main():
    print("Task 2 started...")

    if not os.path.isdir(DATA_FOLDER):
        print(f"Data folder not found: {DATA_FOLDER}")
        sys.exit(1)

    latest_file = find_latest_json_file(DATA_FOLDER)
    if not latest_file:
        print("No JSON file found")
        sys.exit(1)

    print(f"Loading file: {latest_file}")

    records = load_records(latest_file)
    initial_columns = len(records[0].keys()) if records else 0
    print(f"Initial shape: ({len(records)}, {initial_columns})")

    cleaned_records = clean_records(records)
    print(f"After cleaning: ({len(cleaned_records)}, {len(EXPECTED_COLUMNS)})")

    write_csv(cleaned_records, OUTPUT_FILE)

    print(f"Saved cleaned data to: {OUTPUT_FILE}")
    print("Task 2 finished.")


if __name__ == "__main__":
    main()
