#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, NamedTuple

import numpy as np
import pandas as pd


def _require_matplotlib():
    import matplotlib.pyplot as plt  # noqa: F401

    return plt


class TopicMatch(NamedTuple):
    path: Path
    score: int


@dataclass
class TopicData:
    logical_name: str
    candidates: list[str]
    matched_files: list[Path]
    df: pd.DataFrame | None = None
    timestamp_col: str | None = None
    time_scale: float | None = None  # divide timestamp by this to get seconds
    notes: list[str] | None = None
    key_fields: list[str] | None = None

    def add_note(self, note: str) -> None:
        if self.notes is None:
            self.notes = []
        self.notes.append(note)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a single PX4 flight exported as per-topic CSVs (ulog2csv output)."
    )
    parser.add_argument("--logdir", required=True, help="CSV subdirectory for a single flight.")
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory (default: ./analysis_out/<log_name>/).",
    )
    parser.add_argument(
        "--start",
        type=float,
        default=None,
        help="Optional analysis window start (seconds since t=0, or raw timestamp).",
    )
    parser.add_argument(
        "--end",
        type=float,
        default=None,
        help="Optional analysis window end (seconds since t=0, or raw timestamp).",
    )
    parser.add_argument("--plots", action="store_true", help="Generate plots (PNG).")
    parser.add_argument("--report", action="store_true", help="Generate Markdown report (report.md).")
    return parser.parse_args(argv)


def list_csv_files(logdir: Path) -> list[Path]:
    return sorted([p for p in logdir.glob("*.csv") if p.is_file()])


def _score_match(filename_lower: str, token_lower: str) -> int:
    if token_lower not in filename_lower:
        return 0
    score = len(token_lower)
    if f"_{token_lower}_" in filename_lower:
        score += 50
    # Strong preference: exact topic token before the instance id suffix "_<n>.csv"
    if re.search(rf"_{re.escape(token_lower)}_\d+\.csv$", filename_lower):
        score += 200
    if filename_lower.endswith(f"_{token_lower}.csv"):
        score += 30
    return score


def find_topic_files(logdir: Path, candidates: list[str]) -> list[Path]:
    files = list_csv_files(logdir)
    matches: dict[Path, int] = {}
    for f in files:
        name = f.name.lower()
        best = 0
        for cand in candidates:
            best = max(best, _score_match(name, cand.lower()))
        if best > 0:
            matches[f] = best
    if not matches:
        return []
    max_score = max(matches.values())
    best_matches = [TopicMatch(p, s) for p, s in matches.items() if s == max_score]
    return [m.path for m in sorted(best_matches, key=lambda x: x.path.name)]


def detect_timestamp_column(columns: Iterable[str]) -> str | None:
    cols = list(columns)
    if "timestamp" in cols:
        return "timestamp"
    # Common alternatives
    for cand in ("time", "t", "timestamp_sample", "nav_state_timestamp", "armed_time", "takeoff_time"):
        if cand in cols:
            return cand
    # Fuzzy: first col containing 'timestamp'
    for c in cols:
        if "timestamp" in c:
            return c
    return None


def infer_time_scale(timestamp_values: pd.Series) -> float:
    ts = pd.to_numeric(timestamp_values, errors="coerce").to_numpy(dtype=float)
    ts = ts[np.isfinite(ts)]
    if ts.size < 5:
        return 1e6 if np.nanmax(ts) > 1e6 else 1.0

    ts_sorted = np.sort(ts)
    diffs = np.diff(ts_sorted)
    diffs = diffs[np.isfinite(diffs) & (diffs > 0)]
    dt_med = float(np.nanmedian(diffs)) if diffs.size else 0.0

    # Heuristic for ULog exports:
    # - microseconds: dt ~ 1e3..1e5
    # - nanoseconds: dt ~ 1e6..1e8
    # - seconds: dt < 1
    if dt_med >= 1e6:
        return 1e9
    if dt_med >= 10:
        return 1e6
    return 1.0


def load_topic_csv(topic: TopicData) -> TopicData:
    if not topic.matched_files:
        topic.add_note("CSV file not found.")
        return topic

    frames: list[pd.DataFrame] = []
    ts_col: str | None = None
    for path in topic.matched_files:
        try:
            df = pd.read_csv(path)
        except Exception as e:  # noqa: BLE001
            topic.add_note(f"Failed to read {path.name}: {e}")
            continue

        found_ts = detect_timestamp_column(df.columns)
        if not found_ts:
            topic.add_note(f"{path.name}: no timestamp column found; skipping.")
            continue

        if ts_col is None:
            ts_col = found_ts
        elif ts_col != found_ts:
            topic.add_note(
                f"{path.name}: timestamp column '{found_ts}' differs from '{ts_col}'; using '{ts_col}'."
            )
            if ts_col not in df.columns:
                topic.add_note(f"{path.name}: missing '{ts_col}' column; skipping.")
                continue

        df = df.copy()
        df["_source_file"] = path.name
        df[ts_col] = pd.to_numeric(df[ts_col], errors="coerce")
        df = df.dropna(subset=[ts_col])
        frames.append(df)

    if not frames or ts_col is None:
        topic.add_note("No readable CSV data.")
        return topic

    df_all = pd.concat(frames, ignore_index=True)
    df_all = df_all.sort_values(ts_col, kind="mergesort")
    df_all = df_all.drop_duplicates(subset=[ts_col], keep="first")

    topic.df = df_all
    topic.timestamp_col = ts_col
    topic.time_scale = infer_time_scale(df_all[ts_col])
    topic.key_fields = [c for c in df_all.columns if c not in (ts_col, "_source_file")][:20]
    return topic


def normalize_timebase(topics: list[TopicData]) -> float | None:
    t0_abs_sec: float | None = None
    for t in topics:
        if t.df is None or t.timestamp_col is None or t.time_scale is None:
            continue
        t.df = t.df.copy()
        t.df["_t_abs_sec"] = t.df[t.timestamp_col].astype(float) / float(t.time_scale)
        vmin = float(np.nanmin(t.df["_t_abs_sec"].to_numpy(dtype=float)))
        if math.isfinite(vmin):
            t0_abs_sec = vmin if t0_abs_sec is None else min(t0_abs_sec, vmin)

    if t0_abs_sec is None:
        return None

    for t in topics:
        if t.df is None:
            continue
        if "_t_abs_sec" not in t.df.columns:
            continue
        t.df["t"] = t.df["_t_abs_sec"] - t0_abs_sec
    return t0_abs_sec


def _parse_time_window_arg(value: float | None, t0_abs_sec: float | None) -> float | None:
    if value is None:
        return None
    # If user passed a large number, treat as raw timestamp (assume microseconds, as in ULog).
    if value > 1e6:
        if t0_abs_sec is None:
            return None
        return (value / 1e6) - t0_abs_sec
    return float(value)


def apply_time_window(df: pd.DataFrame, t_start: float | None, t_end: float | None) -> pd.DataFrame:
    if "t" not in df.columns:
        return df
    out = df
    if t_start is not None:
        out = out[out["t"] >= t_start]
    if t_end is not None:
        out = out[out["t"] <= t_end]
    return out


def align_by_timestamp(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    tolerance_s: float = 0.05,
    suffix: str = "_r",
) -> pd.DataFrame:
    if left.empty or right.empty:
        return left.copy()
    if "t" not in left.columns or "t" not in right.columns:
        return left.copy()
    left_sorted = left.sort_values("t", kind="mergesort")
    right_sorted = right.sort_values("t", kind="mergesort")
    return pd.merge_asof(
        left_sorted,
        right_sorted,
        on="t",
        direction="nearest",
        tolerance=tolerance_s,
        suffixes=("", suffix),
    )


