from flask import Flask, render_template, request, redirect, url_for
import threading

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])  ## This is the firs page you see when going to the url
def FrontPage():
    if request.method == 'POST':
        ##here send info to main script
        
        return redirect(url_for("RunPage"))  ## If something gets posted on this page, redirect to RunPage()


    return render_template("FrontPage.html") ## When page is just opened show FrontPage.html


@app.route("/Run", methods=["POST","GET"])
def RunPage():
    if request.method == 'POST':
        ##here send info to main script
        return redirect(url_for("ReportPage")) ## If something gets posted to this page, redirect to ReportPage()

    return render_template("RunPage.html") ## When page is just opened show RunPage.html


@app.route("/Report", methods=["POST","GET"])
def ReportPage():
    if request.method == 'POST':
        ##here send info to main script
        return redirect(url_for("RunPage"))  ## You get it by now
    return render_template("ReportPage.html")


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=1337, debug=True)  ## hosts script on own ip on port 1337, with debugging on for console