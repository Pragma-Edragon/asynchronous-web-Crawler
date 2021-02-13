from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

app.secret_key = "QWERTYUIOP[QWERTYUIOP["


@app.errorhandler
def errorPage(error):
    print(error)
    return "Error", 500


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/test", methods=['GET', 'POST'])
def testFunc():
    return render_template("test.html")


@app.route("/test/<int:value>", methods=['GET', 'POST'])
def testFuncInt(value):
    if value == 6:
        return redirect(url_for("testFunc", value=10))
    return "Hello, user:" + str(value)
