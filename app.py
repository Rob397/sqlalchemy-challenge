from flask import Flask, jsonify
# example dictionary to jsonify
justice_league_dict = [
    {"superhero": "Aquaman", "real_name": "Arthur Curry"},
    {"superhero": "Batman", "real_name": "Bruce Wayne"},
]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("")
def example_():
    """Return the justice league data as json"""

    return jsonify(justice_league_dict)