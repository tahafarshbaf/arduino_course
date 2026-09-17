# Lecture 00 — Electronics Fundamentals

Every project from here on hands you a component list with things like
"220 Ω resistor" and a wiring diagram that just works — without ever
explaining *why* it's 220 Ω and not 1 Ω, or why some pins can't be
connected straight to a motor. This lecture fills that gap once, so every
later lecture can stop re-explaining it.

## 1. What Will You Learn?

- Voltage, current, and resistance, and how Ohm's Law ties them together
- How to read a resistor's value from its color bands
- How a breadboard is actually wired underneath the holes
- Why Arduino pins have current limits, and when a project needs an
  external power supply
- The absolute basics of using a multimeter

## 2. Voltage, Current, Resistance

Think of electricity like water in a pipe:

| Electrical quantity | Water analogy | Unit |
|---|---|---|
| **Voltage (V)** | Water pressure | Volts (V) |
| **Current (I)** | Flow rate (how much water moves) | Amps (A) |
| **Resistance (R)** | How narrow the pipe is | Ohms (Ω) |

Higher pressure (voltage) pushes more water (current) through a pipe of a
given width (resistance). Squeeze the pipe (raise resistance) and less
water flows for the same pressure.

### Ohm's Law

```
V = I × R
```

Three quantities, one equation — know any two, calculate the third:

```
I = V / R        R = V / I        V = I × R
```

**Worked example:** you're driving a red LED that needs about 2 V across
it and should be limited to 15 mA (0.015 A) to stay safe, from a 5 V
Arduino pin. The resistor has to absorb the *difference* in voltage:

```
V_resistor = 5 V - 2 V = 3 V
R = V / I = 3 / 0.015 = 200 Ω
```

That's exactly why every LED in this course sits behind a resistor in the
100–330 Ω range — it's this calculation, just rounded to a value you can
actually buy.

> [!CAUTION]
> An LED with **no** resistor is not "a bit brighter" — Ohm's law still
> applies, but the LED's own resistance is tiny and unpredictable, so
> current spikes far past its rating in a fraction of a second and it
> burns out. Every LED in this course needs a resistor in series, no
> exceptions.

## 3. Reading Resistor Color Codes

Resistors are too small to print numbers on, so they use colored bands
instead. A standard 4-band resistor reads:

```
[Band 1][Band 2][Multiplier][Tolerance]
  digit    digit    ×10^n      ± %
```

| Color | Digit | Multiplier | Tolerance |
|---|---|---|---|
| Black | 0 | ×1 | |
| Brown | 1 | ×10 | ±1% |
| Red | 2 | ×100 | ±2% |
| Orange | 3 | ×1,000 | |
| Yellow | 4 | ×10,000 | |
| Green | 5 | ×100,000 | |
| Blue | 6 | ×1,000,000 | |
| Violet | 7 | | |
| Grey | 8 | | |
| White | 9 | | |
| Gold | | ×0.1 | ±5% |
| Silver | | ×0.01 | ±10% |

**Example:** Red-Red-Brown-Gold → `2`, `2`, ×10, ±5% → **220 Ω, ±5%** —
the exact resistor this course keeps asking you to grab for LEDs.

You don't need to memorize this table by heart; every simulator (Wokwi,
Tinkercad) shows the resistance value directly when you click a resistor.
What matters is understanding that **the color bands are just an encoded
number**, so a datasheet or schematic saying "220 Ω" and a real resistor
in your hand saying "Red-Red-Brown" are the same fact in two notations.

## 4. The Breadboard, Underneath the Holes

A breadboard *looks* like a uniform grid of holes, but the copper strips
underneath connect them in a specific pattern:

