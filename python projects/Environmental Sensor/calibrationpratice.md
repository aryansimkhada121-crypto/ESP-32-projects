## Soil Moisture Sensor Calibration

## Sensor Info

    - Model: HW-080 (probe) + HW-103 (breakout/interface board) — sold as one unit
    - Reading via: AO (analog output) pin, ADC on ESP32
    - Date tested: 2026-08-29

## Procedure 
    Step 1: Prep the Soil
    - Dig a sample of soil into a small bucket, then split it into two small containers/cups. 
    - Clean out any rocks/debris/roots
    - Label the two containers, one as a dry sample and one as wet.
    
    Step 2: Create dry and wet conditions.
    - Dry labeled container: Leave it alone.
    - Wet labeled container: Add water slowly, mix, and stop when thoroughly absorbed.
    
    Step 3: Measurements

    Precaution: 
    - For each container, fully insert the probes to remove any air pockets.
    - Wait at least 10-15 seconds for the readings to stabilize before recording data.
    - Take 3 values, then take the average for more accurate values.
    - Dry and clean the probes before another attempt.

    to get volume of the specific cup use:

    Volume = 1/12 x π x h (D^2 + Dd + d^2)

    D - diameter of the larger circle (cm)
    d - diameter of the smaller circle (cm)
    h - height of cup (cm)

    Volume = 204 cm^3
    1 cm^3 = 1 ml

    2 cm gap at the top removes a large chunk of the total volume (roughly 25% to 30% of it).
    145 mL to 155 mL of actual soil

    45% water target: 150 ml x 0.45 = 67.5 ml of water needed
    
    | Container | Reading 1 | Reading 2 | Reading 3 | Average |
    |___________|___________|___________|___________|_________|
    | DRY       | 44079.33  | 44424.19  |   36710   |         | DRY_VALUE = 41737.84
    | WET       | 19600.88  | 10538.63  |  9935.09  |         | WET_VALUE = 13358.20
    
    Step 4: 
    How does the sensor function?- What do the WET_VALUE and DRY_VALUE represent physically? Does a higher value mean dry soil, or vice versa? And how should this be interpreted in this project?

    - The WET_VALUE and DRY_VALUE represent the percentage of moisture detected by the sensor; a higher value received by the sensor, e.g., DRY_VALUE, represents the soil in a state where it is in need of water, whereas the WET_VALUE state represents the state after the soil has received a certain calculated percentage of water relative to the volume the soil occupies in the cup/container. When the sensor reads a high value, it can be interpreted as the soil is becoming/is already dry and is in need of watering, whereas when it reads a low value, water has been supplied and the soil is in good condition for the plants.
    
## Final Results
- DRY_VALUE = 41737.84
- WET_VALUE = 13358.20
- Direction confirmed: +higher = dry ; -lower = wet
- Threshold chosen for "needs water": Threshold>41737.84 
- Reasoning for that threshold: As the soil chosen was already quite moist, the threshold for needing water must be higher, as providing water earlier/at a lower value in this case would lead to overflowing/flooding and damaging the plants.