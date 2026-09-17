# Practice Problems

Five problems, no hardware. Solve each one in a plain C file (`main()` +
`printf`) using any of the [online compilers](<./00-Welcome.md>) from the
Welcome page. Difficulty is marked with stars (⭐ = warm-up, ⭐⭐⭐ = will
take real thought).

Don't look at the hint until you're stuck for a few minutes — struggling
first is the point.

---

## Problem 1 — Factorial Series ⭐

Write a program that prints the factorial of every integer from `1` to
`10`:

```
1! = 1
2! = 2
3! = 6
...
10! = 3628800
```

*Hint: `factorial(n) = n * factorial(n-1)`, with `factorial(1) = 1`. You can
compute this with either a loop or a recursive function — try the loop
first. Use `unsigned long` for the result; `10!` is bigger than `int` can
always be trusted with on every compiler.*

---

## Problem 2 — Armstrong Numbers ⭐⭐

An **Armstrong number** (for a 3-digit number) is one where the sum of the
cube of each digit equals the number itself. Example: `153 = 1³ + 5³ + 3³
= 1 + 125 + 27 = 153`.

Write a program that prints every 3-digit Armstrong number between 100 and
999.

*Hint: to pull out digits from a number `n`, use `n % 10` to get the last
digit, then `n = n / 10` to drop it, and repeat.*

---

## Problem 3 — Goldbach's Conjecture ⭐⭐

Goldbach's conjecture states that **every even integer greater than 2 can
be written as the sum of two prime numbers**. Write a program that:

1. Takes an even number `N` from the user (`scanf`).
2. Finds *any one* pair of primes `p1, p2` such that `p1 + p2 == N`.
3. Prints the pair, e.g. for `N = 28`: `28 = 5 + 23`.

*Hint: write a helper function `int isPrime(int n)` first and reuse it. To
find the pair, loop a candidate `p1` from 2 upward, and check whether
`N - p1` is also prime.*

---

## Problem 4 — Prime and Perfect Numbers ⭐⭐

Write a program that, for every number from 1 to 100:

- Prints it if it's **prime** (only divisible by 1 and itself).
- Separately, prints it if it's **perfect** (equal to the sum of its
  proper divisors — e.g. `6 = 1 + 2 + 3`).

*Hint: for perfect numbers, loop `d` from 1 to `n/2`, sum up every `d` where
`n % d == 0`, then compare the sum to `n`. There are only two perfect
numbers below 100 — if your program finds more or fewer, you have a bug.*

---

## Problem 5 — Taylor Series Approximation ⭐⭐⭐

The Taylor series lets you approximate a function using only additions,
multiplications, and divisions — exactly what a computer (or a
microcontroller with no built-in trig hardware) is good at.

**Part A — π via the Leibniz series:**

```
π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
```

Write a program that sums the first 100,000 terms and prints the resulting
approximation of π. It converges slowly — expect only 3-4 correct digits.

**Part B — sin(x) via its Taylor expansion:**

```
sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
```

Write a program that approximates `sin(x)` for a value of `x` (in radians)
entered by the user, summing the first 10 terms, and compare your result
against the C standard library's own `sin(x)` from `<math.h>`.

*Hint for Part B: keep a running `term` variable and update it each
iteration by multiplying by `-x*x / ((2k)(2k+1))` instead of recomputing the
whole power and factorial from scratch each time — it's both faster and
avoids overflowing the factorial for larger terms.*

---

## What's Next

Once these feel manageable — you're not fighting the syntax anymore, just
the logic — you're ready for hardware. Move on to
[Lectures/00 - Electronics Fundamentals](<../Lectures/00-Electronics%20Fundamentals.md>).
