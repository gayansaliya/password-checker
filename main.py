from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import re

app = FastAPI(title="Password Strength Checker")

# 🧠 Core logic function (UI එකටයි, API එකටයි දෙකටම පොදුවේ පාවිච්චි කරන්න)
def calculate_strength(password: str):
    score = 0
    suggestions = []

    if not password:
        return {"score": "0/5", "strength": "Empty", "suggestions": ["Please enter a password."]}

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

    if score == 5:
        strength = "Very Strong"
    elif score >= 3:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "score": f"{score}/5",
        "strength": strength,
        "suggestions": suggestions if suggestions else ["Password is very strong!"]
    }


# 🌐 1. මේක තමයි ඔයාගේ ලස්සන UI එක (Home Page)
@app.get("/", response_class=HTMLResponse)
def get_ui(password: str = Query(None)):
    result_html = ""
    
    # URL එකේ password එකක් තිබ්බොත් විතරක් ප්‍රතිඵලය පෙන්නන්න
    if password:
        res = calculate_strength(password)
        
        # Strength එක අනුව පාට තීරණය කිරීම
        color = "red" if res["strength"] == "Weak" else "yellow" if res["strength"] == "Medium" else "green"
        
        suggestions_list = "".join([f"<li class='text-sm text-gray-600'>• {s}</li>" for s in res["suggestions"]])
        
        result_html = f"""
        <div class="mt-6 p-4 bg-{color}-50 border border-{color}-200 rounded-lg">
            <h2 class="text-xl font-bold text-{color}-700">Strength: {res["strength"]} ({res["score"]})</h2>
            <ul class="mt-2 space-y-1">
                {suggestions_list}
            </ul>
        </div>
        """

    # සම්පූර්ණ HTML පිටුව (Tailwind CSS වලින් හැඩ කරපු)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Strength Checker</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex items-center justify-center min-h-screen">
        <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">🔒 Password Strength Checker</h1>
            
            <form method="get" action="/" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Enter Password</label>
                    <input type="text" name="password" value="{password or ''}" placeholder="Type your password here..." 
                           class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded-md transition duration-200">
                    Check Strength
                </button>
            </form>

            {result_html}
            
            <div class="mt-6 text-center text-xs text-gray-400">
                <p>You can also use the URL: <code>/?password=your_text</code></p>
            </div>
        </div>
    </body>
    </html>
    """


# 🚀 2. මේක URL එකෙන්ම Data ගන්න පුළුවන් API Endpoint එක (JSON Response)
@app.get("/api/check")
def check_via_url(password: str = Query(..., description="The password to check")):
    result = calculate_strength(password)
    return {
        "status": "success",
        "password_checked": password,
        **result
    }
