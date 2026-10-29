# SPDX-FileCopyrightText: Copyright (C) Arduino s.r.l. and/or its affiliated companies
#
# SPDX-License-Identifier: MPL-2.0

"""Soil Sensor brick: periodic moisture readings with a dry/ok state.

Sample third-party brick used to exercise the registry flow. The reading is
simulated when no `read` function is given, so the brick runs on any board.
"""

from __future__ import annotations

import os
import random
import threading
import time
from collections.abc import Callable
from typing import TypedDict

from arduino.app_utils import Logger, brick

logger = Logger("SoilSensor")


class Reading(TypedDict):
    moisture: float
    state: str
    threshold: int


@brick
class SoilSensor:
    """Reads soil moisture periodically and reports it as a percentage.

    Args:
        read: Optional function returning the moisture percentage (0-100).
            When omitted, a slowly drifting simulated value is used.
        on_reading: Optional callback invoked with every `Reading`.
        threshold: Moisture percentage below which the soil is dry. Defaults
            to the `SOIL_THRESHOLD` variable.
        period_sec: Seconds between readings. Defaults to `SOIL_PERIOD_SEC`.
    """

    def __init__(
        self,
        read: Callable[[], float] | None = None,
        on_reading: Callable[[Reading], None] | None = None,
        threshold: int | None = None,
        period_sec: float | None = None,
    ) -> None:
        self._read = read or self._simulated_read
        self._on_reading = on_reading
        self.threshold = int(threshold if threshold is not None else os.getenv("SOIL_THRESHOLD", "40"))
        self.period_sec = float(period_sec if period_sec is not None else os.getenv("SOIL_PERIOD_SEC", "5"))
        if not 0 <= self.threshold <= 100:
            raise ValueError("threshold must be between 0 and 100")
        if self.period_sec <= 0:
            raise ValueError("period_sec must be positive")
        self._lock = threading.Lock()
        self._last: Reading | None = None
        self._simulated = 45.0

    def start(self) -> None:
        logger.info(f"Starting SoilSensor (threshold={self.threshold}%, period={self.period_sec}s)")

    def stop(self) -> None:
        logger.info("Stopping SoilSensor")

    def loop(self) -> None:
        """Takes one reading, stores it and notifies the callback. Called repeatedly by the framework."""
        reading = self.read_once()
        if self._on_reading is not None:
            self._on_reading(reading)
        time.sleep(self.period_sec)

    def read_once(self) -> Reading:
        """Takes a single reading and returns it."""
        from tabulate import tabulate  # imported here to keep the app start fast

        moisture = max(0.0, min(100.0, float(self._read())))
        reading: Reading = {
            "moisture": round(moisture, 1),
            "state": "dry" if moisture < self.threshold else "ok",
            "threshold": self.threshold,
        }
        with self._lock:
            self._last = reading
        logger.info("\n" + tabulate([[reading["moisture"], reading["state"]]], headers=["moisture %", "state"]))
        return reading

    def last_reading(self) -> Reading | None:
        """Returns the most recent reading, or None before the first one."""
        with self._lock:
            return self._last

    def _simulated_read(self) -> float:
        self._simulated += random.uniform(-3.0, 3.0)
        self._simulated = max(5.0, min(95.0, self._simulated))
        return self._simulated
