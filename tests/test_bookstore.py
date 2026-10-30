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
@pytest.mark.regression
def test_checkout_empty_cart_returns_none():
    """Author: Thant Thurein Lynn-[6805140024]. Cart.checkout on an empty cart should return None and must not record an order."""
    cart = Cart(Catalog())
    assert cart.checkout() is None
    assert cart.history() == []


@pytest.mark.regression
def test_login_accepts_password_with_symbols():
    """Author: Thant Thurein Lynn-[6805140024], with advice from Khant Naing Hein-[6805140019]. Users.login must accept the exact password the user registered with, including symbols."""
    users = Users()
    users.register("sam", "pass@word1")
    assert users.login("sam", "pass@word1") is True

@pytest.mark.regression
def test_login_rejects_password_with_extra_symbols():
    """Author: Khant Naing Hein-[6805140019]. Users.login must reject a wrong password even when it only differs from the real one by extra symbols; "abc123!!" must not log in the user whose password is "abc123"."""
    users = Users()
    users.register("kim", "abc123")
    assert users.login("kim", "abc123!!") is False
    assert users.login("kim", "abc123") is True

@pytest.mark.regression
def test_login_accepts_password_with_space():
    """Author: Khant Naing Hein-[6805140019]. Users.login must accept a registered password that contains a space; "my pass 1" must log in."""
    users = Users()
    users.register("lee", "my pass 1")
    assert users.login("lee", "my pass 1") is True

@pytest.mark.regression
def test_login_accepts_symbols_only_password():
    """Author: Khant Naing Hein-[6805140019]. Users.login must accept a password made only of symbols, and reject a different symbols-only one."""
    users = Users()
    users.register("zed", "!!!")
    assert users.login("zed", "!!!") is True
    assert users.login("zed", "!!") is False

@pytest.mark.smoke
def test_login_rejects_wrong_password():
    """Author: Khant Naing Hein-[6805140019]. Smoke: an existing user with a wrong password cannot log in, and an unknown user cannot log in."""
    users = Users()
    users.register("amy", "secret1")
    assert users.login("amy", "other22") is False
    assert users.login("nobody", "secret1") is False



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
@pytest.mark.slow
def test_catalog_search_with_many_products():
    """Author: Thant Sin Hein-[6805140004]. Slow: searching a catalog with 300000 products returns the correct single match."""
    # Slow because: 300,000 add_product calls, then search() lowercases and
    # scans all 300,000 titles.
    catalog = Catalog()
    for i in range(300000):
        catalog.add_product(i, f"Book {i}", 10)
    # Hand-computed: "book 299999" appears only in the title "Book 299999".
    assert catalog.search("Book 299999") == [299999]


@pytest.mark.slow
def test_catalog_repeated_searches():
    """Author: Thant Sin Hein-[6805140004]. Slow: repeated searches in a large catalog return the correct result every time."""
    # Slow because: 100 searches x 50,000 titles = 5,000,000 title checks.
    catalog = Catalog()
    for i in range(50000):
        catalog.add_product(i, f"Python Book {i}", 20)
    # Hand-computed: "python book 49999" matches only "Python Book 49999".
    for _ in range(100):
        assert catalog.search("Python Book 49999") == [49999]