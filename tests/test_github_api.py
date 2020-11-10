import unittest
import responses
import json

from unittest import mock
from app import github_api

from .mock_github_api import (
    MOCK_MAILCHIMP_REPOS,
    SAMPLE_TOPICS,
    SAMPLE_AGGRAGATED_REPOS,
)


class TestGithubAPI(unittest.TestCase):
    @responses.activate
    def test_get_github_org_repos(self):
        """Make sure basic happy path is golden"""
        responses.add(
            responses.GET,
            "https://api.github.com/orgs/mailchimp/repos",
            status=200,
            body=MOCK_MAILCHIMP_REPOS,
        )

        result = github_api.get_github_org_repos("mailchimp")

        self.assertEqual(len(result), 3)

    @responses.activate
    def test_get_github_org_repos_github_failure(self):
        """Make sure a random exception is raised on
        any type of error
        """
        responses.add(
            responses.GET, "https://api.github.com/orgs/mailchimp/repos", status=500
        )

        self.assertRaises(Exception, github_api.get_github_org_repos, "mailchimp")

    @responses.activate
    def test_get_topics_always_wins(self):
        responses.add(responses.GET, "https://winner/topics", status=500)

        result = github_api.get_topics("https://winner")

        self.assertEqual(len(result), 0)

    @responses.activate
    def test_get_topics_happy_path(self):
        responses.add(
            responses.GET, "https://winner/topics", status=200, body=SAMPLE_TOPICS
        )

        result = github_api.get_topics("https://winner")

        self.assertEqual(result[0], "topic 1")

    @responses.activate
    def test_transform_github_repos_happy_path(self):
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/ChimpKit2/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/email-blueprints/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/MailChimp.tmbundle/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )

        result = github_api.transform_github_repos(json.loads(MOCK_MAILCHIMP_REPOS))

        expected_1 = {
            "language": "Objective-C",
            "private": False,
            "fork": False,
            "watchers": 29,
            "topics": ["topic 1", "topic 2"],
        }

        self.assertDictEqual(result[0], expected_1)

    def test_aggragate_github_info_happy_path(self):
        result = github_api.aggragate_github_info(SAMPLE_AGGRAGATED_REPOS)

        expected = {
            "languages": ["Python", "Objective-C", "Javascript"],
            "watchers": 35,
            "topics": ["topic 1", "topic 2", "topic 3", "topic 4"],
            "repos": {"original": 3, "forked": 2},
        }

        self.assertEqual(result["watchers"], expected["watchers"])
        self.assertDictEqual(result["repos"], expected["repos"])
        self.assertCountEqual(result["languages"], expected["languages"])
        self.assertCountEqual(result["topics"], expected["topics"])

    @responses.activate
    def test_functional_happy_path(self):
        responses.add(
            responses.GET,
            "https://api.github.com/orgs/mailchimp/repos",
            status=200,
            body=MOCK_MAILCHIMP_REPOS,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/ChimpKit2/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/email-blueprints/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/mailchimp/MailChimp.tmbundle/topics",
            status=200,
            body=SAMPLE_TOPICS,
        )

        result = github_api.get_org("mailchimp")

        expected = {
            "languages": ["PHP", "Objective-C"],
            "watchers": 6806,
            "topics": ["topic 1", "topic 2"],
            "repos": {"original": 3, "forked": 0},
        }

        self.assertEqual(result["watchers"], expected["watchers"])
        self.assertDictEqual(result["repos"], expected["repos"])
        self.assertCountEqual(result["languages"], expected["languages"])
        self.assertCountEqual(result["topics"], expected["topics"])


if __name__ == "__main__":
    unittest.main()
