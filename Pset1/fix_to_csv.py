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
    we return (prefix_ts, {tag: value, ...})

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

def is_new_order_single(fields):
    """Return True if MsgType (35) is NewOrderSingle (D)."""
    return fields.get("35") == "D"

def is_filled_limit_exec(fields):
    """
    Return True only for filled:
      35=8  (ExecutionReport)
      150=2 (ExecType=FILL)
      39=2  (OrdStatus=FILLED)
      40=2  (OrdType=LIMIT)
    """
    return (
        fields.get("35") == "8"
        and fields.get("150") == "2"
        and fields.get("39") == "2"
        and fields.get("40") == "2"
    )