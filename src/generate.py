import os
import re
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve_relevant_chunks

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CSV_PATH = "placement_data.csv"


# ============================================================
# LOAD STRUCTURED PLACEMENT DATA
# ============================================================

def load_placement_data():
    if not os.path.exists(CSV_PATH):
        return None

    df = pd.read_csv(CSV_PATH)

    df["company"] = df["company"].astype(str).str.upper().str.strip()
    df["year"] = df["year"].astype(str).str.strip()
    df["offers"] = pd.to_numeric(df["offers"], errors="coerce")

    return df


# ============================================================
# NORMALIZATION
# ============================================================

def canonical(text):
    """
    Convert text into a comparison-friendly form.

    Example:
    ALLSECTECHNOLOGIES
    ALLSEC TECHNOLOGIES
    Allsec-Technologies

    -> ALLSECTECHNOLOGIES
    """

    return re.sub(r"[^A-Z0-9]", "", str(text).upper())


def extract_year(question):
    """
    Extract academic year such as:
    2021-22
    2021–22
    2021-2022
    """

    match = re.search(
        r"(20\d{2})\s*[-–]\s*(\d{2,4})",
        question
    )

    if not match:
        return None

    first = match.group(1)
    second = match.group(2)

    if len(second) == 2:
        return f"{first}-{second}"

    return f"{first}-{second[-2:]}"


# ============================================================
# FIND COMPANY IN QUESTION
# ============================================================

def find_company(question, df):

    question_canonical = canonical(question)

    companies = df["company"].dropna().unique()

    # Longest company names first
    # This prevents short names from matching incorrectly.
    companies = sorted(
        companies,
        key=lambda x: len(canonical(x)),
        reverse=True
    )

    for company in companies:

        company_canonical = canonical(company)

        if len(company_canonical) < 3:
            continue

        if company_canonical in question_canonical:
            return company

    return None


# ============================================================
# STRUCTURED LOOKUP
# ============================================================

def structured_lookup(question):

    df = load_placement_data()

    if df is None or df.empty:
        return None

    year = extract_year(question)

    question_lower = question.lower()

    # ========================================================
    # 1. COMPANY-SPECIFIC QUERY
    # ========================================================

    company = find_company(question, df)

    if company and year:

        result = df[
            (df["year"] == year) &
            (df["company"] == company)
        ]

        if not result.empty:

            total_offers = int(result["offers"].sum())

            sources = result["source"].dropna().unique().tolist()

            answer = (
                f"**{company}** had **{total_offers} offers** "
                f"in the **{year} academic year**."
            )

            return answer, sources


    # ========================================================
    # 2. TOTAL OFFERS FOR A YEAR
    # ========================================================

    if year and (
        "how many offers" in question_lower
        or "total offers" in question_lower
        or "number of offers" in question_lower
        or "placement offers" in question_lower
    ):

        result = df[df["year"] == year]

        if not result.empty:

            total_offers = int(result["offers"].sum())

            sources = result["source"].dropna().unique().tolist()

            answer = (
                f"**{total_offers} placement offers** were recorded "
                f"in the **{year} academic year**."
            )

            return answer, sources


    # ========================================================
    # 3. COMPANY LIST FOR A YEAR
    # ========================================================

    if year and (
        "what companies" in question_lower
        or "which companies" in question_lower
        or "companies recruited" in question_lower
        or "companies that recruited" in question_lower
    ):

        result = df[df["year"] == year].copy()

        if not result.empty:

            grouped = (
                result.groupby("company", as_index=False)["offers"]
                .sum()
                .sort_values("company")
            )

            lines = [
                f"### Companies that recruited in {year}\n"
            ]

            for _, row in grouped.iterrows():

                lines.append(
                    f"- {row['company']} — "
                    f"{int(row['offers'])} offers"
                )

            lines.append("")
            lines.append(
                f"**Total companies:** {len(grouped)}"
            )

            lines.append(
                f"**Total offers:** {int(grouped['offers'].sum())}"
            )

            sources = result["source"].dropna().unique().tolist()

            return "\n".join(lines), sources


    # ========================================================
    # 4. YEAR-TO-YEAR COMPARISON
    # ========================================================

    years = re.findall(
        r"20\d{2}\s*[-–]\s*\d{2,4}",
        question
    )

    if len(years) >= 2:

        extracted_years = []

        for y in years:

            match = re.match(
                r"(20\d{2})\s*[-–]\s*(\d{2,4})",
                y
            )

            if match:

                first = match.group(1)
                second = match.group(2)

                if len(second) == 2:
                    formatted = f"{first}-{second}"
                else:
                    formatted = f"{first}-{second[-2:]}"

                if formatted not in extracted_years:
                    extracted_years.append(formatted)

        if len(extracted_years) >= 2:

            year1 = extracted_years[0]
            year2 = extracted_years[1]

            df1 = df[df["year"] == year1]
            df2 = df[df["year"] == year2]

            if not df1.empty and not df2.empty:

                total1 = int(df1["offers"].sum())
                total2 = int(df2["offers"].sum())

                companies1 = set(df1["company"])
                companies2 = set(df2["company"])

                common = companies1.intersection(companies2)

                answer = f"""### Comparison: {year1} vs {year2}

**Total offers**
- {year1}: {total1}
- {year2}: {total2}

**Companies with records**
- {year1}: {len(companies1)}
- {year2}: {len(companies2)}

**Companies appearing in both years:** {len(common)}
"""

                sources = list(
                    dict.fromkeys(
                        df1["source"].dropna().tolist()
                        + df2["source"].dropna().tolist()
                    )
                )

                return answer, sources


    # No structured answer
    return None


# ============================================================
# MAIN ANSWER GENERATOR
# ============================================================

def generate_answer(question, top_k=6):

    # --------------------------------------------------------
    # FIRST: Try exact structured data
    # --------------------------------------------------------

    structured_result = structured_lookup(question)

    if structured_result:

        answer, sources = structured_result

        return answer, [
            {"source": source}
            for source in sources
        ]


    # --------------------------------------------------------
    # SECOND: Fall back to RAG
    # --------------------------------------------------------

    chunks = retrieve_relevant_chunks(
        question,
        top_k=top_k
    )

    context = "\n\n".join(
        [
            f"[Source: {c['source']}]\n{c['text']}"
            for c in chunks
        ]
    )

    prompt = f"""
You are PlaceWise, an AI assistant that answers questions
about college placement data.

Use ONLY the provided context.

Context:
{context}

Question:
{question}

Instructions:

- Answer only using the provided context.
- Do not invent numbers.
- Do not confuse a company-level offer count with the
  total offers for an entire academic year.
- If the answer is not present in the context, say:
  "This isn't covered in the available documents."
- Be concise and direct.
- Mention the source document when relevant.

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content, chunks


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    test_questions = [

        "What companies recruited students in 2021-22?",

        "How many offers were made in 2021-22?",

        "How many offers did ALLSECTECHNOLOGIES have in 2021-22?",

        "How many offers did Amazon have in 2021-22?",

        "How many offers did Accenture have in 2022-23?",

        "Compare placement data from 2021-22 and 2022-23"
    ]

    for question in test_questions:

        print("\n" + "=" * 70)

        print("QUESTION:", question)

        print("=" * 70)

        answer, sources = generate_answer(question)

        print("\nANSWER:")
        print(answer)

        if sources:

            print("\nSOURCES:")

            for source in sources:

                if isinstance(source, dict):
                    print("-", source["source"])
                else:
                    print("-", source)