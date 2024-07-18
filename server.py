import sys
from flask import Flask, redirect, render_template, request, url_for
from flask_misaka import Misaka
from summarize import get_summarized_reviews
from waitress import serve

app = Flask(__name__)
Misaka(app)
port = 5000


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["GET"])
async def get_summary():
    name = request.args.get("name")
    location = request.args.get("location")
    try:
        result = await get_summarized_reviews(name, location)
    except:
        error = sys.exc_info()[1]
        return redirect(url_for("error", message=error))

    return redirect(
        url_for(
            "summary",
            name=name,
            location=location,
            result=result.get("summary"),
        )
    )


@app.route("/summary/<name>/<location>/<result>", methods=["GET"])
def summary(name, location, result):
    return render_template(
        "summarize.html",
        name=name,
        location=location,
        summary=result,
    )


@app.route("/error/<message>", methods=["GET"])
def error(message):
    return render_template("error.html", message=message)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
