import json
import math
import os
from datetime import datetime

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from linkedlist import LinkedList

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# =====================================================================
#  ✏️  EDIT THIS SECTION — put your own personal data here.
#  Every page (profile, contact, home, footer) reads from these values.
# =====================================================================
PROFILE = {
    "name": "Anika Sophia C. Basa",
    "first_name": "Anika",
    "initials": "AB",
    "tagline": "Computer Engineering student who loves solving problems, building things, and making music",
    "roles": ["Computer Engineering Student", "Python Developer", "Problem Solver", "Musician & Gamer"],
    "about": (
        "I'm a 2nd year Computer Engineering student at the Polytechnic University of the Philippines. "
        "I love turning tricky problems into clean, working solutions, whether that's a Python program, "
        "a web page, or a data structure. Outside of code, I'm usually singing, dancing, playing an "
        "instrument, or gaming. I believe creativity and logic work best together."
    ),
    "section": "BSCPE 2-3",
    "course": "Bachelor of Science in Computer Engineering",
    "year": "2nd Year",
    "school": "Polytechnic University of the Philippines",
    "subject": "Data Structures and Algorithms",
    "motto": "Problems are not stop signs, they are guidelines.",
    "sayings": [
        ("Problems are not stop signs, they are guidelines.", "Robert H. Schuller"),
        ("Talk is cheap. Show me the code.", "Linus Torvalds"),
        ("The best way to predict the future is to invent it.", "Alan Kay"),
    ],
    "skills": [
        ("HTML & CSS", 80),
        ("Python", 70),
        ("C / C++", 60),
        ("Git & GitHub", 50),
        ("Arduino & Microcontrollers", 60),
    ],
    "interests": ["Gaming 🎮", "Music 🎵", "Singing 🎤", "Dancing 💃", "Playing Instruments 🎸"],
    "timeline": [
        ("2026", "Learning Data Structures & Algorithms",
         "Building linked lists and more, and turning this Flask lab into my own personal portfolio."),
        ("2025", "Started Computer Engineering at PUP",
         "Began my BS Computer Engineering journey at the Polytechnic University of the Philippines."),
        ("Always", "Creative at heart",
         "Singing, dancing and playing instruments keep me balanced and inspire the way I solve problems."),
    ],
    # Contact
    "email": "anikasophia.cabigbasa@gmail.com",
    "phone": "0968 523 0711",
    "location": "Cainta, Rizal, Philippines",
    "socials": [
        ("GitHub", "https://github.com/anikasophiabasa", "github"),
        ("Facebook", "https://www.facebook.com/anikasophia.cabigbasa", "facebook"),
    ],
}

WORKS = [
    {"title": "toUpperCase", "desc": "Turn any text into UPPERCASE instantly.",
     "url": "works", "icon": "Aa", "tag": "Strings"},
    {"title": "Area of a Circle", "desc": "Enter a radius, get area, diameter & circumference.",
     "url": "acircle", "icon": "◯", "tag": "Math"},
    {"title": "Area of a Triangle", "desc": "Use base × height or the three sides (Heron's formula).",
     "url": "atriangle", "icon": "△", "tag": "Math"},
    {"title": "Linked List", "desc": "An interactive, animated singly linked list.",
     "url": "linkedlist_page", "icon": "⛓", "tag": "Data Structures"},
]


@app.context_processor
def inject_globals():
    photo = os.path.exists(os.path.join(app.static_folder, "images", "profile.jpg"))
    return {"me": PROFILE, "works_list": WORKS, "has_photo": photo, "year": datetime.now().year}


