# Bug-Hunt Findings Log

Fill in one entry per bug you find, AS YOU FIND IT (before doing the AI
comparison). Write in your own words, like a detective's notebook. Show the real
path -- including things you tried that did not work.

Group: <your group name>
Members: <names>

---

## Bug 1

- **Module / function:** <e.g. cart.py -> total()>
- **What we suspected and why:** <what made you look here?>
- **What we did:** <the input or test you tried>
- **What we observed (the wrong result):** <actual output>
- **What we expected instead:** <correct behaviour>
- **The fix we made:** <what you changed>
- **Author of this finding:** <name>

---

## Bug 2

- **Module / function:**
- **What we suspected and why:**
- **What we did:**
- **What we observed (the wrong result):**
- **What we expected instead:**
- **The fix we made:**
- **Author of this finding:**

---

## Bug 3

(copy the block above for each additional bug you find)

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