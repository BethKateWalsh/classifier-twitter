from flask import Flask, render_template, request, url_for, flash
import create_report
from flask_debugtoolbar import DebugToolbarExtension
from flask import send_from_directory

app = Flask(__name__)
filename = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/handle_data", methods=['GET', 'POST'])
def handle_data():
    text = request.form['accountinput']
    preprocessed_text = text.lower()
    filename = create_report.start_script(preprocessed_text)
    path = "reports/" + filename
    return send_from_directory(directory='.', filename=path)

if __name__ == '__main__':
    app.run(debug=True)