def compute_stats(series: pd.Series) -> dict[str, float]:
    s = pd.to_numeric(series, errors="coerce")
    s = s[np.isfinite(s)]
    if s.empty:
        return {
            "count": 0.0,
            "mean": float("nan"),
            "std": float("nan"),
            "min": float("nan"),
            "p5": float("nan"),
            "p50": float("nan"),
            "p95": float("nan"),
            "max": float("nan"),
        }
    q = s.quantile([0.05, 0.5, 0.95]).to_dict()
    return {
        "count": float(s.shape[0]),
        "mean": float(s.mean()),
        "std": float(s.std(ddof=0)),
        "min": float(s.min()),
        "p5": float(q.get(0.05, float("nan"))),
        "p50": float(q.get(0.5, float("nan"))),
        "p95": float(q.get(0.95, float("nan"))),
        "max": float(s.max()),
    }


def _find_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def _find_frequency_column(df: pd.DataFrame) -> str | None:
    preferred = ["frequency_hz", "frequency", "flap_frequency", "flap_frequency_hz", "freq_hz", "freq"]
    col = _find_first_existing_column(df, preferred)
    if col:
        return col
    # Fuzzy fallback
    freq_cols = [c for c in df.columns if c != "timestamp" and "freq" in c.lower()]
    return freq_cols[0] if freq_cols else None


