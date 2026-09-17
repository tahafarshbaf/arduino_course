# Capstone Project — Autonomous Line-Following Robot

## 1. What Are We Building?

This is the final project — no new hardware concept, just **everything so
far, combined into one system**: a two-wheeled robot that follows a black
line on the floor, logs its run statistics to EEPROM, reports status over
Bluetooth, and displays state on an LCD.

If Lecture 09's speed camera was "put a few concepts together," this is
"put the *whole course* together." Treat it as the real test of whether
you understand the pieces, not just each project in isolation.

## 2. What You Already Know That This Uses

| Piece | From | Role here |
|---|---|---|
| State machines (`enum` + `switch`) | Lecture 08 | Tracks robot mode: `FOLLOWING`, `LOST_LINE`, `STOPPED` |
| Non-blocking timing (`millis()`) | Lecture 03 | Sensor polling and status broadcasts without ever blocking motor control |
| Analog thresholds | Lecture 05 | Deciding "line" vs. "floor" from each IR sensor's reading |
| Moving average smoothing | Lecture 04 | Optional: smoothing sensor noise near the line's edge |
| H-bridge motor control | Lecture 10 | Driving and steering the two wheels |
| EEPROM persistence | Lecture 07 | Saving total run count and last completion time across power cycles |
| I2C LCD | Lecture 07 | Displaying current mode and run stats |
| Bluetooth Serial | Lecture 12 | Remote start/stop and live status |

## 3. Components Needed

| Quantity | Component |
|----------|-----------|
| 1 | Arduino Uno |
| 1 | L298N motor driver + 2 DC gear motors (Lecture 10) |
| 3 | IR reflectance (line-following) sensor modules |
| 1 | HC-05 Bluetooth module (Lecture 12) |
| 1 | 16×2 I2C LCD |
| 1 | External battery pack for the motors |
| 1 | Robot chassis (2 wheels + 1 caster) |

## 4. The Control Logic

Three IR sensors are mounted across the front of the chassis: `left`,
`center`, `right`. Each reads HIGH over the light floor and LOW over the
black line (or the reverse — check your specific modules and flip the
logic if needed).

```
   [L]   [C]   [R]      ← sensors, viewed from above
    │     │     │
────┴─────┴─────┴────   ← floor
         ███             ← black line, currently under [C]
```

| Left | Center | Right | Meaning | Action |
|---|---|---|---|---|
| floor | line | floor | On track | Drive straight |
| line | floor | floor | Drifted right | Steer left |
| floor | floor | line | Drifted left | Steer right |
| floor | floor | floor | Lost the line | Stop, or reverse briefly to search |
| line | line | line | Crossing a junction / finish marker | Application-specific (here: treat as finish) |

This table *is* the state machine — translating it into a `switch`
statement is a direct application of Lecture 08's pattern.

## 5. Pin Connections

| Component | Arduino Pin |
|---|---|
| Left IR sensor | A0 |
| Center IR sensor | A1 |
| Right IR sensor | A2 |
| L298N ENA / IN1 / IN2 | 9 / 8 / 7 |
| L298N ENB / IN3 / IN4 | 3 / 6 / 5 |
| HC-05 TX / RX | 10 / 11 (via voltage divider — see Lecture 12) |
| LCD SDA / SCL | A4 / A5 |

## 6. The Code

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>
#include <EEPROM.h>

// ── Sensors ──────────────────────────────────────────────
const int LEFT_SENSOR   = A0;
const int CENTER_SENSOR = A1;
const int RIGHT_SENSOR  = A2;
const int LINE_THRESHOLD = 500;   // calibrate for your floor + line

// ── Motors ───────────────────────────────────────────────
const int ENA = 9, IN1 = 8, IN2 = 7;
const int ENB = 3, IN3 = 6, IN4 = 5;
const int BASE_SPEED = 150;

// ── Bluetooth ────────────────────────────────────────────
SoftwareSerial bluetooth(10, 11);

// ── LCD ──────────────────────────────────────────────────
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ── EEPROM ───────────────────────────────────────────────
const int EEPROM_RUN_COUNT_ADDR = 0;   // unsigned int, 2 bytes

// ── State machine ────────────────────────────────────────
enum RobotState { STOPPED, FOLLOWING, LOST_LINE, FINISHED };
RobotState state = STOPPED;

