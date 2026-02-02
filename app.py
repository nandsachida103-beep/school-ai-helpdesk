from flask import Flask, render_template, request, jsonify
from data import school_data

app = Flask(__name__)

def reply(msg):
    msg = msg.lower()

    if "school name" in msg:
        return school_data["school_name"]

    if "timing" in msg or "school time" in msg:
        return school_data["timing"]

    if "director" in msg:
        return school_data["management"]["director"]

    if "principal" in msg:
        return school_data["management"]["principal"]

    if "vice" in msg:
        return school_data["management"]["vice_principal"]

    if "system manager" in msg:
        return school_data["management"]["system_manager"]

    for subject, data in school_data["teachers"].items():
        if subject in msg and "teacher" in msg:
            if isinstance(data, dict):
                return f"{data['name']} ({data.get('qualification','')})"
            return data["name"]

    if "fee" in msg:
        return f"Class 11 fee is {school_data['class_11']['fee']}"

    if "boys" in msg:
        return ", ".join(school_data["class_11"]["boys"])

    if "girls" in msg:
        return ", ".join(school_data["class_11"]["girls"])

    if "feature" in msg or "facility" in msg:
        return ", ".join(school_data["features"])

    if "house" in msg:
        return ", ".join(school_data["houses"])

    if "sport" in msg or "game" in msg:
        return ", ".join(school_data["sports"])

    if "activity" in msg or "competition" in msg:
        return ", ".join(school_data["activities"])

    if "admission" in msg or "document" in msg:
        return ", ".join(school_data["admission_documents"])

    return "Please ask about teachers, fees, timing, admission, sports, or school details."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    return jsonify({"reply": reply(user_msg)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
