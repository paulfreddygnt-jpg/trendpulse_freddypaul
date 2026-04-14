import csv
from collections import Counter, defaultdict


CLEANED_DATA_FILE = "data/cleaned_trends.csv"
TOP_N = 5


def load_rows(file_path):
    with open(file_path, "r", encoding="utf-8") as file_obj:
        return list(csv.DictReader(file_obj))


def to_int(value):
    try:
        if value is None or value == "":
            return 0
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def print_category_counts(rows):
    counts = Counter(row["category"] for row in rows if row.get("category"))
    print("\nTop Categories:")
    if not counts:
        print("No category data available.")
        return
    for category, count in counts.most_common():
        print(f"{category}: {count}")


def print_top_scores(rows):
    top_rows = sorted(rows, key=lambda row: to_int(row.get("score")), reverse=True)[:TOP_N]
    print(f"\nTop {TOP_N} Stories by Score:")
    if not top_rows:
        print("No stories available.")
        return
    for row in top_rows:
        print(
            f'- {row.get("title", "")} | score={to_int(row.get("score"))} | '
            f'category={row.get("category", "")}'
        )


def print_average_by_category(rows, field_name, heading):
    totals = defaultdict(int)
    counts = defaultdict(int)

    for row in rows:
        category = row.get("category")
        if not category:
            continue
        totals[category] += to_int(row.get(field_name))
        counts[category] += 1

    print(f"\n{heading}:")
    if not counts:
        print("No category data available.")
        return

    for category in sorted(counts):
        average = totals[category] / counts[category]
        print(f"{category}: {average:.2f}")


def print_top_authors(rows):
    authors = Counter((row.get("author") or "unknown") for row in rows)
    print("\nTop Authors:")
    if not authors:
        print("No author data available.")
        return
    for author, count in authors.most_common(TOP_N):
        print(f"{author}: {count}")


def main():
    print("Task 3 started...")

    rows = load_rows(CLEANED_DATA_FILE)
    print(f"Data loaded: ({len(rows)}, {len(rows[0]) if rows else 0})")

    print_category_counts(rows)
    print_top_scores(rows)
    print_average_by_category(rows, "score", "Average Score per Category")
    print_top_authors(rows)
    print_average_by_category(
        rows, "num_comments", "Average Comments per Category"
    )

    print("\nTask 3 finished.")


if __name__ == "__main__":
    main()