def quat_to_euler_rpy_deg(q0: np.ndarray, q1: np.ndarray, q2: np.ndarray, q3: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Quaternion (w,x,y,z) -> roll/pitch/yaw
    w, x, y, z = q0, q1, q2, q3
    t0 = 2.0 * (w * x + y * z)
    t1 = 1.0 - 2.0 * (x * x + y * y)
    roll = np.arctan2(t0, t1)

    t2 = 2.0 * (w * y - z * x)
    t2 = np.clip(t2, -1.0, 1.0)
    pitch = np.arcsin(t2)

    t3 = 2.0 * (w * z + x * y)
    t4 = 1.0 - 2.0 * (y * y + z * z)
    yaw = np.arctan2(t3, t4)

    return np.degrees(roll), np.degrees(pitch), np.degrees(yaw)


def extract_attitude_deg(df_att: pd.DataFrame, topic: TopicData) -> pd.DataFrame:
    if df_att.empty:
        return df_att
    if all(c in df_att.columns for c in ("roll", "pitch", "yaw")):
        out = df_att.copy()
        out["roll_deg"] = np.degrees(pd.to_numeric(out["roll"], errors="coerce"))
        out["pitch_deg"] = np.degrees(pd.to_numeric(out["pitch"], errors="coerce"))
        out["yaw_deg"] = np.degrees(pd.to_numeric(out["yaw"], errors="coerce"))
        return out

    q_cols = ["q[0]", "q[1]", "q[2]", "q[3]"]
    if all(c in df_att.columns for c in q_cols):
        out = df_att.copy()
        q0 = pd.to_numeric(out["q[0]"], errors="coerce").to_numpy(dtype=float)
        q1 = pd.to_numeric(out["q[1]"], errors="coerce").to_numpy(dtype=float)
        q2 = pd.to_numeric(out["q[2]"], errors="coerce").to_numpy(dtype=float)
        q3 = pd.to_numeric(out["q[3]"], errors="coerce").to_numpy(dtype=float)
        roll, pitch, yaw = quat_to_euler_rpy_deg(q0, q1, q2, q3)
        out["roll_deg"] = roll
        out["pitch_deg"] = pitch
        out["yaw_deg"] = yaw
        topic.add_note("Computed roll/pitch/yaw from quaternion q[0..3].")
        return out

    topic.add_note("Attitude angles unavailable (missing roll/pitch/yaw and q[0..3]).")
    return df_att


def extract_body_rates(df_rates: pd.DataFrame, topic: TopicData) -> pd.DataFrame:
    if df_rates.empty:
        return df_rates
    out = df_rates.copy()
    if all(c in out.columns for c in ("rollspeed", "pitchspeed", "yawspeed")):
        out["p"] = pd.to_numeric(out["rollspeed"], errors="coerce")
        out["q"] = pd.to_numeric(out["pitchspeed"], errors="coerce")
        out["r"] = pd.to_numeric(out["yawspeed"], errors="coerce")
        return out
    if all(c in out.columns for c in ("xyz[0]", "xyz[1]", "xyz[2]")):
        out["p"] = pd.to_numeric(out["xyz[0]"], errors="coerce")
        out["q"] = pd.to_numeric(out["xyz[1]"], errors="coerce")
        out["r"] = pd.to_numeric(out["xyz[2]"], errors="coerce")
        return out
    topic.add_note("Body rates unavailable (missing rollspeed/pitchspeed/yawspeed or xyz[0..2]).")
    return out


class FlapAnomalies(NamedTuple):
    step_events: list[tuple[float, float]]  # (t, delta_hz)
    gaps: list[tuple[float, float, float]]  # (t_start, t_end, gap_s)
    rules: dict[str, float]


def detect_flap_frequency_anomalies(df: pd.DataFrame, freq_col: str) -> FlapAnomalies:
    if df.empty or "t" not in df.columns or freq_col not in df.columns:
        return FlapAnomalies([], [], rules={})

    t = pd.to_numeric(df["t"], errors="coerce").to_numpy(dtype=float)
    f = pd.to_numeric(df[freq_col], errors="coerce").to_numpy(dtype=float)
    ok = np.isfinite(t) & np.isfinite(f)
    t = t[ok]
    f = f[ok]
    if t.size < 5:
        return FlapAnomalies([], [], rules={})

    order = np.argsort(t)
    t = t[order]
    f = f[order]
    dt = np.diff(t)
    dfreq = np.diff(f)

    dt_med = float(np.nanmedian(dt[dt > 0])) if np.any(dt > 0) else float("nan")
    gap_threshold_s = max(1.0, 20.0 * dt_med) if math.isfinite(dt_med) else 1.0

    dfreq_abs_med = float(np.nanmedian(np.abs(dfreq[np.isfinite(dfreq)]))) if dfreq.size else 0.0
    step_threshold_hz = max(1.0, 10.0 * dfreq_abs_med)

    gaps: list[tuple[float, float, float]] = []
    if dt.size:
        gap_idx = np.where(dt > gap_threshold_s)[0]
        for i in gap_idx:
            gaps.append((float(t[i]), float(t[i + 1]), float(dt[i])))

    step_events: list[tuple[float, float]] = []
    if dfreq.size:
        step_idx = np.where(np.abs(dfreq) > step_threshold_hz)[0]
        for i in step_idx:
            step_events.append((float(t[i + 1]), float(dfreq[i])))

    return FlapAnomalies(
        step_events=step_events,
        gaps=gaps,
        rules={
            "gap_threshold_s": float(gap_threshold_s),
            "step_threshold_hz": float(step_threshold_hz),
            "dt_median_s": float(dt_med) if math.isfinite(dt_med) else float("nan"),
            "abs_dfreq_median_hz": float(dfreq_abs_med),
        },
    )


def _downsample_for_plot(df: pd.DataFrame, max_points: int = 8000) -> pd.DataFrame:
    if df.shape[0] <= max_points:
        return df
    step = int(math.ceil(df.shape[0] / max_points))
    return df.iloc[::step, :].copy()


def plot_flap_frequency(
    df_freq: pd.DataFrame,
    freq_col: str,
    anomalies: FlapAnomalies,
    out_path: Path,
) -> None:
    plt = _require_matplotlib()
    fig, ax = plt.subplots(figsize=(10, 4))
    dfp = _downsample_for_plot(df_freq)
    ax.plot(dfp["t"], dfp[freq_col], label=freq_col)
    for i, (t_evt, d_evt) in enumerate(anomalies.step_events):
        ax.axvline(t_evt, label=(f"step event(s): {len(anomalies.step_events)}" if i == 0 else None))
    for i, (t0, t1, gap_s) in enumerate(anomalies.gaps):
        ax.axvspan(t0, t1, alpha=0.2, label=(f"gap(s): {len(anomalies.gaps)}" if i == 0 else None))
    ax.set_title("Flap Frequency vs Time")
    ax.set_xlabel("t (s, relative)")
    ax.set_ylabel("frequency (Hz)")
    ax.legend(loc="best", fontsize="small", ncol=2)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_attitude_vs_flapfreq(
    df_att: pd.DataFrame,
    df_freq: pd.DataFrame,
    freq_col: str,
    out_path: Path,
) -> None:
    plt = _require_matplotlib()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(df_att["t"], df_att["roll_deg"], label="roll (deg)")
    ax1.plot(df_att["t"], df_att["pitch_deg"], label="pitch (deg)")
    ax1.plot(df_att["t"], df_att["yaw_deg"], label="yaw (deg)")
    ax1.set_title("Attitude vs Flap Frequency")
    ax1.set_ylabel("angle (deg)")
    ax1.legend(loc="best", fontsize="small", ncol=3)

    ax2.plot(df_freq["t"], df_freq[freq_col], label="flap frequency (Hz)")
    ax2.set_xlabel("t (s, relative)")
    ax2.set_ylabel("frequency (Hz)")
    ax2.legend(loc="best", fontsize="small")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_rates_vs_flapfreq(
    df_rates: pd.DataFrame,
    df_freq: pd.DataFrame,
    freq_col: str,
    out_path: Path,
) -> None:
    plt = _require_matplotlib()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(df_rates["t"], df_rates["p"], label="p (rad/s)")
    ax1.plot(df_rates["t"], df_rates["q"], label="q (rad/s)")
    ax1.plot(df_rates["t"], df_rates["r"], label="r (rad/s)")
    ax1.set_title("Body Rates vs Flap Frequency")
    ax1.set_ylabel("rate (rad/s)")
    ax1.legend(loc="best", fontsize="small", ncol=3)

    ax2.plot(df_freq["t"], df_freq[freq_col], label="flap frequency (Hz)")
    ax2.set_xlabel("t (s, relative)")
    ax2.set_ylabel("frequency (Hz)")
    ax2.legend(loc="best", fontsize="small")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_manual_vs_outputs(
    df_manual: pd.DataFrame,
    df_outputs: pd.DataFrame,
    output_cols: list[str],
    out_path: Path,
) -> None:
    plt = _require_matplotlib()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(df_manual["t"], df_manual["roll"], label="manual roll (normalized)")
    ax1.set_title("Manual Input vs Actuator Outputs")
    ax1.set_ylabel("manual roll")
    ax1.legend(loc="best", fontsize="small")

    dfp = _downsample_for_plot(df_outputs)
    for c in output_cols:
        ax2.plot(dfp["t"], dfp[c], label=c)
    ax2.set_xlabel("t (s, relative)")
    ax2.set_ylabel("output")
    ax2.legend(loc="best", fontsize="small", ncol=2)

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_mode_timeline(df_status: pd.DataFrame, out_path: Path) -> None:
    plt = _require_matplotlib()
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.step(df_status["t"], df_status["nav_state"], where="post", label="nav_state")
    ax.step(df_status["t"], df_status["arming_state"], where="post", label="arming_state")
    ax.set_title("Mode / Arming Timeline (numeric)")
    ax.set_xlabel("t (s, relative)")
    ax.set_ylabel("state (enum)")
    ax.legend(loc="best", fontsize="small")
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_position_xy(
    df_pos: pd.DataFrame,
    x_col: str,
    y_col: str,
    out_path: Path,
    *,
    units: str,
    title_suffix: str,
) -> None:
    plt = _require_matplotlib()
    dfp = _downsample_for_plot(df_pos[["t", x_col, y_col]].copy())
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=False)

    ax1.plot(dfp["t"], dfp[x_col], label=f"{x_col} ({units})")
    ax1.plot(dfp["t"], dfp[y_col], label=f"{y_col} ({units})")
    ax1.set_title(f"Horizontal Position vs Time ({title_suffix})")
    ax1.set_xlabel("t (s, relative)")
    ax1.set_ylabel(f"position ({units})")
    ax1.legend(loc="best", fontsize="small", ncol=2)

    ax2.plot(dfp[x_col], dfp[y_col], label="trajectory")
    ax2.set_title(f"Horizontal Trajectory ({title_suffix})")
    ax2.set_xlabel(f"{x_col} ({units})")
    ax2.set_ylabel(f"{y_col} ({units})")
    ax2.legend(loc="best", fontsize="small")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_baro_altitude(
    df_air: pd.DataFrame,
    alt_col: str,
    out_path: Path,
) -> None:
    plt = _require_matplotlib()
    dfp = _downsample_for_plot(df_air[["t", alt_col]].copy())
    alt0 = float(pd.to_numeric(dfp[alt_col].iloc[0], errors="coerce"))
    dfp["alt_rel_m"] = pd.to_numeric(dfp[alt_col], errors="coerce") - alt0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(dfp["t"], dfp[alt_col], label=f"{alt_col} (m)")
    ax1.set_title("Barometric Altitude")
    ax1.set_ylabel("altitude (m)")
    ax1.legend(loc="best", fontsize="small")

    ax2.plot(dfp["t"], dfp["alt_rel_m"], label="relative altitude (m)")
    ax2.set_xlabel("t (s, relative)")
    ax2.set_ylabel("Δalt (m)")
    ax2.legend(loc="best", fontsize="small")

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _rms(series: pd.Series) -> float:
    x = pd.to_numeric(series, errors="coerce")
    x = x[np.isfinite(x)]
    if x.empty:
        return float("nan")
    return float(np.sqrt(np.mean(np.square(x.to_numpy(dtype=float)))))


def pearson_r(x: pd.Series, y: pd.Series) -> float:
    xs = pd.to_numeric(x, errors="coerce")
    ys = pd.to_numeric(y, errors="coerce")
    ok = np.isfinite(xs) & np.isfinite(ys)
    xs = xs[ok].to_numpy(dtype=float)
    ys = ys[ok].to_numpy(dtype=float)
    if xs.size < 3:
        return float("nan")
    if float(np.std(xs)) == 0.0 or float(np.std(ys)) == 0.0:
        return float("nan")
    return float(np.corrcoef(xs, ys)[0, 1])


def write_stats_csv(rows: list[dict[str, object]], out_path: Path) -> None:
    df = pd.DataFrame(rows)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)


def _md_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(str(r.get(h, "")) for h in headers) + " |")
    return "\n".join(out)


