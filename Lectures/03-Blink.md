# Project 01 — Blink: Making an LED Flash

## 1. What Are We Building?

We will make a single LED turn **ON** and **OFF** repeatedly — once every second.
This is the "Hello, World!" of hardware programming. It is simple, but it introduces
almost every fundamental idea you will use in every future Arduino project.

---

## 2. What Will You Learn?

By the end of this project you will be able to:

- Explain what a **microcontroller** is and what Arduino does
- Understand the **structure** of every Arduino program (`setup` and `loop`)
- Use **digital output** to control a physical component
- Use the `pinMode()`, `digitalWrite()`, and `delay()` functions
- Understand what a **variable** is and why it makes code easier to change
- Build a simple LED circuit on a breadboard
- Read a basic wiring diagram

---

## 3. Components Needed

| Quantity | Component | Notes |
|----------|-----------|-------|
| 1 | Arduino Uno | Any compatible clone works fine |
| 1 | LED (any color) | Red or green recommended for visibility |
| 1 | 220 Ω resistor | Orange–Orange–Brown color bands |
| 1 | Breadboard | Half-size or full-size |
| 2 | Jumper wires | Male-to-male |
| 1 | USB cable | To connect Arduino to your computer |

> **Why the resistor?**  
> An LED on its own allows too much current to flow through it and will burn out
> within seconds. The resistor limits the current to a safe level (~10–20 mA).
> **Never connect an LED directly to power without a resistor.**

---

## 4. Key Concepts

### 4.2 Digital Signals: HIGH and LOW

Arduino pins can be set to one of two states:

| State | Voltage | Meaning |
|-------|---------|---------|
| `HIGH` | 5 V | ON — current flows |
| `LOW` | 0 V | OFF — no current flows |

This is called a **digital** signal because it has only two possible values (like a
light switch: on or off).

### 4.3 The Structure of an Arduino Program (Sketch)

Every Arduino program — called a **sketch** — must contain exactly two functions:

```
setup()   → runs ONCE when the board powers on or is reset
loop()    → runs FOREVER, repeating over and over
```


### 4.4 Functions



Arduino has many **built-in functions** you can use immediately:

| Function | What It Does |
|----------|-------------|
| `pinMode(pin, mode)` | Configures a pin as INPUT or OUTPUT |
| `digitalWrite(pin, value)` | Sets a pin HIGH or LOW |
| `delay(ms)` | Pauses the program for a number of milliseconds |

### 4.5 Variables

A **variable** is a named storage location in memory that holds a value.

```cpp
int ledPin = 13;
```

- `int` — the **data type** (integer: a whole number)
- `ledPin` — the **name** you choose
- `13` — the **value** stored

**Why use a variable?**  
If your LED is on pin 13 and you use the number `13` in 10 places in your code,
changing the pin means editing 10 lines. With a variable, you change **one line**
and the rest updates automatically.



Good comments explain *why* something is done, not just *what* is done.

---

## 5. Hardware Setup

### Pin 13 — The Built-in LED

Arduino Uno has an LED already soldered onto the board, connected to **pin 13**.
This means the Blink sketch works even without any extra components — the built-in
LED will blink. Adding an external LED and resistor simply makes it more visible and
teaches you proper circuit wiring.

---

## 6. The Code

### Version 1 — Basic (using the literal number)

```cpp
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

### Version 2 — Better (using a variable)

```cpp
int ledPin = 13;  // Store the pin number in a variable

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  digitalWrite(ledPin, HIGH);   // Turn LED on
  delay(1000);                  // Wait 1 second (1000 ms)
  digitalWrite(ledPin, LOW);    // Turn LED off
  delay(1000);                  // Wait 1 second
}
```

### Version 3 — Best (using a named constant)

```cpp
const int LED_PIN   = 13;    // Pin number — never changes
const int ON_TIME   = 1000;  // ON duration in milliseconds
const int OFF_TIME  = 1000;  // OFF duration in milliseconds

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(ON_TIME);
  digitalWrite(LED_PIN, LOW);
  delay(OFF_TIME);
}
```

> **`const`** tells Arduino (and the programmer) that this value will never be changed.
> It is good practice to write constant names in ALL_CAPS to make them easy to spot.

---

## 7. How the Code Works — Step by Step

```
Program starts
     │
     ▼
