# Git Profile API Approach

## Requirements

1. Expose at least one RESTful endpoint that responds with a merged organization/team profile with data from both Github and Bitbucket
2. Provide a RESTful way for a client to provide the Github organization and Bitbucket team names to merge for the profile
3. The profile should include the following information (when available):
    1. Total number of public repos (seperate by original repos vs forked repos)
    2. Total watcher/follower count
    3. A list/count of languages used across all public repos
    4. A list/count of repo topics


## Breakdown

### Request

* [Get Group Profile](group.md) : `GET /api/groups/:name` 

## External Dependencies 

### Github


#### [Github Orgs Reference](https://docs.github.com/en/free-pro-team@latest/rest/reference/orgs)

* API Call: `https://api.github.com/orgs/{org}/repos`
* Aggregate keys needed from api call:
  1. `private` and `fork`
  2. `watcher_count`
     1. Total followers could be interperated as orginization followers found from `followers` in the org api call `https://api.github.com/orgs/{org}`
  3. `language` or `languages_url` (make the api call and get the list)
  4. `https://api.github.com/repos/{org}/{repo}/topics` with custom header: `Accept: application/vnd.github.mercy-preview+json`


### Bitbucket

[Bitbucket Teams Reference](https://developer.atlassian.com/bitbucket/api/2/reference/resource/teams)
[Bitbucket Repo Reference](https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories)

Bitbucket API is pagenated, so will need to crawl `next` links to get all repos

* Aggregate keys needed from api call:
  1. `[values].is_private` and `[values].parent` (if parent exists, then repo is a fork, i think)*
     1. Documentation unclear
  2. Request: `[values].links.watchers.href` -> size of request
  3. `[values].language`
  4. N/A - I don't think bitbucket has topics?

## Decisions

It was a super nice weekend, so in order to save time I decided MVP was happy path only. Next iteration would take into account clarifying questions. 

### Workflow

1. User Request
2. Poll Github
3. Poll Bitbucket
4. Data Tranformation
5. Return