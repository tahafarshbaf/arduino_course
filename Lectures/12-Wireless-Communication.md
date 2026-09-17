# Project 13 — Wireless Control with Bluetooth (HC-05)

## 1. What Are We Building?

Every project so far is controlled by something physically wired to the
Arduino — a button, a keypad, a potentiometer. This project replaces that
with a **phone**: an HC-05 Bluetooth module lets any Bluetooth serial
terminal app send commands wirelessly to turn an LED on/off and read back
a sensor value, no wires involved.

The bigger idea being introduced is that **Bluetooth Serial is still just
`Serial`** — everything you already know about `Serial.print()` and
`Serial.read()` transfers directly; only the wire is missing.

## 2. What Will You Learn?

- Wiring and configuring an HC-05 module for basic use
- **`SoftwareSerial`**: giving the Arduino a second serial port on
  ordinary digital pins, since pins 0/1 (the hardware serial port) are
  already used by the USB/Serial Monitor connection
- Designing a tiny **command protocol** (single characters) to control
  hardware remotely
- Why this is the same pattern used later by WiFi (ESP8266/ESP32) modules
  — the transport changes, the "read a command, act on it" logic doesn't

## 3. Components Needed

| Quantity | Component | Notes |
|----------|-----------|-------|
| 1 | Arduino Uno | |
| 1 | HC-05 Bluetooth module | Pre-paired "slave" mode works out of the box |
| 1 | LED + 220 Ω resistor | The thing being controlled |
| 1 | Potentiometer | A value to read back over Bluetooth |
| — | A phone with a Bluetooth serial terminal app | e.g. "Serial Bluetooth Terminal" (Android) |

## 4. Key Concepts

### 4.1 Why `SoftwareSerial`?

The Arduino Uno has exactly **one hardware serial port**, on pins 0
(RX) and 1 (TX) — and that same port is what `Serial.print()` uses to
talk to your computer over USB. If the HC-05 were also wired to pins 0/1,
the two would collide.

The `SoftwareSerial` library solves this by *emulating* a serial port
in software on any two ordinary digital pins:

```cpp
#include <SoftwareSerial.h>

const int BT_RX = 10;   // Arduino receives on this pin
const int BT_TX = 11;   // Arduino transmits on this pin
SoftwareSerial bluetooth(BT_RX, BT_TX);

void setup() {
  Serial.begin(9600);      // USB — for debugging, printed to your computer
  bluetooth.begin(9600);   // HC-05 — talks to your phone
}
```

> [!NOTE]
> Wire the HC-05's **TX to the Arduino's `BT_RX` pin**, and its **RX to
> `BT_TX`** — TX always connects to RX, never TX-to-TX. This crossover is
> easy to get backwards and is the most common reason "nothing happens."

### 4.2 A Minimal Command Protocol

Rather than sending whole words, single characters keep both sides simple:

| Command sent from phone | Meaning |
|---|---|
| `1` | Turn LED ON |
| `0` | Turn LED OFF |
| `?` | Reply with the current potentiometer reading |

This mirrors the keypad-driven state machine from Lecture 07 — a
character comes in, a `switch` or `if` chain decides what it means. The
transport (keypad wires vs. Bluetooth) is irrelevant to that logic.

## 5. Pin Connections

| Component | Arduino Pin |
|---|---|
| HC-05 TX | 10 (BT_RX) |
| HC-05 RX | 11 (BT_TX) — *via a voltage divider, see caution below* |
| HC-05 VCC | 5V |
| HC-05 GND | GND |
| LED (+) | 220Ω → Pin 13 |
| Potentiometer wiper | A0 |

> [!CAUTION]
> The HC-05's RX pin expects **3.3V logic**, but the Arduino Uno's TX pin
> outputs 5V. Wiring it directly can damage the module over time. Use a
> simple voltage divider (two resistors, e.g. 1kΩ and 2kΩ, as covered in
> Lecture 00) between the Arduino's TX pin and the HC-05's RX pin to step
> the signal down. The other direction (HC-05 TX → Arduino RX) is safe as-is,
> since 3.3V still reads as a valid HIGH to the Arduino.

## 6. The Code

```cpp
#include <SoftwareSerial.h>

const int BT_RX  = 10;
const int BT_TX  = 11;
const int LED_PIN = 13;
const int POT_PIN = A0;

SoftwareSerial bluetooth(BT_RX, BT_TX);

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Bluetooth ready — send 1, 0, or ?");
}

void loop() {
  if (bluetooth.available()) {
    char command = bluetooth.read();

    switch (command) {
      case '1':
        digitalWrite(LED_PIN, HIGH);
        bluetooth.println("LED ON");
        break;

      case '0':
        digitalWrite(LED_PIN, LOW);
        bluetooth.println("LED OFF");
        break;

      case '?': {
        int potValue = analogRead(POT_PIN);
        bluetooth.print("Pot: ");
        bluetooth.println(potValue);
        break;
      }

      default:
        bluetooth.println("Unknown command");
    }

    // Mirror everything to the USB Serial Monitor too, for debugging
    Serial.print("Received: ");
    Serial.println(command);
  }
}
```

## 7. Exercises & Challenges

### Exercise 1 — Multi-Character Commands ⭐⭐

Extend the protocol to accept a full word followed by newline (e.g.
`"BLINK\n"`) using `bluetooth.readStringUntil('\n')` instead of single
characters, and trigger a 5-second blink pattern when it's received.

### Exercise 2 — Bluetooth-Controlled Servo ⭐⭐

Combine this project with Lecture 06: send an angle as text (e.g. `"90"`)
over Bluetooth and move a servo to that angle. You'll need to parse the
incoming text into a number — look up `.toInt()` on the received `String`.

### Exercise 3 — Status Broadcast ⭐⭐⭐

Instead of only responding to `?`, have the Arduino automatically send
the potentiometer reading over Bluetooth every 2 seconds (non-blocking,
`millis()`-based, per Lecture 03) so the phone app shows a live-updating
value without having to ask for it.

### Bonus — From Bluetooth to WiFi

Everything here generalizes: an **ESP8266** or **ESP32** module (or an
ESP32 as the main board, replacing the Uno entirely) exposes a WiFi
connection instead of Bluetooth, but the same "receive a command, act on
it" loop applies — only now the commands can come from anywhere on the
internet instead of just a nearby phone. If you want to push further,
look up the `ESP8266WebServer` or `ESP32 WebServer` library and try
serving a simple webpage with an ON/OFF button in place of the phone app.
