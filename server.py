import os
import sys
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_misaka import Misaka
from waitress import serve
from summarize import get_summarized_reviews, get_summary_purely_from_ai

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
    checkbox = request.args.get("checkbox")
    try:
        if checkbox:
            app.logger.warning(
                f"Getting summarized reviews for {name} in {location} purely from AI"
            )
            result = await get_summary_purely_from_ai(name, location)
        else:
            app.logger.warning(f"Getting summarized reviews for {name} in {location}")
            result = await get_summarized_reviews(name, location)
    except:
        error = sys.exc_info()[1]
        app.logger.error(
            f"Error: {error}. Tried to get summarized reviews for {name} in {location}"
        )
        return redirect(url_for("error", message=error))

    return redirect(
        url_for(
            "summary",
            name=name,
            location=location,
            result=result if checkbox else result.get("summary"),
        )
    )


@app.route("/summary/<name>/<location>/<result>", methods=["GET"])
def summary(name, location, result):
    app.logger.warning(f"Summarized reviews for {name} in {location}")
    return render_template(
        "summarize.html",
        name=name,
        location=location,
        summary=result,
    )


@app.route("/error/<message>", methods=["GET"])
def error(message):
    app.logger.warning(f"Redirected user to error page with message: {message}")
    return render_template("error.html", message=message)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, threads=100)