def write_report(
    *,
    out_path: Path,
    argv: list[str],
    logdir: Path,
    topics: list[TopicData],
    t_window: tuple[float | None, float | None],
    overview: dict[str, object],
    flap_summary: dict[str, object],
    correlation_rows: list[dict[str, object]],
    control_rows: list[dict[str, object]],
    missing_items: list[str],
) -> None:
    t_start, t_end = t_window
    topic_rows = []
    for t in topics:
        if not t.matched_files:
            continue
        topic_rows.append(
            {
                "logical": t.logical_name,
                "file(s)": ", ".join([p.name for p in t.matched_files[:3]]) + (" ..." if len(t.matched_files) > 3 else ""),
                "timestamp_col": t.timestamp_col or "",
                "key_fields": ", ".join(t.key_fields or []),
            }
        )

    missing_topics = [t.logical_name for t in topics if not t.matched_files]

    lines: list[str] = []
    lines.append("# Flight Analysis Report")
    lines.append("")
    lines.append("## 1) Run Command")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 analyze_flight.py " + " ".join(argv))
    lines.append("```")
    lines.append("")
    lines.append("## 2) Detected Topics")
    lines.append("")
    if topic_rows:
        lines.append(_md_table(topic_rows, ["logical", "file(s)", "timestamp_col", "key_fields"]))
        lines.append("")
    if missing_topics:
        lines.append("Missing topics:")
        for mt in missing_topics:
            lines.append(f"- {mt}")
        lines.append("")

    lines.append("## 3) Flight Overview")
    lines.append("")
    lines.append(f"- logdir: `{logdir}`")
    lines.append(f"- analysis window: start={t_start if t_start is not None else 'auto'} s, end={t_end if t_end is not None else 'auto'} s (relative)")
    for k, v in overview.items():
        if k in ("nav_state_transitions", "arming_state_transitions") and isinstance(v, list):
            lines.append(f"- {k}:")
            for item in v:
                if isinstance(item, dict) and "t_s" in item:
                    rest = {kk: vv for kk, vv in item.items() if kk != "t_s"}
                    lines.append(f"  - t={float(item['t_s']):.3f}s: {rest}")
                else:
                    lines.append(f"  - {item}")
            continue
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## 4) Flap Frequency")
    lines.append("")
    for k, v in flap_summary.items():
        if k in ("anomaly_rules", "anomalies_md"):
            continue
        lines.append(f"- {k}: {v}")
    rules = flap_summary.get("anomaly_rules", {})
    if rules:
        lines.append("- anomaly detection rules:")
        for rk, rv in rules.items():
            lines.append(f"  - {rk}: {rv}")
    anomalies_md = flap_summary.get("anomalies_md", "")
    if anomalies_md:
        lines.append("")
        lines.append(anomalies_md)
    lines.append("")

    lines.append("## 5) Correlations")
    lines.append("")
    if correlation_rows:
        lines.append(_md_table(correlation_rows, ["metric", "pearson_r", "n"]))
        lines.append("")
        lines.append("- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.")
        lines.append("")
    else:
        lines.append("- Not available (missing required topics/fields).")
        lines.append("")

    lines.append("## 6) Control Link Diagnostics")
    lines.append("")
    if control_rows:
        lines.append(_md_table(control_rows, ["metric", "value", "unit", "notes"]))
        lines.append("")
        lines.append("- Conclusions: Based on the above statistics and plots only.")
        lines.append("")
    else:
        lines.append("- Not available (missing required topics/fields).")
        lines.append("")

    lines.append("## 7) Unfinished Items (Missing Topics/Fields)")
    lines.append("")
    if missing_items:
        for item in missing_items:
            lines.append(f"- {item}")
    else:
        lines.append("- None")
    lines.append("")

    # Append topic notes
    notes = []
    for t in topics:
        if t.notes:
            for n in t.notes:
                notes.append(f"- {t.logical_name}: {n}")
    if notes:
        lines.append("## Notes")
        lines.append("")
        lines.extend(notes)
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    logdir = Path(args.logdir).expanduser().resolve()
    if not logdir.exists() or not logdir.is_dir():
        print(f"Error: --logdir does not exist or is not a directory: {logdir}", file=sys.stderr)
        return 2

    log_name = logdir.name
    out_dir = Path(args.out).expanduser().resolve() if args.out else (Path("analysis_out") / log_name).resolve()
    plots_dir = out_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str((out_dir / ".mplconfig").resolve()))

    # Logical topics -> candidate filename tokens
    topics: list[TopicData] = []
    topics.append(TopicData("flap_frequency", ["flap_frequency", "flapfreq", "flap_freq"], find_topic_files(logdir, ["flap_frequency", "flapfreq", "flap_freq"])))
    topics.append(TopicData("manual_control_setpoint", ["manual_control_setpoint"], find_topic_files(logdir, ["manual_control_setpoint"])))
    topics.append(TopicData("vehicle_attitude", ["vehicle_attitude"], find_topic_files(logdir, ["vehicle_attitude"])))
    topics.append(
        TopicData(
            "vehicle_angular_velocity",
            ["vehicle_angular_velocity", "angular_velocity"],
            find_topic_files(logdir, ["vehicle_angular_velocity", "angular_velocity"]),
        )
    )
    topics.append(TopicData("vehicle_attitude_setpoint", ["vehicle_attitude_setpoint"], find_topic_files(logdir, ["vehicle_attitude_setpoint"])))
    topics.append(TopicData("vehicle_rates_setpoint", ["vehicle_rates_setpoint"], find_topic_files(logdir, ["vehicle_rates_setpoint"])))
    topics.append(TopicData("actuator_controls_0", ["actuator_controls_0"], find_topic_files(logdir, ["actuator_controls_0"])))
    topics.append(TopicData("actuator_outputs", ["actuator_outputs"], find_topic_files(logdir, ["actuator_outputs"])))
    topics.append(TopicData("vehicle_local_position", ["vehicle_local_position"], find_topic_files(logdir, ["vehicle_local_position"])))
    topics.append(TopicData("vehicle_global_position", ["vehicle_global_position"], find_topic_files(logdir, ["vehicle_global_position"])))
    topics.append(TopicData("vehicle_status", ["vehicle_status"], find_topic_files(logdir, ["vehicle_status"])))
    topics.append(TopicData("sensor_gps", ["sensor_gps", "vehicle_gps_position", "gps_position"], find_topic_files(logdir, ["sensor_gps", "vehicle_gps_position", "gps_position"])))
    topics.append(TopicData("vehicle_air_data", ["vehicle_air_data"], find_topic_files(logdir, ["vehicle_air_data"])))

    # Load data
    for i, t in enumerate(topics):
        if t.matched_files:
            # Prefer the best match if many (keep all for now, but best first)
            topics[i] = load_topic_csv(t)

    t0_abs_sec = normalize_timebase(topics)
    if t0_abs_sec is None:
        print("Error: could not normalize timebase (no readable topics with timestamps).", file=sys.stderr)
        return 2

    t_start = _parse_time_window_arg(args.start, t0_abs_sec)
    t_end = _parse_time_window_arg(args.end, t0_abs_sec)
    if t_start is not None and t_end is not None and t_end < t_start:
        print("Error: --end must be >= --start (after conversion).", file=sys.stderr)
        return 2

    # Apply window
    for t in topics:
        if t.df is None:
            continue
        t.df = apply_time_window(t.df, t_start, t_end)

    # Overview duration (based on union of available topics)
    tmins: list[float] = []
    tmaxs: list[float] = []
    for t in topics:
        if t.df is None or t.df.empty or "t" not in t.df.columns:
            continue
        tmins.append(float(t.df["t"].min()))
        tmaxs.append(float(t.df["t"].max()))
    overview: dict[str, object] = {}
    if tmins and tmaxs:
        duration_s = max(tmaxs) - min(tmins)
        overview["duration_s"] = f"{duration_s:.3f}"
    else:
        overview["duration_s"] = "n/a (no usable timestamps)"

    # Mode / arming summary (vehicle_status)
    missing_items: list[str] = []
    t_status = next((t for t in topics if t.logical_name == "vehicle_status"), None)
    df_status = (t_status.df.copy() if t_status and t_status.df is not None else pd.DataFrame())
    if not df_status.empty and all(c in df_status.columns for c in ("nav_state", "arming_state", "t")):
        df_status["nav_state"] = pd.to_numeric(df_status["nav_state"], errors="coerce")
        df_status["arming_state"] = pd.to_numeric(df_status["arming_state"], errors="coerce")
        nav_changes = int((df_status["nav_state"].diff().fillna(0) != 0).sum())
        arm_changes = int((df_status["arming_state"].diff().fillna(0) != 0).sum())
        overview["nav_state_changes"] = nav_changes
        overview["arming_state_changes"] = arm_changes
        overview["nav_state_unique"] = sorted([int(x) for x in pd.unique(df_status["nav_state"].dropna())])[:20]
        overview["arming_state_unique"] = sorted([int(x) for x in pd.unique(df_status["arming_state"].dropna())])[:20]
        # Transition timestamps (compact)
        nav_transitions = df_status.loc[df_status["nav_state"].diff().fillna(0) != 0, ["t", "nav_state"]]
        arm_transitions = df_status.loc[df_status["arming_state"].diff().fillna(0) != 0, ["t", "arming_state"]]
        overview["nav_state_transitions"] = [
            {"t_s": float(r.t), "nav_state": int(r.nav_state)} for r in nav_transitions.itertuples(index=False)
        ][:20]
        overview["arming_state_transitions"] = [
            {"t_s": float(r.t), "arming_state": int(r.arming_state)}
            for r in arm_transitions.itertuples(index=False)
        ][:20]
    else:
        overview["mode_summary"] = "n/a (vehicle_status missing nav_state/arming_state)"
        missing_items.append("Mode/arming analysis requires vehicle_status with nav_state + arming_state.")

    # GPS health (sensor_gps)
    t_gps = next((t for t in topics if t.logical_name == "sensor_gps"), None)
    df_gps = (t_gps.df.copy() if t_gps and t_gps.df is not None else pd.DataFrame())
    gps_summary = {}
    if not df_gps.empty and "t" in df_gps.columns:
        for field in ("fix_type", "eph", "epv"):
            if field in df_gps.columns:
                stats = compute_stats(df_gps[field])
                gps_summary[field] = {k: (f"{v:.3g}" if math.isfinite(v) else "nan") for k, v in stats.items() if k != "count"}
        if gps_summary:
            overview["gps_summary"] = gps_summary
        else:
            overview["gps_summary"] = "n/a (sensor_gps present but missing fix_type/eph/epv)"
            missing_items.append("GPS summary requires sensor_gps with fix_type/eph/epv.")
    else:
        overview["gps_summary"] = "n/a (sensor_gps not found)"
        missing_items.append("GPS summary requires sensor_gps (or equivalent) topic.")

    stats_rows: list[dict[str, object]] = []
    correlation_rows: list[dict[str, object]] = []
    control_rows_md: list[dict[str, object]] = []

    # Position (horizontal) + altitude (baro) plots
    if args.plots:
        pos_source = "n/a"
        t_pos = next((t for t in topics if t.logical_name == "vehicle_local_position"), None)
        df_pos = (t_pos.df.copy() if t_pos and t_pos.df is not None else pd.DataFrame())
        if not df_pos.empty and all(c in df_pos.columns for c in ("t", "x", "y")):
            pos_source = "vehicle_local_position (x,y)"
            df_pos = df_pos.copy()
            df_pos["x"] = pd.to_numeric(df_pos["x"], errors="coerce")
            df_pos["y"] = pd.to_numeric(df_pos["y"], errors="coerce")
            df_pos = df_pos.dropna(subset=["t", "x", "y"])
            if not df_pos.empty:
                plot_position_xy(df_pos, "x", "y", plots_dir / "position_xy.png", units="m", title_suffix="local_position")
            else:
                missing_items.append("position_xy.png requires vehicle_local_position with numeric x/y.")
        else:
            # Fallback: vehicle_global_position -> approximate local meters from lat/lon
            t_gpos = next((t for t in topics if t.logical_name == "vehicle_global_position"), None)
            df_gpos = (t_gpos.df.copy() if t_gpos and t_gpos.df is not None else pd.DataFrame())
            if not df_gpos.empty and all(c in df_gpos.columns for c in ("t", "lat", "lon")):
                pos_source = "vehicle_global_position (lat/lon -> approx meters)"
                g = df_gpos[["t", "lat", "lon"]].copy()
                g["lat"] = pd.to_numeric(g["lat"], errors="coerce")
                g["lon"] = pd.to_numeric(g["lon"], errors="coerce")
                g = g.dropna(subset=["t", "lat", "lon"])
                if not g.empty:
                    lat0 = float(g["lat"].iloc[0])
                    lon0 = float(g["lon"].iloc[0])
                    if abs(lat0) > 180.0 or abs(lon0) > 180.0:
                        g["lat_deg"] = g["lat"] / 1e7
                        g["lon_deg"] = g["lon"] / 1e7
                    else:
                        g["lat_deg"] = g["lat"]
                        g["lon_deg"] = g["lon"]
                    lat0_deg = float(g["lat_deg"].iloc[0])
                    lon0_deg = float(g["lon_deg"].iloc[0])
                    r_earth = 6371000.0
                    lat_rad = np.radians(g["lat_deg"].to_numpy(dtype=float))
                    lon_rad = np.radians(g["lon_deg"].to_numpy(dtype=float))
                    lat0_rad = math.radians(lat0_deg)
                    lon0_rad = math.radians(lon0_deg)
                    g["x_m"] = (lon_rad - lon0_rad) * math.cos(lat0_rad) * r_earth
                    g["y_m"] = (lat_rad - lat0_rad) * r_earth
                    plot_position_xy(g, "x_m", "y_m", plots_dir / "position_xy.png", units="m", title_suffix="global_position")
                else:
                    missing_items.append("position_xy.png requires vehicle_global_position with numeric lat/lon.")
            else:
                missing_items.append("position_xy.png requires vehicle_local_position (x,y) or vehicle_global_position (lat,lon).")

        alt_source = "n/a"
        t_air = next((t for t in topics if t.logical_name == "vehicle_air_data"), None)
        df_air = (t_air.df.copy() if t_air and t_air.df is not None else pd.DataFrame())
        if not df_air.empty and "t" in df_air.columns:
            alt_col = _find_first_existing_column(df_air, ["baro_alt_meter", "baro_altitude", "baro_alt"])
            if alt_col:
                alt_source = f"vehicle_air_data.{alt_col}"
                df_air = df_air.copy()
                df_air[alt_col] = pd.to_numeric(df_air[alt_col], errors="coerce")
                df_air = df_air.dropna(subset=["t", alt_col])
                if not df_air.empty:
                    plot_baro_altitude(df_air, alt_col, plots_dir / "altitude_baro.png")
                else:
                    missing_items.append("altitude_baro.png requires numeric baro altitude data.")
            else:
                missing_items.append("altitude_baro.png requires vehicle_air_data with baro_alt_meter (or similar).")
        else:
            missing_items.append("altitude_baro.png requires vehicle_air_data topic.")

        overview["position_source"] = pos_source
        overview["altitude_source"] = alt_source

    # 2) Flap frequency stats + anomalies + plot
    t_flap = next((t for t in topics if t.logical_name == "flap_frequency"), None)
    flap_summary: dict[str, object] = {}
    df_flap = (t_flap.df.copy() if t_flap and t_flap.df is not None else pd.DataFrame())
    freq_col = _find_frequency_column(df_flap) if not df_flap.empty else None
    anomalies = FlapAnomalies([], [], rules={})

    if df_flap.empty or freq_col is None or "t" not in df_flap.columns:
        flap_summary["status"] = "missing (flap_frequency topic/field not found)"
        missing_items.append("Flap frequency analysis requires flap_frequency CSV with a frequency column.")
    else:
        df_flap = df_flap[["t", freq_col]].copy()
        df_flap = df_flap.dropna()
        df_flap = df_flap.sort_values("t", kind="mergesort")
        flap_stats = compute_stats(df_flap[freq_col])
        flap_summary["count"] = int(flap_stats["count"])
        flap_summary["mean_hz"] = flap_stats["mean"]
        flap_summary["std_hz"] = flap_stats["std"]
        flap_summary["min_hz"] = flap_stats["min"]
        flap_summary["p5_hz"] = flap_stats["p5"]
        flap_summary["p50_hz"] = flap_stats["p50"]
        flap_summary["p95_hz"] = flap_stats["p95"]
        flap_summary["max_hz"] = flap_stats["max"]

        stats_rows.append({"metric": "flap_frequency.mean_hz", "value": flap_stats["mean"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.std_hz", "value": flap_stats["std"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.min_hz", "value": flap_stats["min"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.p5_hz", "value": flap_stats["p5"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.p50_hz", "value": flap_stats["p50"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.p95_hz", "value": flap_stats["p95"], "unit": "Hz", "notes": f"field={freq_col}"})
        stats_rows.append({"metric": "flap_frequency.max_hz", "value": flap_stats["max"], "unit": "Hz", "notes": f"field={freq_col}"})

        anomalies = detect_flap_frequency_anomalies(df_flap, freq_col)
        flap_summary["anomaly_rules"] = anomalies.rules
        anomalies_lines = []
        if anomalies.step_events:
            anomalies_lines.append("Detected step events (|Δf| > step_threshold_hz):")
            for t_evt, d_evt in anomalies.step_events[:50]:
                anomalies_lines.append(f"- t={t_evt:.3f}s, Δf={d_evt:.3g} Hz")
        if anomalies.gaps:
            anomalies_lines.append("Detected gaps (Δt > gap_threshold_s):")
            for t0, t1, gap_s in anomalies.gaps[:50]:
                anomalies_lines.append(f"- t=[{t0:.3f}s, {t1:.3f}s], gap={gap_s:.3f}s")
        flap_summary["anomalies_md"] = "\n".join(anomalies_lines)

        if args.plots:
            plot_flap_frequency(df_flap, freq_col, anomalies, plots_dir / "flap_frequency.png")

    # 3) Attitude/rates vs flapfreq + correlations
    t_att = next((t for t in topics if t.logical_name == "vehicle_attitude"), None)
    df_att = (t_att.df.copy() if t_att and t_att.df is not None else pd.DataFrame())
    if not df_att.empty and "t" in df_att.columns:
        df_att = extract_attitude_deg(df_att, t_att)
        have_angles = all(c in df_att.columns for c in ("roll_deg", "pitch_deg", "yaw_deg"))
        if have_angles and not df_flap.empty and freq_col and "t" in df_flap.columns:
            # Align on flap frequency timestamps for correlation
            base = df_flap.copy()
            base = align_by_timestamp(base, df_att[["t", "roll_deg", "pitch_deg", "yaw_deg"]], tolerance_s=0.05, suffix="_att")
            base = base.dropna(subset=[freq_col, "roll_deg", "pitch_deg", "yaw_deg"])
            if not base.empty:
                for axis in ("roll_deg", "pitch_deg"):
                    r = pearson_r(base[freq_col], base[axis])
                    correlation_rows.append({"metric": f"freq_vs_{axis}", "pearson_r": f"{r:.4f}", "n": int(base.shape[0])})
                    stats_rows.append({"metric": f"corr.freq_vs_{axis}", "value": r, "unit": "", "notes": "pearson"})
            if args.plots:
                plot_attitude_vs_flapfreq(
                    _downsample_for_plot(df_att[["t", "roll_deg", "pitch_deg", "yaw_deg"]]),
                    _downsample_for_plot(df_flap[["t", freq_col]]),
                    freq_col,
                    plots_dir / "attitude_vs_flapfreq.png",
                )
        else:
            missing_items.append("Attitude vs flapfreq requires vehicle_attitude (roll/pitch/yaw or q[0..3]) and flap_frequency.")
    else:
        missing_items.append("Attitude vs flapfreq requires vehicle_attitude topic.")

    t_rates = next((t for t in topics if t.logical_name == "vehicle_angular_velocity"), None)
    df_rates = (t_rates.df.copy() if t_rates and t_rates.df is not None else pd.DataFrame())
    if not df_rates.empty and "t" in df_rates.columns:
        df_rates = extract_body_rates(df_rates, t_rates)
        have_pqr = all(c in df_rates.columns for c in ("p", "q", "r"))
        if have_pqr and not df_flap.empty and freq_col and "t" in df_flap.columns:
            base = df_flap.copy()
            base = align_by_timestamp(base, df_rates[["t", "p", "q", "r"]], tolerance_s=0.05, suffix="_rates")
            base = base.dropna(subset=[freq_col, "p", "q", "r"])
            if not base.empty:
                for axis in ("p", "q", "r"):
                    r_val = pearson_r(base[freq_col], np.abs(base[axis]))
                    correlation_rows.append({"metric": f"freq_vs_abs({axis})", "pearson_r": f"{r_val:.4f}", "n": int(base.shape[0])})
                    stats_rows.append({"metric": f"corr.freq_vs_abs({axis})", "value": r_val, "unit": "", "notes": "pearson"})
            if args.plots:
                plot_rates_vs_flapfreq(
                    _downsample_for_plot(df_rates[["t", "p", "q", "r"]]),
                    _downsample_for_plot(df_flap[["t", freq_col]]),
                    freq_col,
                    plots_dir / "rates_vs_flapfreq.png",
                )
        else:
            missing_items.append("Rates vs flapfreq requires vehicle_angular_velocity and flap_frequency.")
    else:
        missing_items.append("Rates vs flapfreq requires vehicle_angular_velocity topic.")

    # 4) Control link diagnostics
    t_manual = next((t for t in topics if t.logical_name == "manual_control_setpoint"), None)
    df_manual = (t_manual.df.copy() if t_manual and t_manual.df is not None else pd.DataFrame())
    if not df_manual.empty and "t" in df_manual.columns and "roll" in df_manual.columns:
        roll = pd.to_numeric(df_manual["roll"], errors="coerce")
        roll_stats = compute_stats(roll)
        sat_thr = 0.95
        sat_ratio = float((np.abs(roll) >= sat_thr).mean()) if roll.shape[0] else float("nan")
        control_rows_md.append({"metric": "manual.roll.mean", "value": f"{roll_stats['mean']:.4g}", "unit": "", "notes": ""})
        control_rows_md.append({"metric": "manual.roll.max_abs", "value": f"{float(np.nanmax(np.abs(roll))):.4g}", "unit": "", "notes": ""})
        control_rows_md.append({"metric": "manual.roll.sat_ratio(|roll|>=0.95)", "value": f"{sat_ratio:.4g}", "unit": "", "notes": ""})
        stats_rows.append({"metric": "manual.roll.sat_ratio", "value": sat_ratio, "unit": "", "notes": "threshold=0.95"})
        # Correlation with flap frequency (if available)
        if not df_flap.empty and freq_col and "t" in df_flap.columns:
            base = df_flap.copy()
            base = align_by_timestamp(base, df_manual[["t", "roll"]], tolerance_s=0.05, suffix="_manual")
            base = base.dropna(subset=[freq_col, "roll"])
            if not base.empty:
                r_val = pearson_r(base[freq_col], base["roll"])
                correlation_rows.append({"metric": "freq_vs_manual_roll", "pearson_r": f"{r_val:.4f}", "n": int(base.shape[0])})
                stats_rows.append({"metric": "corr.freq_vs_manual_roll", "value": r_val, "unit": "", "notes": "pearson"})
    else:
        missing_items.append("Manual input stats require manual_control_setpoint with roll.")

    t_out = next((t for t in topics if t.logical_name == "actuator_outputs"), None)
    df_out = (t_out.df.copy() if t_out and t_out.df is not None else pd.DataFrame())
    output_cols: list[str] = []
    if not df_out.empty and "t" in df_out.columns:
        # Determine active output columns
        if "noutputs" in df_out.columns:
            nout = int(pd.to_numeric(df_out["noutputs"], errors="coerce").max())
            output_cols = [f"output[{i}]" for i in range(nout) if f"output[{i}]" in df_out.columns]
        else:
            output_cols = [c for c in df_out.columns if c.startswith("output[")]
        # Drop outputs that are constant zero (unused)
        nonzero_cols = []
        for c in output_cols:
            s = pd.to_numeric(df_out[c], errors="coerce")
            if float(np.nanmax(np.abs(s))) > 0:
                nonzero_cols.append(c)
        output_cols = nonzero_cols

        # Pre-align with flap frequency for correlations (if requested)
        aligned_for_corr = pd.DataFrame()
        if not df_flap.empty and freq_col and "t" in df_flap.columns:
            aligned_for_corr = align_by_timestamp(
                df_flap[["t", freq_col]].copy(),
                df_out[["t", *output_cols]].copy(),
                tolerance_s=0.05,
                suffix="_out",
            )

        # Per-channel range and saturation ratio (near min/max within 1% of range)
        for c in output_cols:
            s = pd.to_numeric(df_out[c], errors="coerce")
            s = s[np.isfinite(s)]
            if s.empty:
                continue
            vmin = float(s.min())
            vmax = float(s.max())
            rng = vmax - vmin
            eps = 0.01 * rng if rng > 0 else 0.0
            top_ratio = float((s >= (vmax - eps)).mean()) if s.shape[0] else float("nan")
            bot_ratio = float((s <= (vmin + eps)).mean()) if s.shape[0] else float("nan")
            stats_rows.append({"metric": f"actuator_outputs.{c}.min", "value": vmin, "unit": "", "notes": ""})
            stats_rows.append({"metric": f"actuator_outputs.{c}.max", "value": vmax, "unit": "", "notes": ""})
            stats_rows.append({"metric": f"actuator_outputs.{c}.top_ratio", "value": top_ratio, "unit": "", "notes": ">= max-1%range"})
            stats_rows.append({"metric": f"actuator_outputs.{c}.bottom_ratio", "value": bot_ratio, "unit": "", "notes": "<= min+1%range"})
            # Correlation with flap frequency (if available)
            if not aligned_for_corr.empty and freq_col in aligned_for_corr.columns and c in aligned_for_corr.columns:
                base = aligned_for_corr.dropna(subset=[freq_col, c])
                if not base.empty:
                    r_val = pearson_r(base[freq_col], base[c])
                    stats_rows.append({"metric": f"corr.freq_vs_{c}", "value": r_val, "unit": "", "notes": "pearson"})
                    if c in output_cols[:4]:
                        correlation_rows.append({"metric": f"freq_vs_{c}", "pearson_r": f"{r_val:.4f}", "n": int(base.shape[0])})

        if output_cols:
            # Add a compact summary for the report table
            for c in output_cols[:12]:
                s = pd.to_numeric(df_out[c], errors="coerce")
                s = s[np.isfinite(s)]
                if s.empty:
                    continue
                vmin = float(s.min())
                vmax = float(s.max())
                rng = vmax - vmin
                eps = 0.01 * rng if rng > 0 else 0.0
                top_ratio = float((s >= (vmax - eps)).mean())
                bot_ratio = float((s <= (vmin + eps)).mean())
                control_rows_md.append({"metric": f"actuator_outputs.{c}.range", "value": f"[{vmin:.3g}, {vmax:.3g}]", "unit": "", "notes": f"top={top_ratio:.3g}, bottom={bot_ratio:.3g} (±1% range rule)"})
        else:
            missing_items.append("Actuator outputs present but no non-zero output[*] channels found.")
    else:
        missing_items.append("Actuator output stats require actuator_outputs topic.")

    # Plot manual vs outputs if both exist
    if args.plots and not df_manual.empty and not df_out.empty and "t" in df_manual.columns and "t" in df_out.columns and "roll" in df_manual.columns and output_cols:
        # Use a limited number of channels for readability
        plot_cols = output_cols[:8]
        plot_manual_vs_outputs(
            _downsample_for_plot(df_manual[["t", "roll"]]),
            _downsample_for_plot(df_out[["t", *plot_cols]]),
            plot_cols,
            plots_dir / "manual_vs_outputs.png",
        )
    elif args.plots:
        missing_items.append("manual_vs_outputs.png requires manual_control_setpoint (roll) and actuator_outputs (non-zero output[*]).")

    # Setpoint vs measured error (attitude or rates)
    df_att_sp = pd.DataFrame()
    t_att_sp = next((t for t in topics if t.logical_name == "vehicle_attitude_setpoint"), None)
    if t_att_sp and t_att_sp.df is not None and not t_att_sp.df.empty and "t" in t_att_sp.df.columns:
        df_att_sp = t_att_sp.df.copy()
    df_rates_sp = pd.DataFrame()
    t_rates_sp = next((t for t in topics if t.logical_name == "vehicle_rates_setpoint"), None)
    if t_rates_sp and t_rates_sp.df is not None and not t_rates_sp.df.empty and "t" in t_rates_sp.df.columns:
        df_rates_sp = t_rates_sp.df.copy()

    if not df_att_sp.empty and not df_att.empty:
        # Attitude setpoint: try roll_body/pitch_body/yaw_body, else q_d[0..3]
        df_att_meas = df_att.copy()
        if not all(c in df_att_meas.columns for c in ("roll_deg", "pitch_deg", "yaw_deg")):
            df_att_meas = extract_attitude_deg(df_att_meas, t_att) if t_att else df_att_meas
        sp_roll = _find_first_existing_column(df_att_sp, ["roll_body", "roll", "roll_d"])
        sp_pitch = _find_first_existing_column(df_att_sp, ["pitch_body", "pitch", "pitch_d"])
        sp_yaw = _find_first_existing_column(df_att_sp, ["yaw_body", "yaw", "yaw_d"])
        sp_qd_cols = ["q_d[0]", "q_d[1]", "q_d[2]", "q_d[3]"]

        sp = pd.DataFrame()
        if sp_roll and sp_pitch and sp_yaw:
            sp = df_att_sp[["t", sp_roll, sp_pitch, sp_yaw]].copy()
            sp["roll_deg_sp"] = np.degrees(pd.to_numeric(sp[sp_roll], errors="coerce"))
            sp["pitch_deg_sp"] = np.degrees(pd.to_numeric(sp[sp_pitch], errors="coerce"))
            sp["yaw_deg_sp"] = np.degrees(pd.to_numeric(sp[sp_yaw], errors="coerce"))
        elif all(c in df_att_sp.columns for c in sp_qd_cols):
            sp = df_att_sp[["t", *sp_qd_cols]].copy()
            q0 = pd.to_numeric(sp["q_d[0]"], errors="coerce").to_numpy(dtype=float)
            q1 = pd.to_numeric(sp["q_d[1]"], errors="coerce").to_numpy(dtype=float)
            q2 = pd.to_numeric(sp["q_d[2]"], errors="coerce").to_numpy(dtype=float)
            q3 = pd.to_numeric(sp["q_d[3]"], errors="coerce").to_numpy(dtype=float)
            roll, pitch, yaw = quat_to_euler_rpy_deg(q0, q1, q2, q3)
            sp["roll_deg_sp"] = roll
            sp["pitch_deg_sp"] = pitch
            sp["yaw_deg_sp"] = yaw
            if t_att_sp:
                t_att_sp.add_note("Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].")

        if not sp.empty and all(c in df_att_meas.columns for c in ("roll_deg", "pitch_deg", "yaw_deg")):
            meas = df_att_meas[["t", "roll_deg", "pitch_deg", "yaw_deg"]].copy()
            merged = align_by_timestamp(meas, sp[["t", "roll_deg_sp", "pitch_deg_sp", "yaw_deg_sp"]], tolerance_s=0.05, suffix="_sp")
            merged = merged.dropna()
            if not merged.empty:
                merged["err_roll_deg"] = merged["roll_deg_sp"] - merged["roll_deg"]
                merged["err_pitch_deg"] = merged["pitch_deg_sp"] - merged["pitch_deg"]
                stats_rows.append({"metric": "attitude_error.roll_rms_deg", "value": _rms(merged["err_roll_deg"]), "unit": "deg", "notes": ""})
                stats_rows.append({"metric": "attitude_error.pitch_rms_deg", "value": _rms(merged["err_pitch_deg"]), "unit": "deg", "notes": ""})
                if args.plots:
                    plt = _require_matplotlib()
                    fig, ax = plt.subplots(figsize=(10, 4))
                    dfp = _downsample_for_plot(merged[["t", "err_roll_deg", "err_pitch_deg"]])
                    ax.plot(dfp["t"], dfp["err_roll_deg"], label="roll error (deg)")
                    ax.plot(dfp["t"], dfp["err_pitch_deg"], label="pitch error (deg)")
                    ax.set_title("Attitude Setpoint Error")
                    ax.set_xlabel("t (s, relative)")
                    ax.set_ylabel("error (deg)")
                    ax.legend(loc="best", fontsize="small")
                    fig.tight_layout()
                    fig.savefig(plots_dir / "attitude_error.png", dpi=150)
                    plt.close(fig)
        else:
            missing_items.append("Attitude setpoint error requires vehicle_attitude_setpoint (roll/pitch/yaw or q_d[0..3]) and vehicle_attitude angles.")

    if not df_rates_sp.empty and not df_rates.empty:
        df_rates_meas = df_rates.copy()
        if not all(c in df_rates_meas.columns for c in ("p", "q", "r")):
            df_rates_meas = extract_body_rates(df_rates_meas, t_rates) if t_rates else df_rates_meas
        sp_p = _find_first_existing_column(df_rates_sp, ["roll", "p", "rollspeed"])
        sp_q = _find_first_existing_column(df_rates_sp, ["pitch", "q", "pitchspeed"])
        sp_r = _find_first_existing_column(df_rates_sp, ["yaw", "r", "yawspeed"])
        if sp_p and sp_q and sp_r and all(c in df_rates_meas.columns for c in ("p", "q", "r")):
            sp = df_rates_sp[["t", sp_p, sp_q, sp_r]].copy()
            sp["p_sp"] = pd.to_numeric(sp[sp_p], errors="coerce")
            sp["q_sp"] = pd.to_numeric(sp[sp_q], errors="coerce")
            sp["r_sp"] = pd.to_numeric(sp[sp_r], errors="coerce")
            meas = df_rates_meas[["t", "p", "q", "r"]].copy()
            merged = align_by_timestamp(meas, sp[["t", "p_sp", "q_sp", "r_sp"]], tolerance_s=0.05, suffix="_sp")
            merged = merged.dropna()
            if not merged.empty:
                merged["err_p"] = merged["p_sp"] - merged["p"]
                merged["err_q"] = merged["q_sp"] - merged["q"]
                merged["err_r"] = merged["r_sp"] - merged["r"]
                stats_rows.append({"metric": "rates_error.p_rms", "value": _rms(merged["err_p"]), "unit": "rad/s", "notes": ""})
                stats_rows.append({"metric": "rates_error.q_rms", "value": _rms(merged["err_q"]), "unit": "rad/s", "notes": ""})
                stats_rows.append({"metric": "rates_error.r_rms", "value": _rms(merged["err_r"]), "unit": "rad/s", "notes": ""})
                if args.plots:
                    plt = _require_matplotlib()
                    fig, ax = plt.subplots(figsize=(10, 4))
                    dfp = _downsample_for_plot(merged[["t", "err_p", "err_q", "err_r"]])
                    ax.plot(dfp["t"], dfp["err_p"], label="p error (rad/s)")
                    ax.plot(dfp["t"], dfp["err_q"], label="q error (rad/s)")
                    ax.plot(dfp["t"], dfp["err_r"], label="r error (rad/s)")
                    ax.set_title("Rates Setpoint Error")
                    ax.set_xlabel("t (s, relative)")
                    ax.set_ylabel("error (rad/s)")
                    ax.legend(loc="best", fontsize="small", ncol=3)
                    fig.tight_layout()
                    fig.savefig(plots_dir / "rates_error.png", dpi=150)
                    plt.close(fig)
        else:
            missing_items.append("Rates setpoint error requires vehicle_rates_setpoint and vehicle_angular_velocity fields.")

    # Mode timeline plot
    if args.plots and not df_status.empty and all(c in df_status.columns for c in ("t", "nav_state", "arming_state")):
        plot_mode_timeline(df_status[["t", "nav_state", "arming_state"]].copy(), plots_dir / "mode_timeline.png")
    elif args.plots:
        missing_items.append("mode_timeline.png requires vehicle_status with nav_state + arming_state.")

    # Always write stats.csv
    write_stats_csv(stats_rows, out_dir / "stats.csv")

    # Optional report
    if args.report:
        write_report(
            out_path=out_dir / "report.md",
            argv=argv,
            logdir=logdir,
            topics=topics,
            t_window=(t_start, t_end),
            overview=overview,
            flap_summary=flap_summary,
            correlation_rows=correlation_rows,
            control_rows=control_rows_md,
            missing_items=missing_items,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
