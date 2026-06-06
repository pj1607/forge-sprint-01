# test_missing_title.py

from seo.detector import load_rows

rows = load_rows("../sample-export")

count = 0

for r in rows:
    content_type = str(r.get("Content Type", "")).lower()
    status = str(r.get("Status Code", ""))
    indexability = str(r.get("Indexability", "")).lower()

    if (
        "text/html" in content_type
        and status == "200"
        and indexability == "indexable"
    ):
        title = str(r.get("Title 1", "")).strip()

        if not title:
            count += 1

print("Missing title issues:", count)