from flask import Flask, render_template
from string import Template

app = Flask(__name__)
VIDEO_TEMPLATE = Template("""
      <iframe src="https://www.youtube.com/embed/${youtube_id}?${v_flags}" width="${v_width}" height="${v_height}" frameborder="0" allow="playsinline; accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      """)


@app.route("/hello")
def hello():
    return "Hello, World!"


# This represents the default page
@app.route("/")
# Default function upon accessing page
def home():
    return render_template("home.html")


@app.route('/echo/<text>')
def echo(text):
    return text


@app.route("/about")
# Default function upon accessing page
def about():
    return render_template("about.html")


@app.route('/video')
def video():
    url = "UEorWacjTwk"
    flags = "start=6;autoplay=1"
    return VIDEO_TEMPLATE.substitute(youtube_id=url, v_flags=flags, v_width="1000", v_height="640")


if __name__ == "__main__":
    # Display python errors
    app.run(debug=True)
