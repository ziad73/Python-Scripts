from bs4 import BeautifulSoup

# GPA mapping
grade_to_points = {
    "A+": 4.0,
    "A": 4.7,
    "A-": 3.4,
    "B+": 3.2,
    "B": 3.0,
    "B-": 2.8,
    "C+": 2.6,
    "C": 2.4,
    "C-": 1.2,
    "D+": 2.0,
    "D": 1.5,
    "D-": 1.0,
    "F": 0.0,
}

# === Get Year Range from User ===
start_year = int(input("Enter start year (e.g. 2023): "))
end_year = int(input("Enter end year (e.g. 2024): "))

# === Get Terms Per Year ===
year_term_map = {}
for year in range(start_year, end_year + 1):
    terms_input = input(f"Enter terms for {year} (comma-separated: First Term, Second Term): ")
    terms = [term.strip() for term in terms_input.split(",")]
    year_term_map[str(year)] = terms

# === Load HTML ===
with open("E:\\college\\Grades\\Student Courses.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

rows = soup.select("table.table-striped tbody tr")
total_points = 0
total_credits = 0 #Total Hours

# === Process Rows ===
for row in rows:
    columns = row.find_all("td")
    if len(columns) >= 12:
        year = columns[5].get_text(strip=True)
        term = columns[11].get_text(strip=True)

        if year not in year_term_map or term not in year_term_map[year]:
            continue

        grade_text = columns[6].get_text(strip=True).upper()
        credit_text = columns[3].get_text(strip=True)

        if grade_text not in grade_to_points:
            continue  # No grade yet

        try:
            credit = int(credit_text)
        except ValueError:
            continue

        if credit > 0:
            gpa_point = grade_to_points[grade_text]
            total_points += gpa_point * credit
            total_credits += credit

# === Output Result ===
print("====================")
if total_credits > 0:
    gpa = total_points / total_credits
    print("Included Terms:")
    for y, terms in year_term_map.items():
        print(f"  {y}: {', '.join(terms)}")
    print(f"\nCalculated GPA: {gpa:.2f}")
    print(f"\nTotal Points: {total_points:.2f}")
    print(f"\nTotal Hours: {total_credits:.2f}")
else:
    print("No graded subjects found in the selected range.")
