import unittest
import responses
import json

from app import bitbucket_api

from .mock_bitbucket_api import (
    MOCK_IRUNNEROAC_PAGE_1,
    MOCK_IRUNNEROAC_PAGE_2,
    MOCK_MAILCHIMP_REPOS_SINGLE_PAGE,
    MOCK_WATCHERS,
    MOCK_VALUES,
    SAMPLE_AGGRAGATED_REPOS,
)


class TestGithubAPI(unittest.TestCase):
    @responses.activate
    def test_get_bitbucket_team_repos(self):
        """Make sure basic happy path is golden"""
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/mailchimp",
            status=200,
            body=MOCK_MAILCHIMP_REPOS_SINGLE_PAGE,
        )

        result = bitbucket_api.get_bitbucket_team_repos("mailchimp")
        self.assertEqual(len(result), 10)

    @responses.activate
    def test_get_bitbucket_team_repos_is_recursive(self):
        """Make sure basic happy path is golden"""
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC",
            status=200,
            body=MOCK_IRUNNEROAC_PAGE_1,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/irunneroac?page=2",
            status=200,
            body=MOCK_IRUNNEROAC_PAGE_2,
        )

        result = bitbucket_api.get_bitbucket_team_repos("iRunnerOAC")
        self.assertEqual(len(result), 13)

    @responses.activate
    def test_get_bitbucket_teams_repos_github_failure(self):
        """Make sure a random exception is raised on
        any type of error
        """
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/mailchimp",
            status=500,
        )

        self.assertRaises(
            Exception, bitbucket_api.get_bitbucket_team_repos, "mailchimp"
        )

    @responses.activate
    def test_get_watcher_count_does_no_wrong(self):
        """Make sure a random exception is raised on
        any type of error
        """
        responses.add(responses.GET, "", status=500)

        result = bitbucket_api.get_watcher_count("")

        self.assertEqual(result, 0)

    @responses.activate
    def test_transform_bitbucket_repos_happy_path(self):
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/repo-23/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/repo12/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/mailchimp-api-php/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )

        result = bitbucket_api.transform_bitbucket_repos(json.loads(MOCK_VALUES))

        expected_1 = {"language": "php", "private": False, "fork": True, "watchers": 1}

        self.assertDictEqual(result[0], expected_1)

    def test_aggragate_bitbucket_info_happy_path(self):
        result = bitbucket_api.aggragate_bitbucket_info(SAMPLE_AGGRAGATED_REPOS)

        expected = {
            "languages": ["Python", "Objective-C", "Javascript"],
            "watchers": 35,
            "repos": {"original": 3, "forked": 2},
        }

        self.assertEqual(result["watchers"], expected["watchers"])
        self.assertDictEqual(result["repos"], expected["repos"])
        self.assertCountEqual(result["languages"], expected["languages"])

    @responses.activate
    def test_functional_happy_path(self):
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC",
            status=200,
            body=MOCK_IRUNNEROAC_PAGE_1,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/irunneroac?page=2",
            status=200,
            body=MOCK_IRUNNEROAC_PAGE_2,
        )

        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/repo-23/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/repo12/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )
        responses.add(
            responses.GET,
            "https://api.bitbucket.org/2.0/repositories/iRunnerOAC/mailchimp-api-php/watchers",
            status=200,
            body=MOCK_WATCHERS,
        )

        result = bitbucket_api.get_team("iRunnerOAC")

        expected = {
            "languages": ["ruby", "dart", "php", "c"],
            "watchers": 3,
            "repos": {"original": 6, "forked": 7},
        }

        self.assertEqual(result["watchers"], expected["watchers"])
        self.assertDictEqual(result["repos"], expected["repos"])
        self.assertCountEqual(result["languages"], expected["languages"])


if __name__ == "__main__":
    unittest.main()
