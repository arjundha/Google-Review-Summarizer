from flask import Flask, render_template, request
from summarize import get_summarized_reviews
from waitress import serve

app = Flask(__name__)
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
    return render_template(
        "summarize.html", name=name, location=location, summary=result
    )


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
