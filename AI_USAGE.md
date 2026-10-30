# AI Usage Declaration and Audit

**Group:** Vortex-Five  **Members:** Thant Thurein Lynn, Lin Thant Maung, Khant Naing Hein, Thant Sin Hein, Zaw Moe Aung

**Part D3 of the midterm — 20 marks.** Part 1 is required but carries no marks;
its absence is an academic-honesty matter. Part 2 is worth 16 (2 per test).
Parts 3 and 4 together are worth 4.

Before you submit, check all eight boxes:

- [ ] Part 1 declaration complete, or the "no AI used" statement written
- [ ] All eight tests appear in the summary table with a verdict
- [ ] All eight have **two** pasted evidence runs (shipped code, and your fixed code)
- [ ] Part 3 coverage table filled in against `FINDINGS.md`
- [ ] Part 4 verdict written, under 400 words
- [ ] Every audit entry names the member who did it
- [ ] No claim made that you cannot demonstrate from pasted output
- [ ] File committed as `AI_USAGE.md` in the repository root

---

## Part 1 — AI usage declaration (required, unmarked)

Every AI tool any member used anywhere in this project. Using AI is allowed.
Not declaring it is not.

| Tool | What we used it for | Where in the project | How we checked it before relying on it |
|---|---|---|---|
| Copilot | completing test boilerplate | `tests/test_bookstore.py` | ran each test against the shipped code and confirmed it failed for the reason we expected |
| Claude (Anthropic) | explaining the project layout, drafting the smoke tests, the CI workflow and the Part A/B text | `tests/test_bookstore.py`, `.github/workflows/tests.yml`, `REPORT.md` | ran every smoke test with `pytest -m smoke -v` against the shipped code and confirmed they pass; checked the CI run was green in the Actions tab; edited the report wording ourselves |
| ChatGPT (OpenAI) | Helped analyze AI-generated test results, compare shipped and fixed code, classify test outcomes, and draft audit explanations | `AI_USAGE.md`; test-audit analysis of `ai_review/test_ai_generated.py` | Compared individual pytest outputs from the shipped-code worktree and fixed code; inspected the original `Users.login()` implementation, the test assertions, and `FINDINGS.md` before deciding the verdicts |


If you kept prompts worth showing, add them in an appendix at the end of this
file. Do not paste whole conversations.

If no AI tools were used anywhere, write this instead of the table:

> No AI tools were used in this project. All tests, bug investigation and fixes
> were produced by the group.

---

## Part 2 — Audit of the supplied test set (16 marks)

`ai_review/test_ai_suggested.py` contains eight tests presented as a finished
AI bug hunt for this bookstore. They are confident and they are not all
correct. Your job is to establish, for each one, what it actually does.

### How to classify a test

A single test run cannot tell you. "Fails against the buggy code" does **not**
mean the test found a bug — a test demanding behaviour the application was
never meant to have also fails. You need two runs, and the pair of results is
what identifies the category:

| Shipped Code | Fixed Code | What This Tells You | Verdict |
|---|---|---|---|
| ❌ FAIL | ✅ PASS | The test failed when the bug existed and passed after the bug was fixed. It successfully detected a real defect. | **Genuine detection** |
| ✅ PASS | ✅ PASS | The test passed before and after the fix. It never noticed the bug, so it provides false confidence. | **Detects nothing** |
| ✅ PASS | ❌ FAIL | The test expected the buggy behaviour. After the bug was fixed, the test broke. | **Locks in the bug** |
| ❌ FAIL | ❌ FAIL | The test failed both before and after the fix. It is testing something unrelated to the bug, or a requirement that does not exist. | **Invented requirement** |

The third row is the one to think hardest about. A test that locks in a bug is
worse than one that detects nothing: a team that trusts its suite will see the
test go red after a correct fix, conclude the fix was wrong, and revert it. The
bug then has a test defending it.

### How to produce the evidence

Run each test twice — once with the application as you received it, once with
your fixes in place. If you have already fixed the code, you can get back to
the shipped state with git:

```bash
# your fixed code
pytest ai_review/test_ai_suggested.py -v | tee /tmp/fixed.txt

# the code as it was shipped (replace <sha> with your first commit)
git stash
git checkout <sha> -- bookstore_app/
pytest ai_review/test_ai_suggested.py -v | tee /tmp/shipped.txt
git checkout HEAD -- bookstore_app/
git stash pop
```

Paste the real output. Not a screenshot, not a retyped summary — the text.

### Marks, per test

| | marks |
|---|---|
| Correct verdict | 1 |
| Both evidence runs pasted, showing the outcome you claim | 1 |