┌─────────────┐
│   setup()   │  ← runs once
│             │
│ pinMode(13, │
│   OUTPUT)   │  ← tells Arduino: pin 13 is an output
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│                 loop()                  │  ← repeats forever
│                                         │
│  digitalWrite(13, HIGH) → LED turns ON  │
│  delay(1000)            → wait 1 sec    │
│  digitalWrite(13, LOW)  → LED turns OFF │
│  delay(1000)            → wait 1 sec    │
│                                         │
└────────────────────┬────────────────────┘
                     │ (goes back to top of loop)
                     └──────────────────────────▶ (repeats)
```

## 8. The Trick: Blinking Without `delay()`

`delay(1000)` doesn't just wait — it **freezes the entire program** for
that second. Nothing else can happen: no button can be checked, no sensor
read, no second LED pattern run. In every later project where you're
juggling a sensor, an LCD, and an LED at once, `delay()` becomes a
liability instead of a convenience.

The fix is to track time yourself using `millis()`, which returns the
number of milliseconds since the board powered on, and never blocks:

```cpp
const int LED_PIN = 13;
const unsigned long INTERVAL = 1000;   // 1 second

unsigned long previousMillis = 0;
bool ledState = LOW;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= INTERVAL) {
    previousMillis = currentMillis;      // remember when we last toggled
    ledState = !ledState;                // flip ON/OFF
    digitalWrite(LED_PIN, ledState);
  }

  // loop() keeps running immediately — you could add more code here
  // (read a button, check a sensor...) and it would never be delayed.
}
```

The pattern is always the same: remember `millis()` at the last event,
and on every pass through `loop()` just check whether *enough time has
passed since then* — never sleep. You'll see this exact pattern again in
Lecture 08 (Tank Level Control) and Lecture 09 (Speed Measurement), where
`delay()` would actually make the projects fail to respond in time.

> [!NOTE]
> `previousMillis` and `currentMillis` are `unsigned long`, not `int`.
> `millis()` overflows back to 0 after about 50 days — using unsigned
> subtraction (`currentMillis - previousMillis`) happens to still give the
> correct elapsed time even across that overflow, which is exactly why
> this pattern (and not a `>` comparison) is the standard one.

## 9. Exercises & Challenges




### Exercise 1 — SOS Signal ⭐⭐⭐

Morse code for SOS is: **· · · — — — · · ·**

| Symbol | Duration |
|--------|----------|
| Dot (·) | 200 ms ON, 200 ms OFF |
| Dash (—) | 600 ms ON, 200 ms OFF |
| Letter gap | 600 ms OFF |

Program the LED to continuously transmit the SOS signal.

---


### Exercise 2 — Two LEDs ⭐

Add a **second LED** (with its own resistor) to **pin 12**.
Program them so they alternate — when one is ON, the other is OFF.

*Hint: You will need a second `const int` for the new pin and two more `digitalWrite` calls.*

---

### Exercise 3 — Heartbeat Pattern ⭐⭐⭐

A real heartbeat has two quick beats followed by a pause.  
Program the LED to simulate: flash, flash, long pause, flash, flash, long pause, ...

---

### Exercise 4 — Rewrite with `millis()` ⭐⭐

Take your solution to Exercise 2 (Two LEDs) and rewrite it using the
`millis()` pattern from Section 8 instead of `delay()`, so both LEDs blink
at **different, independent intervals** (e.g. one every 500 ms, the other
every 700 ms) without interfering with each other.

*Hint: you'll need two separate `previousMillis` variables — one per LED
— since each blinks on its own schedule.*
