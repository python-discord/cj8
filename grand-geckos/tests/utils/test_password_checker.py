from grand_geckos.utils import check_password
from password_strength import tests

import pytest

class TestCheckPassword:

    def test_popular_passwords(self):
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("password"))
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("12345678"))
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("87654321"))
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("admin"))

    def test_password_variations(self):
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("p@ssw0rd"))
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("J0hnny"))
        assert any(isinstance(issue.test, tests.Strength) for issue in check_password("adminadminadmin"))

    def test_good_passwords(self):
        assert len(check_password("Gr@atP@ssw0rd")) == 0
        # TODO: Add more tests for good/bad passwords to help refine the checker
