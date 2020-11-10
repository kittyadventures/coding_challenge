import requests


def get_watcher_count(watchers_href):
    try:
        r = requests.get(watchers_href)
        return r.json().get("size")
    except:
        return 0


def get_all_bitbucket_repos(url):
    r = requests.get(url)
    repos = r.json()

    all_repos = []

    if isinstance(repos["values"], list):
        all_repos.extend(repos["values"])
    else:
        raise Exception("Github API Error")

    if repos.get("next", False):
        all_repos.extend(get_all_bitbucket_repos(repos.get("next")))

    return all_repos


def get_bitbucket_team_repos(team_name):
    url = "https://api.bitbucket.org/2.0/repositories/{}".format(team_name)

    return get_all_bitbucket_repos(url)


def transform_bitbucket_repos(values):
    repos = map(
        lambda repo: {
            "language": repo.get("language", False),
            "private": repo.get("is_private", False),
            "fork": "parent" in repo,
            "watchers": get_watcher_count(
                repo.get("links", {}).get("watchers", {}).get("href")
            ),
        },
        values,
    )

    return list(repos)


def aggragate_bitbucket_info(transformed_repos):
    aggragate = {"languages": [], "watchers": 0, "repos": {"original": 0, "forked": 0}}
    for repo in transformed_repos:
        if not repo["private"]:
            aggragate["languages"].append(repo.get("language"))
            aggragate["watchers"] += repo["watchers"]
            if repo["fork"]:
                aggragate["repos"]["forked"] += 1
            else:
                aggragate["repos"]["original"] += 1

    cleaned_languages = set(aggragate["languages"])
    cleaned_languages.discard(None)
    cleaned_languages.discard("")
    aggragate["languages"] = list(cleaned_languages)

    return aggragate


def get_team(team_name):
    """Takes bitbucket team name and returns a dictionary with useful
    information

    Args:
        team_name (string): bitbucket team name

    Returns:
        team (dict): dictionary with keys:

        languages ([string]): List of languages used in repos
        watchers (integer): Total count of watchers/followers from all repos
        repos (dict): dictionary with keys:
            origional (integer): total number of origional repos
            forked (integer): total number of forked repos
    """
    # get raw data
    repos = get_bitbucket_team_repos(team_name)

    # transform raw data
    cleaned_repos = transform_bitbucket_repos(repos)

    # aggragate and return
    return aggragate_bitbucket_info(cleaned_repos)