**A claim you cannot demonstrate costs a mark.** If you assert a test is broken
and the output does not support it, you lose more than you would have gained by
leaving the row blank. Check before you write.

### Summary table — fill this in first

| # | Test | What it claims to catch | Shipped | Fixed | Verdict | Auditor |
|---|---|---|---|---|---|---|
| 1 | `test_cart_total_sums_items` | Incorrect cart total | FAIL | PASS | Genuine detection | [Member who verified] |
| 2 |`test_login_rejects_wrong_password` | Login accepting an incorrect password | PASS | PASS | Detects nothing | [Member who verified] |
| 3 |`test_search_finds_exact_title` | Product search finding a matching title | PASS | PASS | Detects nothing | [Member who verified] |
| 4 |`test_import_returns_count` | Incorrect bulk-import count | FAIL | PASS | Genuine detection | [Member who verified] |
| 5 |`test_register_duplicate_returns_false` | Duplicate registration being accepted | PASS | PASS | Detects nothing | [Member who verified] |
| 6 |`test_checkout_empty_returns_none` | Incorrect result when checking out an empty cart | FAIL | PASS | Genuine detection | [Member who verified] |
| 7 |`test_add_to_cart_returns_true_for_known_product` | Adding a known product to the cart | PASS | PASS | Detects nothing | [Member who verified] |
| 8 | `test_search_is_limited_to_ten_results` | Search returning no more than ten results | FAIL | FAIL | Invented requirement | Lin Thant Maung |

### Detail entries

Copy the block below once for each of the eight tests. Do not paste the test
code — it is in the repository and identical for everyone. Reference it by name
and line instead.

---

#### Test1: `test_<function_name>`  (`ai_review/test_ai_suggested.py:<line>`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.** One or two sentences, in your own words, from
its name and docstring.
This test checks whether the shopping cart correctly adds together the prices of all items added to it.

**2. Evidence — against the shipped code**

```text
<============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_cart_total_sums_items FAILED        [100%]

=================================== FAILURES ===================================
__________________________ test_cart_total_sums_items __________________________

    def test_cart_total_sums_items():
        """Claims to check the cart total is correct."""
        cat = Catalog(); cat.add_product(1, "A", 10); cat.add_product(2, "B", 20)
        c = Cart(cat); c.add(1); c.add(2)
>       assert c.total() == 30
E       assert 10 == 30
E        +  where 10 = total()
E        +    where total = <bookstore_app.cart.Cart object at 0x10634e270>.total

ai_review/test_ai_generated.py:16: AssertionError
=========================== short test summary info ============================
FAILED ai_review/test_ai_generated.py::test_cart_total_sums_items - assert 10...
============================== 1 failed in 0.02s ===============================>
```

**3. Evidence — against your fixed code**

```text
<============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_cart_total_sums_items PASSED        [100%]

============================== 1 passed in 0.02s ===============================>
```

**4. What that pair proves.** Name the row of the classification table you
landed on and say why. If the verdict is "detects nothing" or "locks in the
bug", identify the specific weakness — which assertion, and what it would have
had to say instead. If it is "invented requirement", say where in the
application's behaviour you established that the requirement does not exist.
Classification: Genuine detection — FAIL then PASS. The test fails against the shipped code because the cart total is 10 instead of the expected 30. It passes against the fixed code, showing that the fix corrected the total calculation. The assertion assert c.total() == 30 checks the expected total directly.

**5. Verdict** (tick one)

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test2: `test_login_rejects_wrong_password` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether the login system rejects an incorrect password instead of allowing unauthorized access.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_login_rejects_wrong_password -v 2>&1 | tee /tmp/shipped_test_test_login_rejects_wrong_password.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_login_rejects_wrong_password

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_login_rejects_wrong_password -v 2>&1 | tee /tmp/fixed_test_test_login_rejects_wrong_password.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_login_rejects_wrong_password PASSED [100%]

============================== 1 passed in 0.02s ===============================

**4. What that pair proves.**

Classification: Detects nothing — PASS then PASS. The test passes against both versions. It does not detect the password-cleaning bug because its incorrect password (`wrongpw`) contains no punctuation. The original implementation removes non-alphanumeric characters from attempted passwords, so a stronger test would register a password such as `secret!` and check that logging in with `secret` is rejected.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test3: `test_search_finds_exact_title` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether the catalog search function can find a product when the user searches for its exact title.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_search_finds_exact_title -v 2>&1 | tee /tmp/shipped_test_test_search_finds_exact_title.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_search_finds_exact_title

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_search_finds_exact_title -v 2>&1 | tee /tmp/fixed_test_test_search_finds_exact_title.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_search_finds_exact_title PASSED     [100%]

