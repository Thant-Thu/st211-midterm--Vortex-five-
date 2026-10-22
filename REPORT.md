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

1. **Password-reset email delivered within one minute: slow.** It depends on an external email service and has to wait for delivery, so it takes far longer than a unit test. It should run nightly, not on every push.

2. **Fixed shipping-cost bug has not returned: regression.** It targets one specific bug that was already fixed, and it should fail if the bug comes back. It runs on every build.

3. **Nightly sales report from ten years of orders: slow.** It processes a very large amount of data, so it runs on a schedule and not on every push.

4. **Payment page loads after every deployment: smoke.** It is a fast check that a critical feature works at all, and a failure should stop the release immediately.

5. **Refund issued twice does not credit the customer twice: regression.** It checks a fault that was reported and fixed, so it guards against that bug returning. It is not smoke because it covers one specific defect, not basic functionality.

6. **Recommendation engine responds with one million titles: slow.** It tests behavior under very large data, so it is too heavy to run on every push. It belongs in the nightly run.

## Part F -- Team reflection
1. Why is running only regression tests before every commit inefficient?
2. Why do smoke tests usually run first in a CI/CD pipeline?
3. What risks arise if slow tests are never run?
4. Can one test belong to two categories? Give an example.
5. Bug-finders and bug-fixers are often different people in a real QA team.
   What does that separation change about how a bug report must be written?
