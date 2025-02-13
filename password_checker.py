import re
import hashlib
import requests
import random 
import string

def check_password_strength(password):

    if len(password)<8:
        return "Weak: Passowrd must be at least 8 characters long."
    
    if not re.search(r"[A-Z]",password):
        return "Weak: Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]",password):
        return "Weak: Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]",password):
        return "Weak: Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\:{}|<>]",password):
        return "Weak: Passowrd must contain at least one special character."
    
    return 'Strong: Your Password is secure!'

def check_pwned_password(password):
    # Μετατρέπουμε τον κωδικό σε SHA-1 Hash
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    first5_chars, rest = sha1_password[:5], sha1_password[5:]
    
    # Στέλνουμε μόνο τα πρώτα 5 chars στο API για προστασία απορρήτου
    response = requests.get(f"https://api.pwnedpasswords.com/range/{first5_chars}")
    
    if rest in response.text:
        return " Warning: This password has been found in a data breach! Choose a different one."
    return " This password is not found in leaked databases."


def generate_secure_password(length=16):
    """Δημιουργεί έναν ασφαλή τυχαίο κωδικό"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+=-"

    while True:
        secure_password = ''.join(random.choice(characters) for _ in range(length))
        
        # Ελέγχουμε αν περνάει την πολυπλοκότητα
        if check_password_strength(secure_password):
            # Ελέγχουμε αν έχει διαρρεύσει
            if check_pwned_password(secure_password):
                return secure_password  # Επιστρέφουμε τον τελικό ασφαλή κωδικό

failed_attempts = 0  

while True:
    password = input("Enter a password to check: ")

    # 1️⃣ Ελέγχουμε πρώτα την πολυπλοκότητα
    result = check_password_strength(password)
    print(result)

    if "Weak" in result:
        failed_attempts += 1  # Αυξάνουμε τις αποτυχημένες προσπάθειες

        # 2️⃣ Αν φτάσουμε 2 αποτυχημένες προσπάθειες, προτείνουμε secure password
        if failed_attempts == 2:
            choice = input("❓ Would you like the system to generate a secure password for you? (Yes/No): ").strip().lower()
            if choice == "yes":
               while True: 
                    suggested_password = generate_secure_password()
                    print(f"🔐 Suggested Secure Password: {suggested_password}")

                    if check_pwned_password(suggested_password):
                        print("This Password is strong and not leaked")
                        break  # Τερματίζουμε αφού του δώσαμε ισχυρό password
                    else:
                        print("Suggested Password was found in a leak. Generation a new one...")


               break         
            else:
                failed_attempts=0 #Set the failed attemps to 0 
        continue  # Συνεχίζουμε την επανάληψη αν ο κωδικός είναι αδύναμος

    # 3️⃣ Αν ο κωδικός είναι ισχυρός, ελέγχουμε αν είναι leaked
    breach_result = check_pwned_password(password)
    print(breach_result)

    if "Warning" in breach_result:
        continue  # Αν είναι leaked, ζητάμε νέο password

    # Αν περάσει και τα δύο tests, δεχόμαστε τον κωδικό
    break