unsigned long lastStatusBroadcast = 0;
const unsigned long STATUS_INTERVAL = 1000;

unsigned int runCount = 0;

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);

  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);

  lcd.init();
  lcd.backlight();

  EEPROM.get(EEPROM_RUN_COUNT_ADDR, runCount);
  updateDisplay();
}

void loop() {
  handleBluetoothCommands();

  if (state == FOLLOWING) {
    followLine();
  }

  if (millis() - lastStatusBroadcast >= STATUS_INTERVAL) {
    lastStatusBroadcast = millis();
    broadcastStatus();
  }
}

void handleBluetoothCommands() {
  if (!bluetooth.available()) return;

  char cmd = bluetooth.read();
  if (cmd == 'S') {          // Start
    state = FOLLOWING;
  } else if (cmd == 'X') {   // Stop
    state = STOPPED;
    stopMotors();
  }
  updateDisplay();
}

void followLine() {
  bool left   = analogRead(LEFT_SENSOR)   < LINE_THRESHOLD;
  bool center = analogRead(CENTER_SENSOR) < LINE_THRESHOLD;
  bool right  = analogRead(RIGHT_SENSOR)  < LINE_THRESHOLD;

  if (left && center && right) {
    finishRun();
  } else if (center) {
    driveMotors(BASE_SPEED, BASE_SPEED);        // straight
  } else if (left) {
    driveMotors(BASE_SPEED / 2, BASE_SPEED);    // steer left
  } else if (right) {
    driveMotors(BASE_SPEED, BASE_SPEED / 2);    // steer right
  } else {
    state = LOST_LINE;
    stopMotors();
    updateDisplay();
  }
}

void finishRun() {
  state = FINISHED;
  stopMotors();
  runCount++;
  EEPROM.put(EEPROM_RUN_COUNT_ADDR, runCount);
  updateDisplay();
}

void driveMotors(int leftSpeed, int rightSpeed) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, leftSpeed);
  analogWrite(ENB, rightSpeed);
}

void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}

void broadcastStatus() {
  const char *stateName =
    state == FOLLOWING ? "FOLLOWING" :
    state == LOST_LINE ? "LOST_LINE" :
    state == FINISHED  ? "FINISHED"  : "STOPPED";

  bluetooth.print("State: "); bluetooth.print(stateName);
  bluetooth.print(" | Runs: "); bluetooth.println(runCount);
}

void updateDisplay() {
  lcd.clear();
  lcd.setCursor(0, 0);
  switch (state) {
    case FOLLOWING: lcd.print("Following...");  break;
    case LOST_LINE: lcd.print("Line Lost!");    break;
    case FINISHED:  lcd.print("Finished!");     break;
    case STOPPED:   lcd.print("Ready");         break;
  }
  lcd.setCursor(0, 1);
  lcd.print("Runs: "); lcd.print(runCount);
}
```

## 7. Challenges

### Challenge 1 — Smooth Steering ⭐⭐

Replace the fixed `BASE_SPEED / 2` steering correction with a proportional
one: the further off-center the robot drifts (use more than 3 sensors, or
an analog reflectance sensor array, if available), the sharper the
correction. This is the beginning of a **PID controller** — if you want to
go further, research the "P" (proportional) term first before adding "I"
and "D".

### Challenge 2 — Lost-Line Recovery ⭐⭐⭐

Instead of just stopping in `LOST_LINE`, remember which side (`left` or
`right`) the line was last seen on, and have the robot reverse-turn
briefly toward that side to try to reacquire it before giving up.

### Challenge 3 — Best-Time Tracking ⭐⭐⭐

Time each run with `millis()` from `S` (start) to hitting the finish
marker, and store the **best completion time** in EEPROM alongside
`runCount`, displaying "New Best!" on the LCD when a run beats it.

### Challenge 4 — Full Remote Dashboard ⭐⭐⭐

Extend `broadcastStatus()` to also send live sensor readings, and build a
simple companion app (or just a well-formatted terminal output) that lets
you watch the robot's decisions in real time from your phone as it runs —
useful for debugging why it loses the line at a particular corner.

---

There's no "Lecture 14" after this — from here, the fastest way to keep
learning is to pick a project of your own, and use this course as a
reference for whichever pieces it needs.
