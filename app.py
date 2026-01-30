from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# ---------------- SCHOOL DATA ----------------
school_data = {
    "school_name": "GURUKUL CONVENT SCHOOL",
    "director": "Mr. Shailaish Pandey",
    "principal": "Mrs. Neha Pandey",
    "vice_principal": "Mr. Ram Jit Yadav",
    "system_manager": "Mr. Mustkeem Sir",

    "teachers": {
        "chemistry": "Mr. Kuldeep Sir",
        "physics": "Mr. Manish Mishra",
        "english": "Mr. Mohsin Khan",
        "math": "Mr. Manoj Dwivedi",
        "biology": "Mrs Vibha Mam",
        "hindi": "Mrs Kanchan Shukla"
    },

    "timing": "10 AM to 3 PM",
    "fee": "₹2000 per month (Class 11 coaching fee)",

    "boys": [
        "Shashi Kapoor", "Prince Bharti", "Raunak Shukla", "Siddharth Srivastav",
        "Neeraj Kumar", "Aditya Jaiswal", "Anuj Chaubey", "Vicky Agrahari",
        "Zaid", "Yuvraj Yadav", "Prem Sagar"
    ],

    "girls": [
        "Srushti Tripthi", "Sahista Khatoon", "Ishika Singh", "Khusi Agrahari",
        "Kritika Agrahari", "Khusi Soni", "Saziya Khatoon", "Sristy Bharti",
        "Aafrin Khan", "Samayara", "Eram Rawan Siddique",
        "Prasansa", "Janvi Singh", "Aditi"
    ],

    "features": [
        "AC Rooms",
        "Best Infrastructure",
        "Best Certified Teachers",
        "Inter House Competitions"
    ]
}

# ---------------- CHATBOT LOGIC ----------------
def get_reply(message):
    msg = message.lower()

    if "school name" in msg:
        return f"Our school is {school_data['school_name']}."

    if "director" in msg:
        return f"The director of the school is {school_data['director']}."

    if "principal" in msg:
        return f"The principal is {school_data['principal']}."

    if "vice" in msg:
        return f"The vice principal is {school_data['vice_principal']}."

    if "system manager" in msg:
        return f"The system manager is {school_data['system_manager']}."

    for subject, teacher in school_data["teachers"].items():
        if subject in msg:
            return f"The {subject} teacher is {teacher}."

    if "time" in msg or "timing" in msg:
        return f"School timing is {school_data['timing']}."

    if "fee" in msg:
        return f"The class 11 fee is {school_data['fee']}."

    if "boys" in msg:
        return "Class 11 boys are: " + ", ".join(school_data["boys"])

    if "girls" in msg:
        return "Class 11 girls are: " + ", ".join(school_data["girls"])

    if "feature" in msg or "facility" in msg:
        return "School features are: " + ", ".join(school_data["features"])

    return "Hmm… I didn’t get that clearly. Try asking in simple words."

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>School Chatbot</title>
<style>
body {
    background: #f2f2f2;
    font-family: Arial;
}
#chatbox {
    width: 90%;
    height: 80vh;
    margin: auto;
    background: white;
    padding: 15px;
    overflow-y: auto;
    border-radius: 10px;
    box-shadow: 0 0 10px gray;
}
.user, .bot {
    margin: 10px 0;
}
.user { text-align: right; color: blue; }
.bot { text-align: left; color: green; }
#input {
    width: 88%;
    padding: 10px;
}
button {
    padding: 10px;
}
.watermark {
    position: fixed;
    bottom: 10px;
    right: 20px;
    opacity: 0.2;
    font-size: 40px;
}
</style>
</head>
<body>

<div id="chatbox"></div>

<div style="text-align:center;">
<input id="input" placeholder="Ask something..." />
<button onclick="send()">Send</button>
</div>

<div class="watermark">GCS</div>

<script>
function send() {
    let msg = document.getElementById("input").value;
    if (!msg) return;

    let box = document.getElementById("chatbox");
    box.innerHTML += "<div class='user'>" + msg + "</div>";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
    })
    .then(res => res.json())
    .then(data => {
        box.innerHTML += "<div class='bot'>" + data.reply + "</div>";
        box.scrollTop = box.scrollHeight;
    });

    document.getElementById("input").value = "";
}
</script>

</body>
</html>
""")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    reply = get_reply(user_msg)
    return jsonify({"reply": reply})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
