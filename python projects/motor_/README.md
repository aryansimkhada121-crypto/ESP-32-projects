# ESP32 Indexing Platform (Object Detection Turntable)

An autonomous, sensor-driven system that rotates a 4-station platform, checks each station for a present object using an ultrasonic sensor, and reports status through a TFT display, RGB LED, and buzzer.

## How it works

1. A 28BYJ-48 stepper motor (via ULN2003 driver) rotates the platform 90° to bring the next station into position.
2. An HC-SR04 ultrasonic sensor, mounted above the platform facing down, measures the distance to whatever is directly below it.
3. That reading is compared against a calibrated empty-tray baseline. A meaningfully shorter reading means something is occupying that station.
4. The result is reported three ways at once:
   - TFT display shows the live distance reading and station status
   - RGB LED shows green (clear) or red (object detected)
   - Buzzer plays a distinct tone for "scanning" vs. "object detected"
5. The platform then advances to the next station and repeats.

## Components

- ESP32 (30-pin dev board)
- 28BYJ-48 stepper motor + ULN2003 driver board
- HC-SR04 ultrasonic sensor
- ST7735S 1.8" TFT display (SPI)
- RGB LED (common cathode) + 220Ω resistors
- Passive buzzer + PN2222A transistor + 1kΩ base resistor

## Repo structure

```
motor_[project_name]/
├── code.py
├── README.md
├── schematic/
│   ├── schematic.kicad_sch
│   └── schematic.pdf
├── cad/
│   ├── assembly/
│   │   └── full_assembly.stl
│   └── parts/
│       ├── platform.stl
│       ├── base.stl
│       └── sensor_arm.stl
└── photos/
    ├── build.jpg
    └── working_demo.jpg
```

## Calibration

Detection relies on `EMPTY_BASELINE` in `code.py` — the sensor's measured distance to an empty station. **This value is tied to the physical mount height** and must be re-measured any time the sensor's position changes (e.g. switching from the prototype mount to the final 3D-printed one). To recalibrate: run the sensor alone with the tray empty, take several readings, and update the constant with the observed average.

`THRESHOLD` sets how far below baseline a reading must drop to count as "object present" — it exists to absorb normal sensor jitter (typically well under 1cm in testing) without producing false positives.

## Known limitations / current state

- The sensor mount currently in use is a cardboard prototype rig, not the final 3D-printed bracket (in progress, pending filament). Readings are noticeably more consistent once the final mount is installed, since the prototype introduces some angle drift.
- Detection is based on distance-to-baseline comparison rather than a dedicated presence sensor (e.g. IR break-beam) — this works well for a fixed, known geometry like this one, but is sensitive to recalibration if the mount changes.

## Credits

Stepper motor step-sequencing logic adapted from concepts in:
- Rui Santos & Sara Santos — [Random Nerd Tutorials](https://RandomNerdTutorials.com/raspberry-pi-pico-stepper-motor-micropython/)
- Forked reference: [larsks/micropython-stepper-motor](https://github.com/larsks/micropython-stepper-motor/blob/master/motor.py)

## Future improvements

- Swap cardboard sensor mount for final 3D-printed bracket
- Add non-blocking buzzer state transitions (only tone on state change, not every loop)
- Expand to more stations / variable station count