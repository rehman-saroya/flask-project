# This is the glossary_routes.py
import json
from flask import Blueprint, jsonify

glossary_routes = Blueprint("glossary_routes", __name__)

@glossary_routes.route("/api/glossary", methods=["GET"])
def glossary():
    with open("data/glossary.json") as f:
        terms = json.load(f)
    return jsonify(terms)
