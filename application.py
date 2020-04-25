from flask import Flask, render_template
from get_data import get_teams

# Create an instance of our Flask app.
app = Flask(__name__)

# Set route
@app.route('/')
def index():
    return render_template('index.html', teams=get_teams())


if __name__ == "__main__":
    app.run(debug=True)
