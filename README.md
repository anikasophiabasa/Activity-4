# Personal Portfolio — Flask

A personal portfolio web application built with **Flask** for *Laboratory Exercise 4*
(Data Structures and Algorithms) at the Polytechnic University of the Philippines.

**Author:** Anika Sophia C. Basa — BSCPE 2-3

## Features

- Responsive navigation bar on every page
- Home, Profile and Contact pages with a dark / light theme toggle
- Animated UI: typing effect, scroll reveal, skill bars, cursor glow
- Programming works:
  - **toUpperCase** — converts text to uppercase
  - **Area of a Circle** — area, diameter and circumference
  - **Area of a Triangle** — base × height, or three sides (Heron's formula)
  - **Linked List** — interactive singly linked list (insert, delete, search, reverse, clear)

## Project Structure

```
├── app.py              # Flask routes and personal profile data
├── linkedlist.py       # Node and LinkedList classes
├── requirements.txt    # Python dependencies
├── templates/          # HTML pages (Jinja2)
└── static/
    ├── css/style.css   # Styling
    └── js/             # main.js, linkedlist.js
```

## How to Run

1. Install Python 3.9 or newer.
2. Install the dependency:
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   python app.py
   ```
4. Open <http://127.0.0.1:5000> in your browser.

## Customize

- Edit the `PROFILE` dictionary at the top of `app.py` to change personal information.
- Add a photo by saving it as `static/images/profile.jpg`.
