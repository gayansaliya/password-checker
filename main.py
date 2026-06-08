from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Password Strength Checker API")

# Define the request body structure
class PasswordInput(BaseModel):
    password: str

@app.post("/check-password")
def check_password_strength(data: PasswordInput):
    password = data.password
    score = 0
    suggestions = []

    # 1. Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long.")

    # 2. Uppercase Check
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Include at least one uppercase letter (A-Z).")

    # 3. Lowercase Check
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Include at least one lowercase letter (a-z).")

    # 4. Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Include at least one number (0-9).")

    # 5. Special Character Check
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Include at least one special character (e.g., !, @, #, $, %).")

    # Determine strength level based on the score
    if score == 5:
        strength = "Very Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "status": "success",
        "score": f"{score}/5",
        "strength": strength,
        "suggestions": suggestions if suggestions else ["Password is very strong!"]
    }