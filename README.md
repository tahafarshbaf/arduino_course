# Hands on Arduino!

**Beginner Arduino programming course — Shahid Rajaei University**

A from-scratch, project-based path into embedded systems: starting from "what is a microcontroller" and ending with a working security system, built one concept at a time.


## 🚀 Pre-Course

Before Lecture 01, [`Pre-Course/`](./Pre-Course) gets you comfortable writing and debugging plain C — no hardware, no breadboard, just code — so the projects later test your circuits, not your grasp of `for` loops.

| Page | What it covers |
|---|---|
| [Welcome](<./Pre-Course/00-Welcome.md>) | Why a pre-course, and how to use it |
| [C Fundamentals Primer](<./Pre-Course/01-C-Fundamentals-Primer.md>) | `main()`, `printf`/`scanf`, types, operators, loops, functions |
| [Practice Problems](<./Pre-Course/02-Practice-Problems.md>) | Factorial series, Armstrong numbers, Goldbach's conjecture, prime/perfect numbers, Taylor series (π, sine) |

<br/>

## 📖 Lectures

Each lecture lives in [`Lectures/`](./Lectures) and builds directly on the one before it.

| # | Lecture | What it covers |
|---|---|---|
| 00 | [Electronics Fundamentals](<./Lectures/00-Electronics%20Fundamentals.md>) | Ohm's law, resistor color codes, breadboards, power budgets, multimeters |
| 01 | [Introduction](<./Lectures/01-Introduction.md>) | Arduino's history, the Uno R3 pinout, the IDE, uploading your first sketch |
| 02 | [C Overview](<./Lectures/02-C Overview.md>) | Variables, loops, conditionals, functions — the language fundamentals |
| 03 | [Blink](<./Lectures/03-Blink.md>) | Your first program: digital output, `pinMode`, `digitalWrite`, non-blocking timing with `millis()` |
| 04 | [Potentiometer](<./Lectures/04-Potentiometer.md>) | Analog input, `analogRead`, mapping values, smoothing noisy readings |
| 05 | [Fire Alarm System](<./Lectures/05-Fire%20Alarm%20System.md>) | Sensors, thresholds, conditional logic in a real project |
| 06 | [Servo](<./Lectures/06-Servo.md>) | PWM signals, controlling a servo motor, easing/smooth motion |
| 07 | [Security System](<./Lectures/07-Security%20System.md>) | Putting it all together — sensors, logic, EEPROM, and actuation in one build |
| 08 | [Tank Level Control](<./Lectures/08-Tank Level Control.md>) | Enums, state machines, and cleaner control-flow patterns |
| 09 | [Speed Measurement](<./Lectures/09-SpeedMeasurement.md>) | Hardware interrupts, `attachInterrupt()`, ISRs, and the `volatile` keyword |
| 10 | [DC Motor Driver](<./Lectures/10-DC-Motor-Driver.md>) | H-bridges, the L298N driver, driving and steering two motors |
| 11 | [DHT11 Temperature & Humidity](<./Lectures/11-DHT11-Temperature-Humidity.md>) | Third-party libraries, digital sensors, basic data logging |
| 12 | [Wireless Communication](<./Lectures/12-Wireless-Communication.md>) | Bluetooth (HC-05), `SoftwareSerial`, remote control protocols |
| 13 | [Capstone Project](<./Lectures/13-Capstone-Project.md>) | A line-following robot combining every concept from the course |

<br/>

## 🖥️ Online Compilers

No local setup needed to start writing C:

1. [Compiler 1](https://compiler.edroca.com/)
2. [Compiler 2](https://matlabkar.com/tryit_codes/tryit.php?lang=c_gcc)
3. [Compiler 3](https://sourcesara.com/compiler/editor/c)

<br/>

## 🔧 Simulators

**Why use a simulator?**

- **Zero risk, zero cost** — you can't damage components with a wrong connection, and it's free to start
- **Convenience and speed** — no waiting for parts to ship or debugging physical wiring; test an idea instantly
- **Accessibility** — anyone with a browser can learn embedded systems without buying hardware first

**Online:**
1. [Wokwi](https://wokwi.com/) — free simulator for Arduino, ESP32, and Raspberry Pi Pico, entirely in-browser
2. [Tinkercad](https://www.tinkercad.com/) — best known for 3D design, but its Circuits feature simulates electronics and microcontrollers too

**Offline:**
1. [Fritzing](https://soft98.ir/software/engineering/199-fritzing.html)
2. [Proteus](https://soft98.ir/software/engineering/3535-%D8%AF%D8%A7%D9%86%D9%84%D9%88%D8%AF-proteus.html)

<br/>

## 📚 References

1. *Beginning C for Arduino* — Jack Purdum, Ph.D.
2. *Arduino Key* — Ardeshir Hakimi

<br/>

## 🛠️ Getting Started

1. Pick a compiler or simulator from above (Wokwi is the easiest starting point — no installs, no hardware required).
2. Work through [Pre-Course](<./Pre-Course/00-Welcome.md>) first — no hardware needed yet, just C.
3. Then read [Lecture 00](<./Lectures/00-Electronics%20Fundamentals.md>) and work through the lectures in order.

<br/>

## License

MIT — see [LICENSE](./LICENSE).
