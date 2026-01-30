from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

ADMIN_PASSWORD = "admin123"

def load_data():
    with open("data.json") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

CHAT_HTML = """
<h2>GURUKUL CONVENT SCHOOL – Sinoy Helpdesk</h2>
<form method="post">
<input name="q" style="width:400px" placeholder="Ask your question">
<button>Ask</button>
</form>
<p><b>{{reply}}</b></p>
"""

ADMIN_HTML = """
<h2>ADMIN PANEL</h2>
<form method="post">
School Name: <input name="school_name" value="{{d['school_name']}}"><br><br>
Principal: <input name="principal" value="{{d['principal']}}"><br><br>
Director: <input name="director" value="{{d['director']}}"><br><br>
Timing: <input name="school_timing" value="{{d['school_timing']}}"><br><br>
Fees: <input name="fees" value="{{d['fees']}}"><br><br>
Chemistry Teacher: <input name="chemistry" value="{{d['teachers']['chemistry']}}"><br><br>
<button>Save</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def chat():
    data = load_data()
    reply = ""
    if request.method == "POST":
        q = request.form["q"].lower()
        if "principal" in q:
            reply = data["principal"]
        elif "timing" in q:
            reply = data["school_timing"]
        elif "chemistry" in q:
            reply = data["teachers"]["chemistry"]
        else:
            reply = "I am Sinoy. Ask school-related questions."
    return render_template_string(CHAT_HTML, reply=reply)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.args.get("pass") != ADMIN_PASSWORD:
        return "Unauthorized"

    data = load_data()
    if request.method == "POST":
        data["school_name"] = request.form["school_name"]
        data["principal"] = request.form["principal"]
        data["director"] = request.form["director"]
        data["school_timing"] = request.form["school_timing"]
        data["fees"] = request.form["fees"]
        data["teachers"]["chemistry"] = request.form["chemistry"]
        save_data(data)
        return "Saved successfully"

    return render_template_string(ADMIN_HTML, d=data)
