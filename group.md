# Get Group Profile

Aggragates Github Org and Bitbucket team information.

**URL** : `/api/groups/:name`

**URL Parameters** : `name=[string]` where `name` is the ID of the Org/Team. Name can be overridden in query parameters if needed. 

**Method** : `GET`

**Auth required** : NO

**Query Strings**: 
1. `githubOrgName=[string]` where `githubOrgName` overrides github org name
2. `bitbucketTeamName=[string]` where `bitbucketTeam` overrides bitbucket team name

## Success Response

**Condition** : If both bitbucket and github accounts exist.

**Code** : `200 OK`

**Content example**

```json
{
    "repos": {
        "original": 5,
        "forked": 4 
    },
    "watcher_follower_count": 20,
    "languages": [],
    "topics": []
}
```

## Error Responses

**Condition** : If Account does not exist in either bitbucket or github.

**Code** : `404 NOT FOUND`

**Content** : `{}`

### Or

**Condition** : If requests to either bitbucket or github result in network error.

**Code** : `500 Internal Server Error`

**Content** :

```json
{"detail": "Try again Later"}
```

## Notes

Error handling should be better, but it is super nice outside.