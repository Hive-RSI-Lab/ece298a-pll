<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a charge-pump phase-locked loop. It locks a ring oscillator to the
reference clock on `clk` (5 to 12.5 MHz) at 8 × N times the reference, where N
is 1 to 5.

The analog half is a hard macro: a charge pump, a passive loop filter, a
current-starved ring VCO and its bias. After layout, the VCO covers about 13
to 165 MHz at every process, voltage and temperature corner (7 to 209 MHz at
the typical corner). Pick N and the reference so that 8 × N × f_ref falls in
that range. The nominal point is 6.25 MHz × 16 = 100 MHz. The loop filter's control voltage leaves the tile on
`ua[0]`, and `ua[1]` takes an optional external bias resistor.

The digital half closes the loop:

- A /8 prescaler divides the VCO clock, and a programmable /N divider set by
  `ui[2:0]` divides it again. Codes 0, 6 and 7 act as N = 1.
- A phase-frequency detector compares the divided clock with the reference
  and drives the charge pump's UP and DN switches. The same UP and DN also
  go out on `uo[3]` and `uo[4]`, so the PFD can be watched on a scope.
- A lock detector raises `LOCK` after 16 reference cycles in a row with no
  wide UP or DN pulse, and drops it on the next wide pulse.
- `ui[6]` enables the pump, bias and VCO, and `uio[1:0]` trims the pump
  current. Both are registered on `clk`.

`rst_n` resets every clock domain asynchronously.

## How to test

1. Drive a 5 to 12.5 MHz reference into `clk`, set N on `ui[2:0]`, and set
   `ui[6]` high to enable the loop. Release `rst_n`.
2. Watch `uo[2]` (`LOCK`) go high once the loop settles.
3. Measure `uo[0]`: with `ui[7]` low it carries the VCO divided by 8, and with
   `ui[7]` high the VCO divided by 16. Locked, the VCO sits at 8 × N times the
   reference.
4. `uo[1]` is the feedback clock (VCO / 8N), which should match the reference
   when locked.
5. `uo[3]` (`PFD_UP`) and `uo[4]` (`PFD_DN`) show the PFD's pulses. While the
   loop acquires, one of them stays high for most of each reference period.
   Once it is locked, both are narrow pulses once per reference period, a few
   nanoseconds wide (the PFD's reset delay). `uo[7:5]` are driven low.
6. To see the loop's control voltage, put a high-impedance probe on `ua[0]`.

## External hardware

A reference clock source and an oscilloscope or frequency counter. An external
bias resistor on `ua[1]` is optional.
