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

@pytest.mark.smoke
def test_checkout_works():
    """Author: Thant Thurein Lynn-[6805140024]. Smoke: checkout returns an order containing the item added and empties the cart."""
    catalog = Catalog()
    catalog.add_product(1, "Python Basics", 25)
    cart = Cart(catalog)
    cart.add(1)
    order = cart.checkout()
    assert order == [1]
    assert cart.items == []
    assert cart.history() == [[1]]

@pytest.mark.smoke
def test_register_works():
    """Author: Thant Thurein Lynn-[6805140024]. Smoke: a new user can register, a duplicate is rejected, and the user can log in."""
    users = Users()
    assert users.register("bob", "secret123") is True
    assert users.register("bob", "other456") is False
    assert users.login("bob", "secret123") is True

# ---- YOUR REGRESSION TESTS (the bug hunt) ----

# ---- BONUS: regression + slow ----
# Why regression: it pins down one specific defect in Cart.import_products,
#   the number of products it reports as imported.
# Why slow: it bulk-imports 200,000 products one by one, so it takes
#   far longer than the smoke suite.
# Where in CI: not on every push (too slow); it runs in the nightly full-suite
#   job, where it guards against that bug coming back at scale.
@pytest.mark.regression
@pytest.mark.slow
def test_large_import_reports_correct_count():
    """Author: Thant Thurein Lynn-[6805140024]. Cart.import_products must return exactly how many products it imported; expected 200000 for a 200000-item list."""
    total = 200000
    catalog = Catalog()
    cart = Cart(catalog)
    products = [(i, f"Book {i}", 10) for i in range(total)]
    imported = cart.import_products(products)
    assert len(catalog.products) == total
    assert imported == total


# ======== PERSON 3: users.py regression tests (add below this line only) ========



# ======== PERSON 2: catalog.py regression tests (add below this line only) ========
@pytest.mark.regression
def test_search_is_case_insensitive():
    """Author: Thant Thurein Lynn-[6805140024]. Catalog.search should find a title regardless of the keyword's letter case; search("python") must find "Python Basics"."""
    catalog = Catalog()
    catalog.add_product(1, "Python Basics", 25)
    assert catalog.search("python") == [1]



# ======== PERSON 4: cart.py regression tests (add below this line only) ========
@pytest.mark.regression
def test_import_products_returns_correct_count():
    """Author: Zaw Moe Aung-[6805140020]. Cart.import_products should return the exact number of products imported."""
    catalog = Catalog()
    cart = Cart(catalog)
    products = [
        (1, "Book A", 10),
        (2, "Book B", 20),
    ]

    imported = cart.import_products(products)

    assert len(catalog.products) == 2
    assert imported == 2

@pytest.mark.regression
def test_total_includes_last_cart_item():
    """Author: Zaw Moe Aung-[6805140020]. Cart.total must include the price of every item."""
    catalog = Catalog()
    catalog.add_product(1, "Book A", 100)
    catalog.add_product(2, "Book B", 200)
    catalog.add_product(3, "Book C", 300)

    cart = Cart(catalog)
    cart.add(1)
    cart.add(2)
    cart.add(3)

    assert cart.total() == 600



# ---- YOUR SLOW TESTS (at least 2) ----
# ======== PERSON 2: slow tests (add below this line only) ========
