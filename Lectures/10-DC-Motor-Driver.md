# Project 11 — DC Motor Control with an L298N Driver

## 1. What Are We Building?

A **two-wheel motor rig** you can drive forward, backward, and stop, with
independently adjustable speed on each wheel — the same building block
behind every wheeled robot, conveyor, and fan-speed controller.

The core problem this project solves: an Arduino pin can supply a few
milliamps and 5V. A DC motor wants hundreds of milliamps to amps, at
whatever voltage its rated for (often 6–12V) — and it needs its direction
reversible, which a single pin can never do on its own. The **L298N motor
driver** module sits between the Arduino and the motors, acting as a
current amplifier and direction switch.

## 2. What Will You Learn?

- Why motors need a **driver**, not a direct pin connection (recap of the
  power-budget discussion from Lecture 00)
- How an **H-bridge** makes a motor spin in either direction from a
  fixed-polarity supply
- Controlling motor **speed** with PWM through the driver's enable pins
- Building simple movement functions: `forward()`, `backward()`, `turnLeft()`, `stop()`

## 3. Components Needed

| Quantity | Component | Notes |
|----------|-----------|-------|
| 1 | Arduino Uno | |
| 1 | L298N motor driver module | Dual H-bridge, breakout board with screw terminals |
| 2 | DC gear motors | 6-12V hobby motors, e.g. from a robot chassis kit |
| 1 | External battery pack | 7.4V–9V, matched to your motors — **not** the Arduino's 5V |
| 1 | Breadboard + jumper wires | |

## 4. Key Concepts

### 4.1 The H-Bridge, Conceptually

An H-bridge is four switches arranged so that reversing which pair is
closed reverses the current direction through the motor:

```
        +V
     ┌───┴───┐
   [S1]     [S2]
     │         │
     ├── M ────┤     M = motor
     │         │
   [S3]     [S4]
     └───┬───┘
        GND

S1+S4 closed → current flows left-to-right → motor spins one way
S2+S3 closed → current flows right-to-left → motor spins the other way
```

The L298N module packages two of these H-bridges (one per motor) plus the
transistors to handle real motor current, and exposes simple digital
control pins so you never touch the switches directly.

### 4.2 L298N Control Pins

Each motor channel has three control pins:

| Pin | Purpose |
|---|---|
| `IN1`, `IN2` | Direction — one HIGH + one LOW spins forward, swapped spins backward, both LOW (or both HIGH) stops |
| `ENA` (or `ENB`) | Enable / speed — connect to a PWM pin; `analogWrite()` here controls speed, just like dimming an LED in Lecture 04 |

| `IN1` | `IN2` | Motor behavior |
|---|---|---|
| HIGH | LOW | Spins forward |
| LOW | HIGH | Spins backward |
| LOW | LOW | Coasts to a stop |
| HIGH | HIGH | Brakes (both terminals shorted) |

### 4.3 Two Power Domains, One Shared Ground

The L298N has **two separate power inputs**: 5V logic (can come from the
Arduino) and the motor supply (from your external battery pack). This is
the exact "external power supply" warning from Lecture 00, made concrete:

```
Arduino 5V ──► L298N logic supply
Arduino GND ──► L298N GND ──► Battery pack (−)   ← shared ground, mandatory
Battery pack (+) ──► L298N motor supply (12V screw terminal)
```

> [!CAUTION]
> If the grounds aren't tied together, the Arduino's PWM/direction
> signals have no shared reference voltage with the motor driver, and
> control becomes unreliable or stops working entirely — this is the
> single most common wiring mistake with motor drivers.

## 5. Pin Connections

| L298N Pin | Arduino Pin |
|---|---|
| ENA | 9 (PWM) |
| IN1 | 8 |
| IN2 | 7 |
| IN3 | 6 |
| IN4 | 5 |
| ENB | 3 (PWM) |
| GND | GND (shared with battery −) |
| 5V | Arduino 5V (only if the module's 5V-logic jumper is in place) |
| 12V | Battery pack + |

## 6. The Code

```cpp
// ── Left motor ──────────────────────────────────
const int ENA = 9, IN1 = 8, IN2 = 7;
// ── Right motor ─────────────────────────────────
const int ENB = 3, IN3 = 6, IN4 = 5;

void setup() {
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
}

void loop() {
  forward(200);   // ~78% speed
  delay(2000);

  stopMotors();
  delay(500);

  backward(150);
  delay(2000);

  stopMotors();
  delay(500);

  turnLeft(180);
  delay(1000);

  stopMotors();
  delay(2000);
}

void forward(int speed) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void backward(int speed) {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void turnLeft(int speed) {
  // left wheel backward, right wheel forward → spins in place
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, speed);
  analogWrite(ENB, speed);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}
```

## 7. Exercises & Challenges

### Exercise 1 — Speed from a Potentiometer ⭐

Wire a potentiometer to `A0` and use `map()` (Lecture 04) to control
`forward()`'s speed in real time instead of a fixed value.

### Exercise 2 — Obstacle Stop ⭐⭐

Add an ultrasonic distance sensor (as used in Lecture 08) facing forward.
Call `stopMotors()` automatically if an obstacle comes within 15 cm while
driving forward.

### Exercise 3 — Smooth Start/Stop ⭐⭐

Using the `millis()` non-blocking pattern from Lecture 03, ramp `speed`
from 0 up to its target value over half a second when starting, instead
of jumping straight to full PWM — this reduces the current surge and
wheel slip at startup.

### Exercise 4 — Line Follower Core ⭐⭐⭐

Add two IR reflectance sensors (like the break-beam sensors from Lecture
09, but pointed down at the floor). When the left sensor sees the line's
edge, steer right; when the right sensor does, steer left. This is the
core control loop of a line-following robot — see the
[Capstone Project](<./13-Capstone-Project.md>) for a full build.
