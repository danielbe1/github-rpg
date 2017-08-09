from unittest import TestCase

from github.github_issue_object import GithubIssueObject


class TestGithubIssueObject(TestCase):
    def test_get_difficulty(self):
        self.assertEqual(GithubIssueObject.get_difficulty('difficulty: trivial'), 0.1, 'difficulty should have been 0.5')
        self.assertEqual(GithubIssueObject.get_difficulty('difficulty:easy'), 1, 'difficulty should have been 1')
        self.assertEqual(GithubIssueObject.get_difficulty('difficulty:  medium'), 1.5, 'difficulty should have been 1.5')
        self.assertEqual(GithubIssueObject.get_difficulty('difficulty: hard'), 2, 'difficulty should have been 2')
        self.assertEqual(GithubIssueObject.get_difficulty('difficulty: none'), 1, 'difficulty should have been 1')
        self.assertEqual(GithubIssueObject.get_difficulty(''), 1, 'difficulty should have been 1')
