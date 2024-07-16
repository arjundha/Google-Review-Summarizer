from flask import Flask, render_template, request
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


@app.route("/summarize")
async def get_summary():
    name = request.args.get("name")
    location = request.args.get("location")
    result = await get_summarized_reviews(name, location)
    html_result = result
    return render_template(
        "summarize.html", name=name, location=location, summary=html_result, test="test"
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
