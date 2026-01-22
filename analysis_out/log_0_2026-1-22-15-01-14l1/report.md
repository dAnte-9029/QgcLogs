# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_0_2026-1-22-15-01-14l1 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_0_2026-1-22-15-01-14l1_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_0_2026-1-22-15-01-14l1_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_0_2026-1-22-15-01-14l1_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_0_2026-1-22-15-01-14l1_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_0_2026-1-22-15-01-14l1_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_0_2026-1-22-15-01-14l1_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_0_2026-1-22-15-01-14l1_actuator_outputs_0.csv, log_0_2026-1-22-15-01-14l1_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_0_2026-1-22-15-01-14l1_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_0_2026-1-22-15-01-14l1_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_0_2026-1-22-15-01-14l1_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_0_2026-1-22-15-01-14l1_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_0_2026-1-22-15-01-14l1_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_0_2026-1-22-15-01-14l1_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_0_2026-1-22-15-01-14l1`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 444.230
- nav_state_changes: 4
- arming_state_changes: 0
- nav_state_unique: [0, 3, 15]
- arming_state_unique: [2]
- nav_state_transitions:
  - t=152.198s: {'nav_state': 15}
  - t=188.660s: {'nav_state': 3}
  - t=273.533s: {'nav_state': 15}
  - t=324.247s: {'nav_state': 0}
- arming_state_transitions:
- gps_summary: {'fix_type': {'mean': '4', 'std': '0', 'min': '4', 'p5': '4', 'p50': '4', 'p95': '4', 'max': '4'}, 'eph': {'mean': '0.317', 'std': '0.118', 'min': '0.163', 'p5': '0.166', 'p50': '0.341', 'p95': '0.498', 'max': '0.535'}, 'epv': {'mean': '0.503', 'std': '0.167', 'min': '0.257', 'p5': '0.276', 'p50': '0.532', 'p95': '0.759', 'max': '0.803'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s

## 4) Flap Frequency

- count: 5823
- mean_hz: 1.6171169643639558
- std_hz: 1.4524508081608503
- min_hz: -1.6945323
- p5_hz: -0.0016765404
- p50_hz: 1.8475848
- p95_hz: 3.6378284400000003
- max_hz: 4.2172675
- anomaly detection rules:
  - gap_threshold_s: 1.0000000000002274
  - step_threshold_hz: 1.2580233750000003
  - dt_median_s: 0.05000000000001137
  - abs_dfreq_median_hz: 0.12580233750000003

Detected step events (|Δf| > step_threshold_hz):
- t=164.038s, Δf=-1.49 Hz
- t=164.888s, Δf=-1.52 Hz
- t=164.938s, Δf=1.33 Hz
- t=165.188s, Δf=1.35 Hz
- t=165.588s, Δf=-1.89 Hz
- t=165.688s, Δf=2.4 Hz
- t=166.388s, Δf=-1.51 Hz
- t=166.488s, Δf=-2.96 Hz
- t=166.638s, Δf=1.86 Hz
- t=167.538s, Δf=-1.76 Hz
- t=167.588s, Δf=1.82 Hz
- t=167.688s, Δf=-1.71 Hz
- t=167.788s, Δf=1.39 Hz
- t=167.938s, Δf=-1.4 Hz
- t=168.118s, Δf=-2 Hz
- t=168.438s, Δf=1.41 Hz
- t=168.688s, Δf=-1.7 Hz
- t=168.738s, Δf=1.59 Hz
- t=168.938s, Δf=-2.95 Hz
- t=169.088s, Δf=1.45 Hz
- t=169.178s, Δf=-1.71 Hz
- t=169.338s, Δf=1.58 Hz
- t=169.388s, Δf=-1.37 Hz
- t=169.738s, Δf=-2.07 Hz
- t=169.788s, Δf=1.55 Hz
- t=169.988s, Δf=-3.84 Hz
- t=170.038s, Δf=2.61 Hz
- t=170.388s, Δf=2.35 Hz
- t=170.538s, Δf=-1.36 Hz
- t=170.788s, Δf=-1.78 Hz
- t=170.838s, Δf=1.3 Hz
- t=171.038s, Δf=-1.95 Hz
- t=171.278s, Δf=-1.75 Hz
- t=171.338s, Δf=1.69 Hz
- t=171.388s, Δf=-1.95 Hz
- t=171.438s, Δf=2.32 Hz
- t=171.738s, Δf=-1.7 Hz
- t=171.838s, Δf=-2.21 Hz
- t=171.888s, Δf=2.14 Hz
- t=172.088s, Δf=-1.47 Hz
- t=172.438s, Δf=1.83 Hz
- t=172.888s, Δf=-1.86 Hz
- t=173.238s, Δf=-3.1 Hz
- t=173.388s, Δf=1.75 Hz
- t=173.428s, Δf=-1.32 Hz
- t=174.338s, Δf=-1.58 Hz
- t=174.358s, Δf=-2.29 Hz
- t=174.638s, Δf=1.73 Hz
- t=174.838s, Δf=-3.07 Hz
- t=174.888s, Δf=3.31 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | -0.0736 | 5823 |
| freq_vs_pitch_deg | 0.6802 | 5823 |
| freq_vs_abs(p) | 0.5285 | 5823 |
| freq_vs_abs(q) | 0.3475 | 5823 |
| freq_vs_abs(r) | 0.2830 | 5823 |
| freq_vs_manual_roll | 0.0586 | 2834 |
| freq_vs_output[0] | -0.4308 | 5818 |
| freq_vs_output[1] | -0.4503 | 5818 |
| freq_vs_output[2] | 0.9445 | 5818 |
| freq_vs_output[3] | nan | 5818 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.1553 |  |  |
| manual.roll.max_abs | 1 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0.008202 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.2e+03] |  | top=0.00239, bottom=0.0735 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.15e+03] |  | top=0.000342, bottom=0.00991 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.86e+03] |  | top=0.163, bottom=0.389 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.000342, bottom=1 (±1% range rule) |
| actuator_outputs.output[4].range | [800, 1.57e+03] |  | top=0.00103, bottom=0.00205 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.000342, bottom=1 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.000342, bottom=1 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.000342, bottom=1 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
