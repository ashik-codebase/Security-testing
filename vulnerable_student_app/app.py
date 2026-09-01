import streamlit as st
import sqlite3
#testu
# Initialize In-Memory Database for local testing
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT,
            full_name TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            subject TEXT,
            grade TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    ''')
    
    # Seed Personas & App Initial State
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (username, password, role, full_name, email) VALUES (?, ?, ?, ?, ?)", [
            ('admin', 'AdminPass2026!', 'Admin', 'System Administrator', 'admin@school.edu'),
            ('prof_smith', 'TeacherSec#1', 'Teacher', 'Professor Robert Smith', 'r.smith@school.edu'),
            ('alice_jones', 'StudentP@ss1', 'Student', 'Alice Jones', 'alice.j@school.edu'),
            ('bob_miller', 'StudentP@ss2', 'Student', 'Bob Miller', 'bob.m@school.edu')
        ])
        cursor.executemany("INSERT INTO grades (student_name, subject, grade) VALUES (?, ?, ?)", [
            ('Alice Jones', 'Cybersecurity 101', 'A'),
            ('Alice Jones', 'Database Systems', 'B+'),
            ('Bob Miller', 'Cybersecurity 101', 'C-'),
            ('Bob Miller', 'Software Engineering', 'A-')
        ])
        cursor.executemany("INSERT INTO announcements (content) VALUES (?)", [
            ('Welcome to the 2026 Academic Year!',),
            ('Reminder: Midterm exam registrations close this Friday.',)
        ])
        conn.commit()
    return conn

conn = init_db()
#password for login:"password@1234"
cursor = conn.cursor()

# Session State Setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.user_id = None

st.set_page_config(page_title="Vulnerable Student Portal", layout="centered")

# Logout Button
if st.session_state.logged_in:
    if st.sidebar.button("🔓 Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.user_id = None
        st.rerun()

# --- SCREEN 1: LOGIN PORTAL ---
if not st.session_state.logged_in:
    st.title("🎓 EduSecure Student Management System")
    st.subheader("Sign In")
    
    user_input = st.text_input("Username")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # VULNERABILITY 1: SQL Injection (Direct string concatenation)
        # VULNERABILITY 2: Hardcoded Backdoor Password Token (BACKDOOR_KEY_2026)
        if pass_input == "BACKDOOR_KEY_2026":
            query = f"SELECT id, username, role FROM users WHERE username = '{user_input}'"
        else:
            query = f"SELECT id, username, role FROM users WHERE username = '{user_input}' AND password = '{pass_input}'"
        
        try:
            cursor.execute(query)
            user_record = cursor.fetchone()
            
            if user_record:
                st.session_state.logged_in = True
                st.session_state.user_id = user_record[0]
                st.session_state.username = user_record[1]
                st.session_state.role = user_record[2]
                st.success(f"Welcome back, {user_record[1]}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Database Error: {e} (Query executed: {query})")

# --- AUTHENTICATED EXPERIENCE ---
else:
    # Sidebar Navigation Menu (Screens 2 and 3)
    screen = st.sidebar.radio("Navigation", ["📋 Dashboard Menu", "👤 Edit My Profile"])
    
    # --- SCREEN 2: DYNAMIC ROLE DASHBOARD ---
    if screen == "📋 Dashboard Menu":
        st.title(f"Dashboard - {st.session_state.role} Interface")
        st.write(f"Active Session: **{st.session_state.username}**")
        
        # Section A: Global Announcements
        st.write("---")
        st.markdown("### 📢 Campus Announcements")
        
        # VULNERABILITY 3: Stored XSS via custom HTML rendering (unsafe_allow_html=True)
        cursor.execute("SELECT content FROM announcements")
        announcements = cursor.fetchall()
        for ann in announcements:
            st.markdown(f"<div style='padding:10px; background-color:#f0f2f6; border-radius:5px; margin-bottom:10px;'>{ann[0]}</div>", unsafe_allow_html=True)
            
        # Persona Logic for Adding Announcements
        if st.session_state.role in ["Teacher", "Admin"]:
            new_announcement = st.text_area("Post New Announcement (Teachers/Admins Only)")
            if st.button("Broadcast Announcement"):
                if new_announcement:
                    cursor.execute("INSERT INTO announcements (content) VALUES (?)", (new_announcement,))
                    conn.commit()
                    st.success("Announcement broadcasted successfully!")
                    st.rerun()

        # Section B: Gradebook View (Persona Boundaries)
        st.write("---")
        st.markdown("### 📊 Academic Gradebook Record Lookup")
        
        if st.session_state.role == "Student":
            cursor.execute("SELECT full_name FROM users WHERE username = ?", (st.session_state.username,))
            full_name = cursor.fetchone()[0]
            cursor.execute("SELECT subject, grade FROM grades WHERE student_name = ?", (full_name,))
            student_grades = cursor.fetchall()
            for g in student_grades:
                st.write(f"📚 **{g[0]}:** {g[1]}")
                
        elif st.session_state.role in ["Teacher", "Admin"]:
            cursor.execute("SELECT student_name, subject, grade FROM grades")
            all_grades = cursor.fetchall()
            st.table([{"Student": row[0], "Subject": row[1], "Grade": row[2]} for row in all_grades])

        # Section C: Administrative User Panel
        if st.session_state.role == "Admin":
            st.write("---")
            st.markdown("### 🛠️ Administrative Database Control Panel")
            cursor.execute("SELECT id, username, role, full_name, email FROM users")
            all_users = cursor.fetchall()
            st.table([{"ID": u[0], "User": u[1], "Role": u[2], "Name": u[3], "Email": u[4]} for u in all_users])

    # --- SCREEN 3: PROFILE SETTINGS ---
    elif screen == "👤 Edit My Profile":
        st.title("Profile Management Console")
        
        # VULNERABILITY 4: Insecure Direct Object Reference (IDOR)
        target_id = st.number_input("Look up / Edit User Record ID:", min_value=1, value=int(st.session_state.user_id))
        
        cursor.execute("SELECT username, role, full_name, email FROM users WHERE id = ?", (target_id,))
        profile = cursor.fetchone()
        
        if profile:
            st.write("---")
            st.write(f"📂 Viewing Account Signature: **{profile[2]}** ({profile[1]})")
            new_name = st.text_input("Full Name", value=profile[2])
            new_email = st.text_input("Email Address", value=profile[3])
            
            if st.button("Save Profile Adjustments"):
                cursor.execute("UPDATE users SET full_name = ?, email = ? WHERE id = ?", (new_name, new_email, target_id))
                conn.commit()
                st.success(f"Profile configurations for entry ID {target_id} updated successfully!")
        else:
            st.error("Target database indexing profile record not found.")
