import unittest
import responses
import json

from app import gitbucket_groups

from .mock_bitbucket_api import (
    MOCK_IRUNNEROAC_PAGE_1,
    MOCK_IRUNNEROAC_PAGE_2,
    MOCK_MAILCHIMP_REPOS_SINGLE_PAGE,
    MOCK_WATCHERS,
    MOCK_VALUES,
    SAMPLE_AGGRAGATED_REPOS,
)
from .mock_github_api import (
    MOCK_MAILCHIMP_REPOS,
    SAMPLE_TOPICS,
    SAMPLE_AGGRAGATED_REPOS,
)


class TestGithubAPI(unittest.TestCase):
    def test_merge(self):
        """Make sure basic happy path is golden"""
        team = {
            "languages": ["ruby", "dart", "php", "c"],
            "watchers": 3,
            "repos": {"original": 6, "forked": 7},
        }

        org = {
            "languages": ["PHP", "Objective-C"],
            "watchers": 6806,
            "topics": ["topic 1", "topic 2"],
            "repos": {"original": 3, "forked": 0},
        }

        expected = {
            "languages": ["PHP", "Objective-C", "ruby", "dart", "php", "c"],
            "watchers": 6809,
            "topics": ["topic 1", "topic 2"],
            "repos": {"original": 9, "forked": 7},
        }

        result = gitbucket_groups.merge_group(org, team)

        self.assertEqual(result["watchers"], expected["watchers"])
        self.assertDictEqual(result["repos"], expected["repos"])
        self.assertCountEqual(result["languages"], expected["languages"])
        self.assertCountEqual(result["topics"], expected["topics"])


if __name__ == "__main__":
    unittest.main()
