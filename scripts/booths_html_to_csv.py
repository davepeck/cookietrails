#!/usr/bin/env python3
"""Parse eBudde booths HTML and emit CSV with one row per date/time slot."""

import csv
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup


def parse_booths_html(html_path: Path) -> list[dict]:
    """Parse booth HTML and return list of booth slot dictionaries."""
    with open(html_path) as f:
        soup = BeautifulSoup(f, "html.parser")

    rows = []

    # Each location is in a div with class "location"
    for location_div in soup.find_all("div", class_="location"):
        # Extract store name from first span.ellipsis inside span.percent40
        percent40_spans = location_div.find_all("span", class_="percent40")
        if not percent40_spans:
            continue

        # First percent40 span contains store name and zip
        name_span = percent40_spans[0]
        store_name_el = name_span.find("span", class_="ellipsis")
        # Normalize whitespace (HTML may have newlines/tabs)
        store_name = " ".join(store_name_el.get_text().split()) if store_name_el else ""

        # Find zip code
        zip_code = ""
        for span in name_span.find_all("span"):
            text = span.get_text(strip=True)
            if text.startswith("Zip:"):
                zip_code = text.replace("Zip:", "").strip()
                break

        # Second percent40 span contains address
        address = ""
        if len(percent40_spans) > 1:
            addr_span = percent40_spans[1]
            ellipsis_spans = addr_span.find_all("span", class_="ellipsis")
            if ellipsis_spans:
                # Normalize whitespace (HTML may have newlines/tabs)
                address = " ".join(ellipsis_spans[0].get_text().split())

        # Find all date/time slots in the timedrawer
        timedrawer = location_div.find("div", class_="timedrawer")
        if not timedrawer:
            continue

        for datetime_span in timedrawer.find_all("span", class_="cbs_datetime"):
            datetime_text = datetime_span.get_text(strip=True)
            # Parse datetime like "Thu Feb 26 2026 2:00pm - 8:00pm"
            match = re.match(
                r"(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+(\d+:\d+[ap]m)\s*-\s*(\d+:\d+[ap]m)",
                datetime_text,
            )
            if match:
                day_of_week, month, day, year, start_time, end_time = match.groups()
                rows.append(
                    {
                        "store_name": store_name,
                        "address": address,
                        "zip_code": zip_code,
                        "date": f"{month} {day}, {year}",
                        "day_of_week": day_of_week,
                        "start_time": start_time,
                        "end_time": end_time,
                    }
                )

    return rows


def main():
    html_path = Path(__file__).parent.parent / "data" / "seattle_booths.html"
    if not html_path.exists():
        print(f"Error: {html_path} not found", file=sys.stderr)
        sys.exit(1)

    rows = parse_booths_html(html_path)

    # Write CSV to stdout
    fieldnames = [
        "store_name",
        "address",
        "zip_code",
        "day_of_week",
        "date",
        "start_time",
        "end_time",
    ]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
