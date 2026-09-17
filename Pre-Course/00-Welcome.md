# Pre-Course — Before You Touch a Single Wire

## Why a Pre-Course?

Every project in this course — the fire alarm, the security system, the tank
level controller — is really just **C code wearing a circuit as a costume**.
The `if` statement that decides whether a flame sensor means "fire" is the
exact same `if` statement you'd use to decide whether an exam score is a
passing grade. If the C underneath is shaky, no amount of correct wiring will
save the project.

So before Lecture 01 and your first Arduino board, this short pre-course
gets you comfortable **writing, running, and debugging plain C** — no
microcontroller, no breadboard, nothing that can be plugged in backwards.
Every mistake here costs you a re-run, not a burnt-out LED.

## What's in It

| # | Page | What it covers |
|---|---|---|
| 00 | Welcome (this page) | Why this exists, how to use it |
| 01 | [C Fundamentals Primer](<./01-C-Fundamentals-Primer.md>) | `main()`, `printf`/`scanf`, types, operators, `if`, loops, functions — the parts of C that exist with or without Arduino |
| 02 | [Practice Problems](<./02-Practice-Problems.md>) | Five problems (factorial series, Armstrong numbers, Goldbach's conjecture, prime/perfect numbers, Taylor series) to actually build the muscle |

## How to Use It

1. Open an online C compiler — e.g. [compiler.edroca.com](https://compiler.edroca.com/)
   (two more options are listed in the project README's Online Compilers
   section). Wokwi and Tinkercad are for circuits later, these are for
   pure code right now.
2. Read [01 - C Fundamentals Primer](<./01-C-Fundamentals-Primer.md>). It's
   short on purpose — it's a map of what exists, not a full textbook.
3. Solve the problems in [02 - Practice Problems](<./02-Practice-Problems.md>)
   yourself before checking any solution. Getting one wrong and fixing it
   teaches you more than getting it right by copying.
4. Once you can write a loop and a function without hesitating, move on to
   [Lectures/00 - Electronics Fundamentals](<../Lectures/00-Electronics%20Fundamentals.md>)
   and then [Lecture 01](<../Lectures/01-Introduction.md>).

> [!NOTE]
> `Lectures/02-C Overview.md` covers a lot of this same ground again, in
> more depth and in the specific dialect of C the Arduino IDE compiles
> ("Arduino C"). That's not a mistake — this pre-course is meant to be fast
> and hands-on; Lecture 02 is the deeper reference you'll come back to.

<br/>

**Next:** [01 - C Fundamentals Primer →](<./01-C-Fundamentals-Primer.md>)
