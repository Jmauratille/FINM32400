#fix_to_csv.py

from __future__ import annotations
import argparse
import csv
import sys

SOH = "\x01"

def parse_fix_line(line):
    """
    Given a line like:
      20250910-00:02:34.713753 : 8=FIX.4.29=33035=834=1962...
    we return (prefix_ts, {tag: value, ...}).

    """
    line = line.rstrip("\n")
    if " :" in line:
        prefix, msg = line.split(" :", 1)
        prefix_ts = prefix.strip()
    else:
        prefix_ts, msg = None, line

    # Splitting on SOH and ignoring empty 
    parts = [p for p in msg.split(SOH) if p]

    fields = {}
    for part in parts:
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        fields[k] = v

    return prefix_ts, fields

sample = "20250910-00:02:34.713753 : 8=FIX.4.29=33035=834=196249=ID152=20250910-04:02:34.71356=ID21=ID66=32.9811=ID314=1017=ID520=030=ID731=32.9832=1037=ID438=1039=240=244=32.9854=255=SMCX59=060=20250910-04:02:34.71376=ID8150=2151=010=235"
ts, f = parse_fix_line(sample)
print("prefix_ts:", ts)
print("tag 35:", f.get("35"))
print("all fields:", f)