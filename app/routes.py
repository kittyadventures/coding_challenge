import logging
import json
from flask import Flask, logging as flask_logging, request, Response
from flasgger import Swagger


from .gitbucket_groups import get_gitbucket_group

app = Flask("user_profiles_api")
logger = flask_logging.create_logger(app)
logger.setLevel(logging.INFO)

swagger = Swagger(app)


@app.route("/health-check", methods=["GET"])
def health_check():
    """Simple Health Check
    ---
    responses:
      200:
        description: Returns 200 if route can be accessed
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/api/groups/<name>", methods=["GET"])
def get_group(name):
    """Aggragates Github Org and Bitbucket team information.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
      - name: githubOrgName
        in: query
        type: string
        required: false
      - name: bitbucketTeamName
        in: query
        type: string
        required: false
    responses:
      200:
        description: Json of things
    """

    githubOrgName = name
    bitbucketTeamName = name
    if request.args.get("githubOrgName"):
        githubOrgName = request.args.get("githubOrgName")
    if request.args.get("bitbucketTeamName"):
        githubOrgName = request.args.get("bitbucketTeamName")

    data = get_gitbucket_group(githubOrgName, bitbucketTeamName)

    app.logger.info(data)
    return Response(json.dumps(data), status=200)
