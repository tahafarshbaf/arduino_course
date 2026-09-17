# Arduino Italiano!

## History

The idea of creating Arduino took shape in 2003 at the IDII (Interaction Design Institute Ivrea) in Italy. The idea was to build a simple, low-cost device for students to carry out digital projects, especially those who did not have much familiarity with the principles of engineering and programming. Three key individuals played a role in realizing this idea: Hernando Barragán, Massimo Banzi, and Casey Reas.

Barragán was a student at the Ivrea Institute who decided to carry out his master's thesis in this field. Banzi and Reas were Barragán's thesis advisors. At that time, the name "Arduino" did not yet exist. The outcome of Barragán's thesis was highly successful and led to the creation of hardware and software called "Wiring." The Wiring hardware possessed the desired characteristics compared to other available products on the market at the time—namely, it was simple and low-cost. The Wiring software was also based on an existing programming language called "Processing."

After the completion of the thesis, Banzi set out to reduce the costs of the Wiring hardware. In 2005, in collaboration with David Cuartielles and David Mellis (who were, respectively, an employee and a student at the Ivrea Institute), he developed the Wiring project and changed its name to "Arduino." This new name was derived from a bar called "Arduino" in the town of Ivrea, where most of the group's meetings were held. The word "Arduino" is also the name of an ancient Italian king who was once the ruler of the town of Ivrea and became King of Italy in the 11th century. Gradually, the core team of Arduino was formed with five main individuals: Banzi, Cuartielles, Mellis, and two new members named Tom Igoe and Gianluca Martino. Among the members of this five-person group, Barragán's name (the thesis author) is not seen, and he was never invited to participate in this group. [1](Refrences.md#hakimi-arduino-key)

![](Images/Interaction%20Design%20Institute%20Ivrea.png)


This five-person team registered the Arduino trademark in the United States in 2008. Around the same time, Martino, one of the members of this group, secretly registered the Arduino name for himself in Italy and began operating in parallel with the main company, personally producing and selling the product. The legal complexities that arose around the Arduino trademark forced the original company in the United States to use the trademark "Genuino" for selling its products outside of America. The specifications and features of Genuino boards are exactly similar to those of Arduino and have no difference from it.

The Arduino platform consists of both hardware and software components. This chapter introduces the Arduino hardware.

There are various models of Arduino boards available on the market, but the most suitable model for beginners is the **"Uno R3 DIP"** , and the explanations in this section of the book are presented according to this model. The word "Uno" means "one" in Italian. "R3" stands for Revision 3, indicating the third version of the Arduino Uno board, which has undergone revisions and improvements compared to its predecessors. The term "DIP" refers to the type of microcontroller used on the board, which will be explained below.

## Microcontroller: ATmega328P

The heart of the Arduino Uno R3 DIP is the **ATmega328P** microcontroller. This is the chip that executes the program you write. The "DIP" (Dual In-line Package) designation means that the microcontroller is housed in a package with pins that can be inserted into a socket on the board. This is a key feature for beginners because if the chip gets damaged, it can be easily removed and replaced without needing to solder or buy a new board.

Some key specs worth knowing up front, because they explain limits you'll
run into later:

| Spec | Value | Why it matters |
|---|---|---|
| Clock speed | 16 MHz | How many basic instructions per second the chip can run — plenty for these projects, but not for heavy math or video |
| Flash memory | 32 KB | Where your compiled program is stored; a "sketch too big" error means you've filled this |
| SRAM | 2 KB | Where variables live while the program runs; overflow this and behavior gets silently weird, not a clean error |
| EEPROM | 1 KB | Small memory that **survives power loss** — used in Lecture 07 to remember settings after a reset |
| Operating voltage | 5V | Every pin expects signals around 0V (LOW) or 5V (HIGH) |

## The Board: Pinout

```
                    ┌─────────────────────────────┐
             RESET →│ [ ]                     [ ] │→ 13
                    │ [ ]  3V3                [ ] │→ 12
                    │ [ ]  5V                 [ ]~│→ 11 (PWM)
                    │ [ ]  GND               [ ]~ │→ 10 (PWM)
                    │ [ ]  GND                [ ]~│→ 9  (PWM)
                    │ [ ]  Vin                [ ] │→ 8
                    │                              │
             A0    →│ [ ]                     [ ] │→ 7
             A1    →│ [ ]                    [ ]~ │→ 6  (PWM)
             A2    →│ [ ]                    [ ]~ │→ 5  (PWM)
             A3    →│ [ ]                     [ ] │→ 4
             A4    →│ [ ]                    [ ]~ │→ 3  (PWM) / INT1
             A5    →│ [ ]                     [ ] │→ 2  INT0
                    │             [USB]      TX→[ ]│→ 1  (TX)
                    │                        RX→[ ]│→ 0  (RX)
                    └─────────────────────────────┘
```

| Pin group | Purpose |
|---|---|
| `0`–`13` | **Digital** I/O — read/write HIGH or LOW. Pins marked `~` (3, 5, 6, 9, 10, 11) also support `analogWrite()` (PWM — see Lecture 04) |
| `A0`–`A5` | **Analog input** — read a continuous voltage with `analogRead()` (see Lecture 04); can also be used as extra digital pins |
| `2`, `3` | Digital pins that double as **external interrupt** sources (`INT0`, `INT1`) — used in Lecture 09 |
| `5V` / `3.3V` | Regulated power output for external components |
| `GND` | Ground — the 0V reference every circuit needs, shared with any external power supply (see Lecture 00) |
| `Vin` | Raw voltage input if powering the board from something other than USB (e.g. a 9V battery) |
| `RESET` | Restarts the running program from `setup()` |
| `0` (RX) / `1` (TX) | Serial communication pins — used internally by `Serial.print()` over USB; avoid using them for other components while also using Serial |

## The Arduino IDE

The **IDE** (Integrated Development Environment) is the program you write
and upload code with.

1. **Install** it from [arduino.cc/en/software](https://www.arduino.cc/en/software), or use the [Wokwi](https://wokwi.com/) online simulator to skip installation entirely for now.
2. **Connect** the board via USB, then in the IDE go to `Tools → Board` and select **Arduino Uno**, and `Tools → Port` to select the port your board appears on.
3. **Write** your code in the editor — every sketch needs exactly two functions:

```cpp
void setup() {
  // runs once, when the board powers on or resets
}

void loop() {
  // runs over and over, forever, after setup() finishes
}
```

This `setup()` / `loop()` structure is doing the same job as the `main()`
function from the [Pre-Course C primer](<../Pre-Course/01-C-Fundamentals-Primer.md>) —
Arduino just splits it into "run once" and "run forever" for you, since
that's the shape almost every embedded program takes.

4. **Upload**: click the → (Upload) button. The IDE compiles your code and
   sends it to the board over USB. Watch the small LEDs near the USB port
   blink during the transfer — a bar at the bottom will confirm "Done
   uploading."

> [!NOTE]
> If upload fails with a port or "not found" error, the two most common
> causes are: the wrong board/port is selected under `Tools`, or another
> program (like the Serial Monitor from a previous run) is still holding
> the port open.

Once you can get a sketch to compile and upload without errors, you're
ready for [Lecture 03 - Blink](<./03-Blink.md>) — your first program that
actually does something you can see.

