"""Example Flask blueprint used by the scraper app."""

from flask import Blueprint, Response


example_blueprint = Blueprint("example_blueprint", __name__)


@example_blueprint.route("/")
def index() -> Response:
    """Return a simple plain-text response for the index route."""
    return Response("This is an example app\n", mimetype="text/plain")

