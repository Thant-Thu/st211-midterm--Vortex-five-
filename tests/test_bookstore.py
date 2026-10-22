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


@pytest.mark.smoke
def test_add_product_works():
    """Author: Thant Thurein Lynn-[6805140024]. Smoke: a product added to the catalog can be found."""
    catalog = Catalog()
    catalog.add_product(1, "Python Basics", 25)
    assert 1 in catalog.products
    assert catalog.products[1]["title"] == "Python Basics"
    assert catalog.search("Python") == [1]


@pytest.mark.smoke
def test_add_to_cart_works():
    """Author: Thant Thurein Lynn-[6805140024]. Smoke: a product added to the cart appears in it, and an unknown product is rejected."""
    catalog = Catalog()
    catalog.add_product(1, "Python Basics", 25)
    cart = Cart(catalog)
    assert cart.add(1) is True
    assert cart.items == [1]
    assert cart.add(999) is False
    assert cart.items == [1]

# ---- YOUR REGRESSION TESTS (the bug hunt) ----


# ---- YOUR SLOW TESTS (at least 2) ----