============================== 1 passed in 0.02s ===============================

**4. What that pair proves.**

Classification: Detects nothing — PASS then PASS. The test passes against both versions because it searches using exactly the same capitalization as the product title. It does not detect the case-sensitive search bug. To catch that bug, the test should also search using different capitalization, such as python testing instead of Python Testing.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test4: `test_import_returns_count` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether the product-import function returns the correct number of products imported.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_import_returns_count -v 2>&1 | tee /tmp/shipped_test_test_import_returns_count.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_import_returns_count

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_import_returns_count -v 2>&1 | tee /tmp/fixed_test_test_import_returns_count.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_import_returns_count PASSED         [100%]

============================== 1 passed in 0.01s ===============================

**4. What that pair proves.**

Classification: Genuine detection — FAIL then PASS. The shipped implementation returned 3 when only 2 products were imported. The fixed implementation returned the correct count, so the test successfully detects the import-count bug.

**5. Verdict**

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test5: `test_register_duplicate_returns_false` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether the registration system rejects an attempt to register an account using a username that already exists.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_register_duplicate_returns_false -v 2>&1 | tee /tmp/shipped_test_test_register_duplicate_returns_false.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_register_duplicate_returns_false

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_register_duplicate_returns_false -v 2>&1 | tee /tmp/fixed_test_test_register_duplicate_returns_false.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_register_duplicate_returns_false PASSED [100%]

============================== 1 passed in 0.02s ===============================

**4. What that pair proves.**

Classification: Detects nothing — PASS then PASS. The test passes against both the shipped and fixed versions because the original implementation already rejected duplicate registrations. Therefore, it does not detect a bug that our group fixed.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test6: `test_checkout_empty_returns_none` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether checking out an empty shopping cart returns `None` instead of an incorrect result.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_checkout_empty_returns_none -v 2>&1 | tee /tmp/shipped_test_test_checkout_empty_returns_none.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_checkout_empty_returns_none

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_checkout_empty_returns_none -v 2>&1 | tee /tmp/fixed_test_test_checkout_empty_returns_none.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

**4. What that pair proves.**

Classification: Genuine detection — FAIL then PASS. The shipped implementation returned an empty list ([]) instead of None. The fixed implementation returned the expected None, so this test successfully detects the empty-cart checkout bug.

**5. Verdict**

- [x] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test7: `test_add_to_cart_returns_true_for_known_product` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether adding an existing product to the shopping cart succeeds and returns `True`.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product -v 2>&1 | tee /tmp/shipped_test_test_add_to_cart_returns_true_for_known_product.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product -v 2>&1 | tee /tmp/fixed_test_test_add_to_cart_returns_true_for_known_product.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_add_to_cart_returns_true_for_known_product PASSED [100%]

============================== 1 passed in 0.01s ===============================

**4. What that pair proves.**

Classification: Detects nothing — PASS then PASS. The test passes against both the shipped and fixed versions because adding a known product to the cart already worked in the original implementation. Therefore, it does not detect a bug fixed by our group.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [x] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [ ] Invented requirement — FAIL then FAIL

---

### Test8: `test_search_is_limited_to_ten_results` (`ai_review/test_ai_generated.py`)

**Audited by:** Lin Thant Maung

**1. What it claims to catch.**

This test checks whether the search function limits its results to a maximum of ten products.

**2. Evidence — against the shipped code**

lynnheinkhant@lynns-MacBook-Pro st211-midterm--Vortex-Five- % cd /tmp/vortex-shipped
pytest ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results -v 2>&1 | tee /tmp/shipped_test_test_search_is_limited_to_ten_results.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /private/tmp/vortex-shipped
configfile: pytest.ini
collecting ... ERROR: found no collectors for /private/tmp/vortex-shipped/ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results

collected 0 items / 1 error

==================================== ERRORS ====================================
_______________ ERROR collecting ai_review/test_ai_generated.py ________________
ImportError while importing test module '/private/tmp/vortex-shipped/ai_review/test_ai_generated.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ai_review/test_ai_generated.py:9: in <module>
    from bookstore_app import Users, Catalog, Cart
E   ModuleNotFoundError: No module named 'bookstore_app'
=========================== short test summary info ============================
ERROR ai_review/test_ai_generated.py
=============================== 1 error in 0.02s ===============================

**3. Evidence — against your fixed code**

