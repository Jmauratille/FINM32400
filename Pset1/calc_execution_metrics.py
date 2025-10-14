# calc_execution_metrics.py

"""
Usage: 
    python ~/FINM32400/Pset1/calc_execution_metrics.py --input_csv_file ~/FINM32400/Pset1/fills.csv --output_metrics_file ~/FINM32400/Pset1/metrics.csv
"""

import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser(description="Compute per-exchange metrics.")
    ap.add_argument("--input_csv_file", required=True)
    ap.add_argument("--output_metrics_file", required=True)
    args = ap.parse_args()

    # Reading CSV
    df = pd.read_csv(args.input_csv_file)

    # Execution speeds
    df["OrderTransactTime"] = pd.to_datetime(df["OrderTransactTime"])
    df["ExecutionTransactTime"] = pd.to_datetime(df["ExecutionTransactTime"])
    df["ExecSpeedSecs"] = (df["ExecutionTransactTime"] - df["OrderTransactTime"]).dt.total_seconds()

    # Metrics
    df["LimitPrice"] = df["LimitPrice"].astype(float)
    df["AvgPx"] = df["AvgPx"].astype(float)
    df["Side"] = df["Side"].astype(int)

    # Price improvement by long/short position
    buy_impr  = (df["LimitPrice"] - df["AvgPx"]).clip(lower=0)
    sell_impr = (df["AvgPx"] - df["LimitPrice"]).clip(lower=0) 

    df["PriceImprovement"] = 0.0
    df.loc[df["Side"] == 1, "PriceImprovement"] = buy_impr
    df.loc[df["Side"] == 2, "PriceImprovement"] = sell_impr

    # Per-exchange avgs
    output = (
        df.groupby("LastMkt", as_index=False)
          .agg(
              AvgPriceImprovement=("PriceImprovement", "mean"),
              AvgExecSpeedSecs=("ExecSpeedSecs", "mean"),
          )
    )

    # Output
    output.to_csv(args.output_metrics_file, index=False)

if __name__ == "__main__":
    main()
