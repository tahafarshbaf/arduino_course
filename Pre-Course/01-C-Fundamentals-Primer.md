# C Fundamentals Primer

This is a fast tour of plain, standalone C — the kind you compile with a
`main()` function and run on a normal computer, no microcontroller involved.
Everything here transfers directly to Arduino C later; the only real
difference is that Arduino hides `main()` from you and gives you `setup()`
and `loop()` instead (more on that in Lecture 01).

## 1. The Skeleton of a C Program

```c
#include <stdio.h>

int main() {
    printf("Hello, world!\n");
    return 0;
}
```

- `#include <stdio.h>` — pulls in the **standard input/output** library, so
  you can use `printf` and `scanf`.
- `int main() { ... }` — every C program starts executing here. The `int`
  means this function hands back a number when it finishes.
- `return 0;` — tells the operating system "finished successfully."

Paste this into any of the online compilers linked from
[00 - Welcome](<./00-Welcome.md>) and run it. That's the entire loop
you'll repeat for every problem in this pre-course: write, compile, run,
fix.

## 2. Talking to the Program: `printf` and `scanf`

```c
printf("Result: %d\n", 42);     // print an integer
printf("Pi is %f\n", 3.14159);  // print a float

int age;
scanf("%d", &age);              // read an integer from the user
printf("You are %d years old\n", age);
```

The `%d`, `%f`, etc. are **format specifiers** — placeholders that say what
type of value goes there:

| Specifier | Type |
|---|---|
| `%d` | `int` |
| `%f` | `float` / `double` |
| `%c` | `char` |
| `%s` | string (`char` array) |

Notice the `&` in `scanf("%d", &age)` — `scanf` needs the **address** of the
variable so it can write into it, not a copy of its value. This is your
first taste of pointers; you don't need to understand them fully yet.

## 3. Variables and Types

```c
int    count   = 10;      // whole numbers
float  voltage = 3.3;     // decimals, ~7 digits of precision
double precise = 3.14159265358979; // decimals, ~15 digits of precision
char   grade   = 'A';     // a single character, in single quotes
```

Naming rules: letters, digits, and `_`; can't start with a digit; can't be a
C keyword (`int`, `return`, `for`, ...). `speedKmh` and `speed_kmh` are both
fine — pick a style and stay consistent.

## 4. Operators

```c
int a = 7, b = 2;

a + b;   // 9
a - b;   // 5
a * b;   // 14
a / b;   // 3   ← integer division truncates! 7/2 is 3, not 3.5
a % b;   // 1   ← modulo: the remainder

a == b;  // is a equal to b?   (== , not =)
a != b;  // is a not equal to b?
a > b; a < b; a >= b; a <= b;

a && b;  // logical AND
a || b;  // logical OR
!a;      // logical NOT
```

The integer-division trap catches everyone once: if you want `3.5`, at
least one of the operands must be a `float`:

```c
float result = (float)a / b;   // 3.5 — the cast forces float division
```

## 5. Making Decisions

```c
if (voltage < 3.0) {
    printf("Low battery\n");
} else if (voltage < 4.0) {
    printf("OK\n");
} else {
    printf("Full\n");
}
```

`switch` is the alternative when you're comparing one variable against many
exact values:

```c
switch (grade) {
    case 'A': printf("Excellent\n"); break;
    case 'B': printf("Good\n");      break;
    default:  printf("Keep trying\n");
}
```

Don't forget `break;` — without it, execution "falls through" into the next
case.

## 6. Loops

```c
// for: when you know how many times up front
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}

// while: when you loop until a condition changes
int n = 100;
while (n > 1) {
    n = n / 2;
}

// do-while: like while, but always runs at least once
int input;
do {
    printf("Enter a positive number: ");
    scanf("%d", &input);
} while (input <= 0);
```

## 7. Arrays

```c
int scores[5] = {88, 92, 79, 95, 60};
printf("%d\n", scores[0]);   // 88 — indexing starts at 0
printf("%d\n", scores[4]);   // 60 — the last valid index is length - 1

for (int i = 0; i < 5; i++) {
    printf("%d\n", scores[i]);
}
```

`scores[5]` in that same array would read past the end — C does **not**
stop you, it just reads garbage memory. This is one of the most common bugs
in beginner C: always double-check your loop bound is `< length`, not
`<= length`.

## 8. Functions

```c
float celsiusToFahrenheit(float celsius) {
    return celsius * 9.0 / 5.0 + 32.0;
}

int main() {
    float c = 20.0;
    printf("%.1f C = %.1f F\n", c, celsiusToFahrenheit(c));
    return 0;
}
```

A function has: a **return type** (`float`), a **name**, **parameters** in
parentheses, and a **body** that ends with `return` (unless the return type
is `void`, meaning it returns nothing). Breaking a problem into functions
like this — one job per function — is the single habit that will help you
most once projects get bigger.

## 9. Comments

```c
// a single-line comment

/* a
   multi-line
   comment */
```

Use them to explain *why*, not *what* — `i++; // increment i` teaches
nobody anything the code didn't already say.

---

That's the whole toolbox for the practice problems ahead. Nothing here is
Arduino-specific yet — every line compiles and runs on a plain desktop C
compiler.

**Next:** [02 - Practice Problems →](<./02-Practice-Problems.md>)
