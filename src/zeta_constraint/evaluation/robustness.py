from __future__ import annotations


HARD_BLOCK_MASKS = {
    "k_high": lambda x: x["k"].astype(float) == 7.0,
    "k_low": lambda x: x["k"].astype(float) == 3.0,
    "forcing::condition": lambda x: x["forcing_mode"].astype(str) == "condition_gap",
    "forcing::capacity": lambda x: x["forcing_mode"].astype(str) == "capacity_gap",
    "forcing::feature": lambda x: x["forcing_mode"].astype(str) == "feature_gap",
    "system::entropy": lambda x: x["system"].astype(str) == "entropy",
    "system::unevenness": lambda x: x["system"].astype(str) == "unevenness",
    "flow::linear": lambda x: x["flow_mode"].astype(str) == "linear",
    "flow::nonlinear": lambda x: x["flow_mode"].astype(str) == "nonlinear",
}
