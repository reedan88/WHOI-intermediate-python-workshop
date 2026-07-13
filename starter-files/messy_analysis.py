"""
Quick look at the mooring data from last week's deployment.

TODO: clean this up, it's getting hard to maintain every time I add a variable
"""

import csv

# --- load the data -----------------------------------------------------

timestamps = []
temperature_readings = []
salinity_readings = []
do_readings = []

with open("data/ooi_mooring_sample.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        timestamps.append(row["timestamp"])

        temp = row["temperature_c"]
        temperature_readings.append(float(temp) if temp != "" else None)

        sal = row["salinity_psu"]
        salinity_readings.append(float(sal) if sal != "" else None)

        do = row["dissolved_oxygen_umol_kg"]
        do_readings.append(float(do) if do != "" else None)

# --- temperature ---------------------------------------------------------

cleaned = [v for v in temperature_readings if v is not None]
n = len(cleaned)
mean = sum(cleaned) / n
variance = sum((v - mean) ** 2 for v in cleaned) / n
std = variance ** 0.5
minimum = min(cleaned)
maximum = max(cleaned)
print(f"temperature_c: mean={mean:.2f}, std={std:.2f}, min={minimum:.2f}, max={maximum:.2f}, n={n}")

# --- salinity --------------------------------------------------------------

cleaned = [v for v in salinity_readings if v is not None]
n = len(cleaned)
mean = sum(cleaned) / n
variance = sum((v - mean) ** 2 for v in cleaned) / n
std = variance ** 0.5
minimum = min(cleaned)
maximum = max(cleaned)
print(f"salinity_psu: mean={mean:.2f}, std={std:.2f}, min={minimum:.2f}, max={maximum:.2f}, n={n}")

# --- dissolved oxygen -----------------------------------------------------

cleaned = [v for v in do_readings if v is not None]
n = len(cleaned)
mean = sum(cleaned) / n
variance = sum((v - mean) ** 2 for v in cleaned) / n
std = variance ** 0.5
minimum = min(cleaned)
maximum = max(cleaned)
print(f"dissolved_oxygen_umol_kg: mean={mean:.2f}, std={std:.2f}, min={minimum:.2f}, max={maximum:.2f}, n={n}")

# --- quick and dirty flag for possible sensor drift -----------------------
# (copy-pasted from a different script last month, not sure this is right)

cleaned = [v for v in temperature_readings if v is not None]
mean = sum(cleaned) / len(cleaned)
for i, v in enumerate(temperature_readings):
    if v is not None and abs(v - mean) > 3 * std:  # bug: this is salinity's std!
        print(f"possible outlier at row {i}: temperature_c={v}")
