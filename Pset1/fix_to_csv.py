#fix_to_csv.py

"""
Usage:
    python ~/FINM32400/Pset1/fix_to_csv.py --input_fix_file /opt/assignment1/trading.fix --output_csv_file ~/FINM32400/Pset1/fills.csv
"""

from __future__ import annotations
import argparse
import csv

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

def main():
    ap = argparse.ArgumentParser(
        description="Parse FIX file to CSV of fills matched to orders."
    )
    ap.add_argument("--input_fix_file", required=True)
    ap.add_argument("--output_csv_file", required=True)
    args = ap.parse_args()

    with open(args.input_fix_file, "r", encoding="utf-8", errors="replace") as infile, \
        open(args.output_csv_file, "w", newline="", encoding="utf-8") as outfile:

        writer = csv.writer(outfile)
        writer.writerow([
            "OrderID","OrderTransactTime","ExecutionTransactTime","Symbol",
            "Side","OrderQty","LimitPrice","AvgPx","LastMkt",
        ])

        # Caching NewOrderSingle by ClOrdID (11)
        orders_by_clordid = {}
        for raw in infile:
            _, fields = parse_fix_line(raw)
            if not fields:
                continue
            if is_new_order_single(fields):
                cl_id = fields.get("11")
                if not cl_id:
                    continue
                orders_by_clordid[cl_id] = {
                    "ClOrdID": cl_id,
                    "TransactTime": fields.get("60",""),
                    "Symbol": fields.get("55",""),
                    "Side": fields.get("54",""),
                    "OrderQty": fields.get("38",""),
                    "LimitPrice": fields.get("44",""),
                }
            elif is_filled_limit_exec(fields):
                cl_id = fields.get("11")
                if not cl_id:
                    continue
                order = orders_by_clordid.get(cl_id)
                if not order:
                    continue
                writer.writerow([
                    order.get("ClOrdID",""),
                    order.get("TransactTime",""),
                    fields.get("60",""),
                    order.get("Symbol",""),
                    order.get("Side",""),
                    order.get("OrderQty",""),
                    order.get("LimitPrice",""),
                    fields.get("6",""),
                    fields.get("30",""),
                ])


if __name__ == "__main__":
    main()
