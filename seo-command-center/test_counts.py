from seo.detector import load_rows

rows = load_rows("../sample-export")

print("Rows:", len(rows))

server_errors = [
    r["Address"]
    for r in rows
    if str(r.get("Status Code", "")).startswith("5")
]

print("5xx count:", len(server_errors))

missing_titles = [
    r["Address"]
    for r in rows
    if not str(r.get("Title 1", "")).strip()
]

print("Missing titles:", len(missing_titles))