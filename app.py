from flask import Flask, render_template, request
import os
import asyncio
from playwright_script import run_booking

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'user_data'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["user_file"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            data = {
                "level": request.form["level"],
                "location": request.form["location"],
                "start_date": request.form["start_date"],
                "end_date": request.form["end_date"],
                "hour": int(request.form["hour"]),
                "minute": int(request.form["minute"]),
                "user_file": filepath,
            }

            asyncio.run(run_booking(data))
            return render_template("result.html", msg="✅ Booking started. Check terminal/logs.")
    return render_template("index.html")