```
  + ─────────────────────────────────────  ← power rail (+), one long strip
  − ─────────────────────────────────────  ← power rail (−), one long strip

  a b c d e │ f g h i j
  a b c d e │ f g h i j     ← each column (a-e) of 5 holes is one
  a b c d e │ f g h i j       connected strip, but NOT connected
  a b c d e │ f g h i j       across the center gap to f-j
  a b c d e │ f g h i j
        ...

  + ─────────────────────────────────────
  − ─────────────────────────────────────
```

- The two long **rails** at top and bottom (often marked red `+` and blue
  `−`) run the full length of the board — that's where you bring in 5V and
  GND once, then tap into them anywhere.
- The middle section is split into short **columns of 5 holes**, each
  column internally connected — but *not* connected to the column next to
  it, and *not* connected across the center gap.

This is why a wire "one hole over" sometimes does nothing (still the same
column) and why plugging a component straight across the center gap is a
common way to bridge two separate circuits by accident.

## 5. Arduino's Power Budget

The Arduino Uno's 5V pin doesn't have infinite current to give:

| Source | Safe current limit |
|---|---|
| A single digital I/O pin | ~20 mA continuous (40 mA absolute max) |
| The board's 5V pin (via USB) | ~500 mA total, shared across everything |
| The board's 5V pin (external power) | up to ~1–2 A, depends on the supply |

An LED draws ~15–20 mA — well within a pin's limit, which is why
`digitalWrite(pin, HIGH)` can drive one directly (through its resistor).

A **servo motor** or a **DC motor**, on the other hand, can draw
**hundreds of milliamps to a few amps**, especially when it stalls or
starts moving. That is far beyond what a single pin — or sometimes even
the whole 5V rail from USB — can safely supply.

> [!CAUTION]
> Powering a servo or motor from the Arduino's own 5V pin off USB "mostly
> works" in a demo and then resets the board or fries a regulator under
> load. Projects with a motor or more than one servo need their own
> external power supply for the motor, with the grounds of the Arduino and
> the external supply **tied together** (a shared GND reference is the one
> connection that can never be skipped).

## 6. Using a Multimeter (Just Enough to Get Started)

A multimeter has (at least) three modes relevant here:

| Mode | Symbol | Use it to... |
|---|---|---|
| Voltage (DC) | `V⎓` | Measure voltage **across** two points — probes touch both ends of a component, in parallel with it |
| Current (DC) | `A⎓` | Measure current **through** a wire — the meter must be placed *in series*, breaking the circuit to insert itself |
| Continuity / Resistance | `Ω` / `)))` | Check if two points are electrically connected (beeps), or measure a resistor's value, with the **circuit powered off** |

The most common beginner mistake is trying to measure current the same way
as voltage (probes touching two points without breaking the circuit) —
this doesn't measure anything useful and, depending on the meter, can trip
its internal fuse.

## 7. Exercises

### Exercise 1 — Resistor Sizing ⭐

A green LED needs about 2.1 V across it and should be limited to 20 mA.
It will be driven from a 5V Arduino pin. Calculate the resistor value you
need, then find the closest standard resistor value at or above your
answer (standard values include 100, 150, 220, 330, 470, 680, 1000 Ω).

### Exercise 2 — Color Code Practice ⭐

Decode these resistor color bands into resistance values:
1. Brown-Black-Red-Gold
2. Yellow-Violet-Orange-Gold
3. Green-Blue-Brown-Gold

### Exercise 3 — Breadboard Tracing ⭐⭐

Sketch (on paper) a simple LED + resistor circuit powered from the two
rails of a breadboard, with the LED's anode in column `c3` and the
resistor connecting `c3`'s row to the `+` rail. Mark every hole that is
electrically the same node.

### Exercise 4 — Power Budget Check ⭐⭐

You're building a robot with 4 DC motors, each drawing up to 300 mA when
starting. Calculate the total current if all 4 start simultaneously.
Compare it against the Arduino's USB-powered 5V budget (~500 mA) and
explain, in your own words, why this project needs an external power
supply.

---

**Next:** [Lecture 01 - Introduction →](<./01-Introduction.md>)