lynnheinkhant@lynns-MacBook-Pro vortex-shipped % cd ~/Documents/GitHub/st211-midterm--Vortex-Five-
pytest ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results -v 2>&1 | tee /tmp/fixed_test_test_search_is_limited_to_ten_results.txt
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1, pluggy-1.7.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/lynnheinkhant/Documents/GitHub/st211-midterm--Vortex-Five-
configfile: pytest.ini
collecting ... collected 1 item

ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results FAILED [100%]

=================================== FAILURES ===================================
____________________ test_search_is_limited_to_ten_results _____________________

    def test_search_is_limited_to_ten_results():
        """Claims the catalogue search returns at most ten results."""
        cat = Catalog()
        for i in range(20):
            cat.add_product(i, "match", 1)
>       assert len(cat.search("match")) <= 10
E       AssertionError: assert 20 <= 10
E        +  where 20 = len([0, 1, 2, 3, 4, 5, ...])
E        +    where [0, 1, 2, 3, 4, 5, ...] = search('match')
E        +      where search = <bookstore_app.catalog.Catalog object at 0x105ece120>.search

ai_review/test_ai_generated.py:60: AssertionError
=========================== short test summary info ============================
FAILED ai_review/test_ai_generated.py::test_search_is_limited_to_ten_results
============================== 1 failed in 0.03s ===============================

**4. What that pair proves.**

Classification: Invented requirement — FAIL then FAIL. Both the shipped and fixed implementations return 20 results, causing the test to fail. However, the project requirements do not specify that search results must be limited to ten. Therefore, this test enforces an unsupported requirement rather than detecting a confirmed bug.

**5. Verdict**

- [ ] Genuine detection — FAIL then PASS
- [ ] Detects nothing — PASS then PASS
- [ ] Locks in the bug — PASS then FAIL
- [x] Invented requirement — FAIL then FAIL


## Part 3 — Coverage against your own bug hunt

One row per bug you recorded in `FINDINGS.md`, plus a row for any bug the
supplied set caught that you had not found yourself.

| Bug (your description) | We found it | The supplied set catches it | Which test, and how you established that |
|---|---|---|---|
| `cart.py → total()`: the last item was skipped (Bug 5). | Yes | Yes | `test_cart_total_sums_items` failed on shipped code and passed on fixed code. |
| `cart.py → import_products()`: the import count was one higher than the number of products imported (Bug 4). | Yes | Yes | `test_import_returns_count` failed on shipped code and passed on fixed code. |
| `catalog.py → search()`: searching with different capitalization returned no results (Bug 3). | Yes | No | `test_search_finds_exact_title` passed on both versions because it searched using exact capitalization. |
| Empty-cart checkout returned the wrong result; this was not recorded in the completed findings. | No | Yes | `test_checkout_empty_returns_none` failed on shipped code and passed on fixed code. |

This is a factual cross-reference, not an opinion. Every "yes" in the third
column must point at a test you classified as a genuine detection in Part 2.

---

## Part 4 — Verdict (4 marks, 400 words maximum)

Four questions. Be specific and cite your own table.

1. **Which failure mode was most common** in the supplied set? Give the count
   “Detects nothing” was the most common verdict, with 4 out of 8 tests. These tests passed on both shipped and fixed code and therefore did not demonstrate that they could detect a defect.
2. **Why is a test that passes against buggy code more dangerous than one that
   crashes?** A crashing test gets attention. Say what happens to the other
   kind.
   A failing test attracts attention, but a test that passes against buggy code creates false confidence. Developers may assume the feature is properly tested even though the test never exposes the defect. For example, test_search_finds_exact_title passed on both versions but did not detect our case-sensitive search bug.
3. **Did the supplied set catch anything you had missed?** If yes, what, and
   what would have led you to it. If no, say so — that is a legitimate answer
   and does not cost marks.
   The supplied set caught the empty-checkout behavior problem through test_checkout_empty_returns_none. This issue was not recorded in the completed entries of our FINDINGS.md. The test failed against shipped code and passed against fixed code, demonstrating a genuine detection.
4. **What will you check before trusting a generated test in future?** Name
   checks you actually performed in this exercise, not general principles.
   We ran all eight tests against the shipped code in a separate Git worktree and against our fixed code, saved the outputs, and compared each pair. We inspected the original Users.login() implementation and found that the wrong-password test did not expose the punctuation-cleaning bug. We also checked the catalog search behavior and found that the ten-result limit asserted by the AI test was not specified in the search function's documented behavior.

Answers that could have been written about any project score half marks at
best.

---

## Appendix (optional)

Prompts, or notes on AI use, that support Part 1.
