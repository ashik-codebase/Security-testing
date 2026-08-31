# Deliberately Vulnerable Student Management Application

An intentionally broken, single-file Student Management Application built using Python (`streamlit`) and an in-memory SQLite database. This project is specifically designed for local penetration testing labs, vulnerability assessment benchmarking, and educational code-review exercises.

## 👥 Seeded Personas & Credentials
The application starts with an in-memory database populated with 4 users spanning 3 distinct access levels:
1. **Admin** (Username: `admin`, Password: `AdminPass2026!`)
2. **Teacher** (Username: `prof_smith`, Password: `TeacherSec#1`)
3. **Student** (Username: `alice_jones`, Password: `StudentP@ss1`)
4. **Student** (Username: `bob_miller`, Password: `StudentP@ss2`)

## 📱 Features & Screens
- **Screen 1: Login Portal:** Basic entry point verifying identity parameters.
- **Screen 2: Role Dashboard:** A dynamic system panel that shows custom views (Announcements, Grades, Administrative Lists) depending on the active persona.
- **Screen 3: Profile Settings:** An update panel where users can alter account biographical metadata.

## 🪓 Intentionally Included Flaws
- **SQL Injection (SQLi):** Direct query assembly via text variables allows global validation bypasses (e.g., username input `admin' --`).
- **Hardcoded Backdoor:** Providing `BACKDOOR_KEY_2026` as the password bypasses standard hashing and matches any existing account name.
- **Insecure Direct Object Reference (IDOR):** Changing the numeric `ID` spinner on the Profile management portal shifts authorization state context directly without checking session validity.
- **Stored Cross-Site Scripting (XSS):** Announcements submitted by administrative contexts render raw script payloads to downstream viewers natively (`unsafe_allow_html=True`).

## 🚀 Installation & Local Launch
Ensure Python 3.8+ is installed on your workstation, then execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```
