# Soil Sensor Brick

This Brick reads a capacitive soil moisture sensor periodically and reports the moisture as a percentage with a dry/ok state. It is a sample third-party brick: without a real sensor it produces a simulated, slowly drifting reading.

## Overview

The Soil Sensor Brick allows you to:

- Take moisture readings at a fixed interval in the background.
- Receive every reading through a callback.
- Classify the soil as dry or ok against a configurable threshold.

