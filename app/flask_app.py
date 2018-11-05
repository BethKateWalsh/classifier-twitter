from flask import Flask, render_template, request, url_for, flash
from create_report import start_script

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    error = None
    try:
        if request.method == "POST":
            console.log("Started...")
            attempted_account = request.form['account']

            if attempted_account != "":
                console.log("Not equal to 0")
                start_script(attempted_account)

            else:
                console.log("Equal to 0")
                return render_template('home.html', error = error)

        return render_template('home.html')

    except Exception as e:
        return render_template('home.html', error = error)


if __name__ == '__main__':
    app.run(debug=True)
