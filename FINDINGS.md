# Bug-Hunt Findings Log

Fill in one entry per bug you find, AS YOU FIND IT (before doing the AI
comparison). Write in your own words, like a detective's notebook. Show the real
path -- including things you tried that did not work.

Group: Vortex-Five
Members: Thant Thurein Lynn, Lin Thant Maung, Khant Naing Hein, Thant Sin Hein, Zaw Moe Aung

## Bug 1

- **Module / function:** bookstore_app/users.py -> login()
- **What we suspected and why:** register() stores the password exactly as given, so a user should be able to log in with the same password. We suspected login() changed the password before comparing it.
- **What we did:** Registered a user with the password `pass@word1`, then logged in with the same password, and wrote a regression test for it.
- **What we observed (the wrong result):** login() returned False for the correct password. The regression test failed with `AssertionError: assert False is True`.
- **What we expected instead:** A user must be able to log in with exactly the password they registered, including symbols, so login() should return True.
- **The fix we made:** Removed the `cleaned` line that stripped non-alphanumeric characters from the typed password, and compared the password as typed (`stored == password`).
- **Author of this finding:** Thant Thurein Lynn-[6805140024], with advice from Khant Naing Hein-[6805140019]

---

## Bug 2

- **Module / function:** bookstore_app/cart.py -> checkout() (two defects in the same function)
- **What we suspected and why:** The docstring says checkout() returns the order list, or None if the cart is empty, so we suspected the empty case was not handled. While testing it, we also checked whether the returned order is kept safely in the history.
- **What we did:** Created a cart with an empty catalog and called checkout() without adding anything. Then added one product, checked out, appended `99` to the returned order, and printed history(). We wrote a regression test for each case.
- **What we observed (the wrong result):** (a) An empty cart returned `[]` instead of None; the test failed with `assert [] is None`. (b) The original code stored the same list it returned (`self.orders.append(order)`), so after `order.append(99)` history() showed `[[1, 99]]` instead of `[[1]]`.
- **What we expected instead:** (a) An empty cart should return None, and no empty order should be recorded. (b) The recorded history should not change when the caller edits the returned order, so history() should still be `[[1]]`.
- **The fix we made:** Added `if not self.items: return None` at the start of checkout(), and changed the history line to store a copy: `self.orders.append(list(order))`.
- **Author of this finding:** Thant Thurein Lynn-[6805140024]

---

## Bug 3

- **Module / function:** bookstore_app/catalog.py -> search()
- **What we suspected and why:** search() is the only function in catalog.py with logic, and its docstring says it returns products whose title contains the keyword, so we suspected it was too strict about what counts as "contains".
- **What we did:** Added "Python Basics" to a catalog and searched for "Python" and then "python" in the Python shell, then wrote a regression test for the lowercase search.
- **What we observed (the wrong result):** search("Python") returned [1] but search("python") returned []. The regression test failed with `assert [] == [1]`.
- **What we expected instead:** A customer typing the keyword in any letter case should find the product, so search("python") should return [1].
- **The fix we made:** Changed `if keyword in info["title"]` to `if keyword.lower() in info["title"].lower()`.
- **Author of this finding:** Thant Thurein Lynn-[6805140024]

---

## Bug 4

- Module / function: "bookstore_app/cart.py" → "import_products()"
- What we suspected and why: We suspected that the function was returning the wrong number of imported products.
- What we did: We created a regression test that imported two products and checked the returned count.
- What we observed (the wrong result): The test failed because the function returned one more than expected.
- What we expected instead: The function should return 2 when two products are imported.
- The fix we made: We changed "return count + 1" to "return count".
- Author of this finding: Zaw Moe Aung-[6805140020]

---

## Bug 5

- Module / function: "bookstore_app/cart.py" → "total()"
- What we suspected and why: We suspected that the cart total was not including every item.
- What we did: We added three books priced at 100, 200, and 300 and tested the total.
- What we observed (the wrong result): The test returned 300 instead of 600 because the last item was skipped.
- What we expected instead: The total should include the prices of all items in the cart, which is 600.
- The fix we made: We changed "range(len(self.items) - 1)" to "range(len(self.items))".
- Author of this finding: Zaw Moe Aung-[6805140020]