import os
import re
import pdfplumber
import pandas as pd

DATA_DIR = "data"

def extract_year_from_filename(filename):
    match = re.search(r"(\d{4})-(\d{2,4})", filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return "Unknown"

def normalize_company_name(name):
    """Clean up company names so variants of the same company merge together."""
    name = name.upper()
    name = re.sub(r'[^\w\s]', '', name)  # remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # collapse multiple spaces
    # Remove common suffixes that cause mismatches
    name = re.sub(r'\b(PVT|LTD|PRIVATE|LIMITED|PVTLTD|INC)\b', '', name).strip()
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def build_dataset():
    rows = []
    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith(".pdf"):
            continue
        year = extract_year_from_filename(filename)
        path = os.path.join(DATA_DIR, filename)

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    for row in table:
                        clean = [c.strip() if c else "" for c in row]
                        nums = [c for c in clean if c.replace(",", "").isdigit()]
                        text_cells = [c for c in clean if c and not c.replace(",", "").isdigit()]
                        if nums and text_cells:
                            company = max(text_cells, key=len)
                            company = normalize_company_name(company)
                            try:
                                offers = int(nums[-1].replace(",", ""))
                                rows.append({"year": year, "company": company, "offers": offers, "source": filename})
                            except ValueError:
                                continue

    df = pd.DataFrame(rows)
    df = df[df["company"].str.len() > 2]
    return df

if __name__ == "__main__":
    df = build_dataset()
    print(df.head(20))
    print(f"\nTotal rows extracted: {len(df)}")
    df.to_csv("placement_data.csv", index=False)
    print("Saved to placement_data.csv")