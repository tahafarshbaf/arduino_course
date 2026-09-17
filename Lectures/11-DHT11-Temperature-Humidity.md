# Project 12 — Temperature & Humidity Logging with DHT11

## 1. What Are We Building?

A small **weather station**: a DHT11 sensor reports temperature and
humidity, both are shown on the LCD, and a fan (simulated with an LED, or
a real DC motor from Lecture 10) turns on automatically past a heat
threshold — the same pattern as the Fire Alarm System in Lecture 05, but
with a real digital sensor and library instead of a simple analog
threshold.

## 2. What Will You Learn?

- Using a **third-party library** end to end: installing it, reading its
  documentation, calling its functions
- The difference between an **analog sensor** (LDR, potentiometer — a
  continuous voltage you interpret yourself) and a **digital sensor**
  (DHT11 — a chip that does its own measuring and hands you a finished
  number over a single data wire)
- Basic **data logging**: printing readings with a timestamp for later
  review
- Combining a sensor threshold with actuator output, same shape as
  Lecture 05

## 3. Components Needed

| Quantity | Component | Notes |
|----------|-----------|-------|
| 1 | Arduino Uno | |
| 1 | DHT11 sensor module | Often sold pre-mounted with a pull-up resistor already on the breakout board |
| 1 | 16×2 I2C LCD | From Lecture 07 |
| 1 | LED + 220 Ω resistor | Stands in for a fan/heater relay |
| 1 | Breadboard + jumper wires | |

## 4. Key Concepts

### 4.1 Installing a Library

Nearly every sensor beyond a raw analog voltage ships with a library that
handles its specific communication protocol. In the Arduino IDE:

`Sketch → Include Library → Manage Libraries...` → search **"DHT sensor
library"** by Adafruit → Install (it will also ask to install the
**Adafruit Unified Sensor** dependency — accept that too).

This is the same idea as `#include <Wire.h>` or
`#include <LiquidCrystal_I2C.h>` from earlier projects — someone already
wrote the hard part (talking to the exact timing protocol this chip
expects), and packaged it as functions you call.

### 4.2 Reading the Sensor

```cpp
#include <DHT.h>

const int DHT_PIN = 2;
DHT dht(DHT_PIN, DHT11);

void setup() {
  dht.begin();
}

void loop() {
  float humidity    = dht.readHumidity();
  float temperature = dht.readTemperature();   // Celsius by default

  if (isnan(humidity) || isnan(temperature)) {
    // isnan() = "is Not a Number" — the read failed, don't use the value
    return;
  }

  // use humidity / temperature here
}
```

> [!CAUTION]
> The DHT11 is slow — it can only be read reliably about **once every 2
> seconds**. Calling `dht.readTemperature()` more often than that returns
> stale or invalid data. This is a hardware limitation, not a bug in your
> code — space your reads out with the non-blocking `millis()` pattern
> from Lecture 03, not a 2-second `delay()` that would freeze everything
> else.

### 4.3 Analog vs. Digital Sensors, Compared

| | LDR (Lecture 09) / Potentiometer (Lecture 04) | DHT11 |
|---|---|---|
| What you read | A raw voltage (`analogRead()`, 0–1023) | A finished, calibrated value (`dht.readTemperature()`) |
| Who does the math | You (voltage divider, scaling) | The sensor's internal chip |
| Wiring | Any analog pin | Any digital pin (it has its own protocol, not `analogRead`) |
| Speed | Instant, read as often as you like | Limited to ~1 reading / 2 sec |

## 5. Pin Connections

| Component | Arduino Pin |
|---|---|
| DHT11 → Data | 2 |
| DHT11 → VCC | 5V |
| DHT11 → GND | GND |
| LCD SDA | A4 |
| LCD SCL | A5 |
| Fan LED (+) | 220Ω → Pin 8 |

## 6. The Code

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

const int DHT_PIN  = 2;
const int FAN_PIN  = 8;
const float HEAT_THRESHOLD_C = 28.0;
const unsigned long READ_INTERVAL = 2500;   // DHT11 needs ≥2s between reads

DHT dht(DHT_PIN, DHT11);
LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastReadTime = 0;
unsigned long readingCount = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();
  lcd.init();
  lcd.backlight();
  pinMode(FAN_PIN, OUTPUT);
}

void loop() {
  if (millis() - lastReadTime < READ_INTERVAL) {
    return;   // not time for a new reading yet — don't block, just skip
  }
  lastReadTime = millis();

  float humidity    = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("DHT11 read failed — skipping this cycle");
    return;
  }

  readingCount++;

  // ── Log to Serial with a running reading count ──────────────
  Serial.print("[");
  Serial.print(readingCount);
  Serial.print("] Temp: "); Serial.print(temperature, 1);
  Serial.print(" C | Humidity: "); Serial.print(humidity, 1);
  Serial.println(" %");

  // ── Display on LCD ───────────────────────────────────────────
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: "); lcd.print(temperature, 1); lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Hum:  "); lcd.print(humidity, 1); lcd.print("%");

  // ── Fan control ──────────────────────────────────────────────
  bool fanOn = temperature > HEAT_THRESHOLD_C;
  digitalWrite(FAN_PIN, fanOn ? HIGH : LOW);
}
```

## 7. Exercises & Challenges

### Exercise 1 — Min/Max Tracking ⭐

Keep track of the highest and lowest temperature seen since power-on, and
display them on request (e.g. when a button is pressed).

### Exercise 2 — Heat Index Warning ⭐⭐

High humidity makes heat feel worse than the thermometer alone suggests.
Add a second threshold: if `temperature > 25` **and** `humidity > 70`,
show a "Muggy!" warning instead of the normal readout.

### Exercise 3 — EEPROM Data Log ⭐⭐⭐

Using the EEPROM technique from Lecture 07, store the last 20 temperature
readings in EEPROM as a circular buffer, so a power cycle doesn't lose
recent history. Add a way to print the whole log over Serial on startup.

### Exercise 4 — Rolling Average ⭐⭐

Apply the moving-average technique from Lecture 04 (Section 8.5) to the
temperature readings, to smooth out any noise before deciding whether to
turn the fan on — this avoids the fan flickering on/off right at the
threshold.
