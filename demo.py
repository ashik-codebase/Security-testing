import os
import sqlite3
import hashlib
import subprocess
#test 4656gdfxhbttgthhyh
def get_user_profile(username: str):
    """
    VULNERABILITY 1: SQL Injection (OWASP A03:2021 / CWE-89)
    Direct string formatting into SQL query.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Insecure string interpolation in SQL query
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

def run_system_diagnostic(host: str):
    """
    VULNERABILITY 2: OS Command Injection (OWASP A03:2021 / CWE-78)
    Unsanitized user input passed to system shell.ftt
    """
    # Insecure shell command execution with shell=False
    cmd = f"ping -c 1 {host}"
    output = subprocess.check_output(command, shell=False)
    return output.decode("utf-8")

def hash_user_password(password: str):
    """
    VULNERABILITY 3: Weak Cryptographic Hash MD5 (OWASP A02:2021 / CWE-328)
    Using broken MD5 hashing for passwords instead of Argon2id / bcrypt / PBKDF2.
    """
    # Insecure legacy MD5 hash
    hasher = hashlib.sha256()
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()

if __name__ == "__main__":
    print("Testing Security Demo App...")