# ------------------------------- pages -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "message": request.form.get("message", "").strip(),
        }
        if entry["name"] and entry["email"] and entry["message"]:
            with open("messages.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
            flash("Thanks for reaching out! Your message has been saved.", "success")
        else:
            flash("Please fill in all the fields.", "error")
        return redirect(url_for("contact") + "#form")
    return render_template("contact.html")


# --------------------------- programming works ---------------------------
@app.route("/works", methods=["GET", "POST"])
def works():
    result, text = None, ""
    if request.method == "POST":
        text = request.form.get("inputString", "")
        result = text.upper()
    return render_template("touppercase.html", result=result, text=text)


@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    data, error, radius = None, None, ""
    if request.method == "POST":
        radius = request.form.get("radius", "").strip()
        try:
            r = float(radius)
            if r < 0 or not math.isfinite(r):
                raise ValueError
            data = {"area": math.pi * r * r, "diameter": 2 * r, "circumference": 2 * math.pi * r}
        except ValueError:
            error = "Please enter a valid, non-negative number for the radius."
    return render_template("circle.html", data=data, error=error, radius=radius)


@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    data, error, mode = None, None, request.form.get("mode", "bh")
    form = request.form
    if request.method == "POST":
        try:
            if mode == "bh":
                b, h = float(form.get("base", "")), float(form.get("height", ""))
                if b < 0 or h < 0:
                    raise ValueError("Base and height must not be negative.")
                data = {"area": 0.5 * b * h, "formula": f"½ × {b:g} × {h:g}"}
            else:
                a, b, c = (float(form.get(k, "")) for k in ("side_a", "side_b", "side_c"))
                if min(a, b, c) <= 0:
                    raise ValueError("All sides must be greater than zero.")
                if a + b <= c or a + c <= b or b + c <= a:
                    raise ValueError("Those sides can't form a triangle (triangle inequality).")
                s = (a + b + c) / 2
                data = {"area": math.sqrt(s * (s - a) * (s - b) * (s - c)),
                        "formula": f"√[s(s−a)(s−b)(s−c)], s = {s:g}", "perimeter": a + b + c}
        except ValueError as e:
            msg = str(e)
            error = msg if "must" in msg or "can't" in msg else "Please enter valid numbers in every field."
    return render_template("triangle.html", data=data, error=error, mode=mode, form=form)


# ------------------------------ linked list ------------------------------
ll = LinkedList()
for v in ("Flask", "Python", "Portfolio"):
    ll.insert_tail(v)


def _snapshot(message, highlight=None, ok=True):
    return jsonify({"ok": ok, "message": message, "nodes": ll.to_list(),
                    "size": ll.size, "highlight": highlight})


@app.route("/works/linkedlist")
def linkedlist_page():
    return render_template("linkedlist.html")


@app.route("/api/linkedlist", methods=["GET"])
def ll_state():
    return _snapshot("Linked list loaded.")


@app.route("/api/linkedlist/<op>", methods=["POST"])
def ll_op(op):
    body = request.get_json(silent=True) or {}
    value = str(body.get("value", "")).strip()
    raw_index = body.get("index", "")
    try:
        needs_value = {"insert_head", "insert_tail", "insert_at", "delete_value", "search"}
        if op in needs_value and not value:
            raise ValueError("Please enter a value.")
        if op in {"insert_at", "delete_at"}:
            try:
                index = int(raw_index)
            except (TypeError, ValueError):
                raise ValueError("Please enter a whole number for the index.")

        if op == "insert_head":
            i = ll.insert_head(value); return _snapshot(f'Inserted "{value}" at the head.', i)
        if op == "insert_tail":
            i = ll.insert_tail(value); return _snapshot(f'Inserted "{value}" at the tail.', i)
        if op == "insert_at":
            i = ll.insert_at(index, value); return _snapshot(f'Inserted "{value}" at index {i}.', i)
        if op == "delete_head":
            v = ll.delete_at(0); return _snapshot(f'Deleted head node "{v}".')
        if op == "delete_tail":
            v = ll.delete_at(ll.size - 1) if ll.size else ll.delete_at(0)
            return _snapshot(f'Deleted tail node "{v}".')
        if op == "delete_at":
            v = ll.delete_at(index); return _snapshot(f'Deleted "{v}" at index {index}.')
        if op == "delete_value":
            i = ll.delete_value(value); return _snapshot(f'Deleted "{value}" (was at index {i}).')
        if op == "search":
            i = ll.search(value)
            if i == -1:
                return _snapshot(f'"{value}" was not found.', None, ok=False)
            return _snapshot(f'Found "{value}" at index {i}.', i)
        if op == "reverse":
            ll.reverse(); return _snapshot("List reversed.")
        if op == "clear":
            ll.clear(); return _snapshot("List cleared.")
        return _snapshot("Unknown operation.", None, ok=False)
    except (ValueError, IndexError) as e:
        return _snapshot(str(e), None, ok=False)


if __name__ == "__main__":
    app.run(debug=True)
