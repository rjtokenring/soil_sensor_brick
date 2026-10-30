# Soil Sensor Brick

This Brick reads a capacitive soil moisture sensor periodically and reports the moisture as a percentage with a dry/ok state. It is a sample third-party brick: without a real sensor it produces a simulated, slowly drifting reading.

## Overview

The Soil Sensor Brick allows you to:

- Take moisture readings at a fixed interval in the background.
- Receive every reading through a callback.
- Classify the soil as dry or ok against a configurable threshold.

## Features

- Pluggable `read` function: pass your own sensor reader, or use the simulated one
- Readings delivered to an `on_reading` callback and kept as `last_reading()`
- Threshold and period configurable from **Brick Configuration** or the constructor
- No hardware required to run

## Prerequisites

- **Supported boards**: Arduino® UNO™ Q and Arduino VENTUNO™ Q.
- **Sensor**: optional. Any function returning a percentage can act as the sensor.

## Code example and usage

### Simulated readings

```python
from arduino.app_utils import App
from soil_sensor import SoilSensor

def on_reading(reading):
    print(f"moisture {reading['moisture']}% -> {reading['state']}")

sensor = SoilSensor(on_reading=on_reading)

App.run()
```

### Your own sensor

```python
from arduino.app_utils import App
from soil_sensor import SoilSensor

def read_adc():
    raw = 512  # replace with the ADC value read from the sensor
    return 100 - raw / 1023 * 100

sensor = SoilSensor(read=read_adc, threshold=35)

App.run()
```

## Configuration

Set these variables in **Brick Configuration** in App Lab:

| Variable | Description | Default |
|----------|-------------|---------|
| `SOIL_THRESHOLD` | Moisture percentage below which the soil is reported as dry | `40` |
| `SOIL_PERIOD_SEC` | Seconds between two readings | `5` |

Both can also be passed to the constructor: `SoilSensor(threshold=35, period_sec=10)`.

## Methods

- **`read_once()`**: Takes a single reading and returns a dictionary with `moisture`, `state` and `threshold`.
- **`last_reading()`**: Returns the most recent reading, or `None` before the first one.

## Errors

- The constructor raises `ValueError` if the threshold is outside 0-100 or the period is not positive.
- A `read` function that raises stops the loop with the original exception, visible in the app logs.

## License

MPL-2.0. See the SPDX headers in the source files.
