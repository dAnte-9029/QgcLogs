# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_41_2026-1-8-22-52-32 --out analysis_out/test_log41 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_41_2026-1-8-22-52-32_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_41_2026-1-8-22-52-32_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_41_2026-1-8-22-52-32_vehicle_attitude_0.csv, log_41_2026-1-8-22-52-32_vehicle_attitude_setpoint_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter, yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_angular_velocity | log_41_2026-1-8-22-52-32_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_41_2026-1-8-22-52-32_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_41_2026-1-8-22-52-32_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_41_2026-1-8-22-52-32_actuator_outputs_0.csv, log_41_2026-1-8-22-52-32_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_41_2026-1-8-22-52-32_vehicle_local_position_0.csv, log_41_2026-1-8-22-52-32_vehicle_local_position_setpoint_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_status | log_41_2026-1-8-22-52-32_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |

Missing topics:
- actuator_controls_0
- vehicle_global_position
- sensor_gps

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_41_2026-1-8-22-52-32`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 86.443
- nav_state_changes: 1
- arming_state_changes: 1
- nav_state_unique: [0, 15]
- arming_state_unique: [1, 2]
- gps_summary: n/a (sensor_gps not found)

## 4) Flap Frequency

- count: 1320
- mean_hz: 2.4426398597533767
- std_hz: 1.7256464864028072
- min_hz: -0.012809053
- p5_hz: -2.0925956999999972e-07
- p50_hz: 3.52088615
- p95_hz: 4.051588075
- max_hz: 4.1645627
- anomalies_md: Detected step events (|Δf| > step_threshold_hz):
- t=85.509s, Δf=-1.52 Hz
- t=85.559s, Δf=-1 Hz
- anomaly detection rules:
  - gap_threshold_s: 1.0
  - step_threshold_hz: 1.0
  - dt_median_s: 0.04999999999999716
  - abs_dfreq_median_hz: 0.08967440000000027

Detected step events (|Δf| > step_threshold_hz):
- t=85.509s, Δf=-1.52 Hz
- t=85.559s, Δf=-1 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | -0.5194 | 1320 |
| freq_vs_pitch_deg | 0.6995 | 1320 |
| freq_vs_abs(p) | 0.5859 | 1320 |
| freq_vs_abs(q) | 0.1220 | 1320 |
| freq_vs_abs(r) | 0.4640 | 1320 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.005042 |  |  |
| manual.roll.max_abs | 0.9136 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.2e+03] |  | top=0.237, bottom=0.0242 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.2e+03] |  | top=0.0106, bottom=0.00906 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.85e+03] |  | top=0.14, bottom=0.311 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.00151, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[4].range | [0, 1e+03] |  | top=0.00151, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.00151, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.00151, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.00151, bottom=0.998 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- GPS summary requires sensor_gps (or equivalent) topic.
- Attitude setpoint error requires vehicle_attitude_setpoint with roll/pitch/yaw fields and vehicle_attitude angles.

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
