# REPORT.md

##Group: <Vortex-Five>   Members: <Thant Thurein Lynn  (Paleon)      -       [6805140024]>
                                  <Lin Thant Maung     (Voldiel)     -       [6805140001]>
                                  <Khant Naing Hein    (Jason)       -       [6805140019]>
                                  <Thant Sin Hein      (Louis)       -       [6805140004]>
                                  <Zaw Moe Aung        (Zek)         -       [6805140020]>
## Part A -- Test types

**Smoke tests** are quick checks that the core features work at all. They run on every push, and a failure means the build is not worth testing further. Examples: a new user can register and log in; a product added to the cart appears in it and checkout returns an order.

**Regression tests** pin down one specific bug that was found and fixed, so it cannot return unnoticed. They run before merging and in CI. Examples: `cart.total()` includes the last item in the cart; `login()` accepts a password containing special characters.

**Slow tests** exercise the system with large data or heavy processing and take noticeably longer. They run on a schedule, such as nightly, not on every push. Examples: importing thousands of products into the catalog; searching a catalog of hundreds of thousands of titles.

## Part B -- Scenario classification
For each of the six scenarios: smoke / regression / slow (may be more than one)
with a 2-3 sentence justification.

## Part F -- Team reflection
1. Why is running only regression tests before every commit inefficient?
2. Why do smoke tests usually run first in a CI/CD pipeline?
3. What risks arise if slow tests are never run?
4. Can one test belong to two categories? Give an example.
5. Bug-finders and bug-fixers are often different people in a real QA team.
   What does that separation change about how a bug report must be written?
