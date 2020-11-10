import requests

GITHUB_HEADERS = {"Accept": "application/vnd.github.v3+json"}

GITHUB_EXPERIMENTAL_HEADERS = {"Accept": "application/vnd.github.mercy-preview+json"}


def get_topics(repo_url):
    url = "{}/topics".format(repo_url)
    try:
        r = requests.get(url, headers=GITHUB_EXPERIMENTAL_HEADERS)

        return r.json().get("names")
    except:
        return []


def transform_github_repos(data):
    repos = map(
        lambda repo: {
            "language": repo.get("language"),
            "private": repo.get("private", False),
            "fork": repo.get("fork", False),
            "watchers": repo.get("watchers_count", 0),
            "topics": get_topics(repo.get("url")),
        },
        data,
    )

    return list(repos)


def aggragate_github_info(transformed_repos):
    aggragate = {
        "languages": [],
        "watchers": 0,
        "topics": [],
        "repos": {"original": 0, "forked": 0},
    }
    for repo in transformed_repos:
        if not repo["private"]:
            aggragate["languages"].append(repo.get("language"))
            aggragate["watchers"] += repo["watchers"]
            aggragate["topics"].extend(repo["topics"])
            if repo["fork"]:
                aggragate["repos"]["forked"] += 1
            else:
                aggragate["repos"]["original"] += 1

    cleaned_languages = set(aggragate["languages"])
    cleaned_languages.discard(None)
    cleaned_languages.discard("")
    aggragate["languages"] = list(cleaned_languages)

    aggragate["topics"] = list(set(aggragate["topics"]))

    return aggragate


def get_github_org_repos(org_name):
    url = "https://api.github.com/orgs/{}/repos".format(org_name)
    r = requests.get(url, headers=GITHUB_HEADERS)

    repos = r.json()
    if isinstance(repos, list):
        return repos
    raise Exception("Github API Error")


def get_org(org_name):
    """Takes github orginization name and returns a dictionary with useful
    information

    Args:
        team_name (string): github orginization name

    Returns:
        org (dict): dictionary with keys:

        languages ([string]): List of languages used in repos
        topics ([string]): List of repo topics
        watchers (integer): Total count of watchers/followers from all repos
        repos (dict): dictionary with keys:
            origional (integer): total number of origional repos
            forked (integer): total number of forked repos
    """
    # get raw data
    repos = get_github_org_repos(org_name)

    # transform raw data
    cleaned_repos = transform_github_repos(repos)

    # aggragate and return
    return aggragate_github_info(cleaned_repos)
