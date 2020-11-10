from .github_api import get_org
from .bitbucket_api import get_team


def merge_group(org, team):
    languages = []
    languages.extend(org.get("languages", []))
    languages.extend(team.get("languages", []))

    languages = list(set(languages))

    topics = org.get("topics")

    watchers = org.get("watchers", 0) + team.get("watchers", 0)

    origional = org.get("repos", {}).get("original", 0) + team.get("repos", {}).get(
        "original", 0
    )
    fork = org.get("repos", {}).get("forked", 0) + team.get("repos", {}).get(
        "forked", 0
    )

    return {
        "languages": languages,
        "watchers": watchers,
        "topics": topics,
        "repos": {"original": origional, "forked": fork},
    }


def get_gitbucket_group(github_org_name, bitbucket_team_name):
    """Takes github orginization name and bitbucket team name, makes API calls
    to get information on repos and returns in a unified format

    Args:
        github_org_name (string): github orginization name
        bitbucket_team_name (string): bitbucket team name

    Returns:
        group (dict): dictionary with keys:

            languages ([string]): List of languages used in repos
            topics ([string]): List of repo topics
            watchers (integer): Total count of watchers/followers from all repos
            repos (dict): dictionary with keys:
                origional (integer): total number of origional repos
                forked (integer): total number of forked repos
    """
    org = get_org(github_org_name)
    team = get_team(bitbucket_team_name)

    return merge_group(org, team)
