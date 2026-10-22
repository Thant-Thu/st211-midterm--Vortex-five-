"""Your test suite. Write smoke, regression, and slow tests here.

Every test MUST carry exactly one marker (@pytest.mark.smoke / regression /
slow) and name its author in the docstring, e.g.:

    @pytest.mark.smoke
    def test_login_works():
        '''Author: <name>. Smoke test for login.'''

Run:  pytest            (all)     pytest -m smoke     pytest -m regression
"""
import pytest
from bookstore_app import Users, Catalog, Cart


@pytest.mark.smoke
def test_example_register():
    """Author: <example>. Smoke: a new user can register."""
    assert Users().register("newuser", "password123") is True


# ---- YOUR SMOKE TESTS (at least 5) ----
@pytest.mark.smoke
def test_login_works():
    """Author: Thant Thurein Lynn-[6805140024]. Smoke: a registered user can log in, and a wrong password is rejected."""
    users = Users()
    users.register("alice", "password123")
    assert users.login("alice", "password123") is True
    assert users.login("alice", "wrongpass") is False

# ---- YOUR REGRESSION TESTS (the bug hunt) ----

# ---- YOUR SLOW TESTS (at least 2) ----
