# Device Clock Drift Investigation

## Problem
One of the biometric devices in the plant had its internal clock running approximately 1 hour ahead of standard time, causing employee check-in times to appear abnormally late.

## Detection Method
We compared the average check-in time per device ID against scheduled shift start times. Device `DEV-04` showed a consistent +60 minute offset across all assigned employee punches compared to the rest of the gateway devices.

## Solution
In Stage 2 cleaning, we applied a -1 hour correction offset to all raw timestamps originating from `DEV-04` before pairing check-ins and check-outs.
