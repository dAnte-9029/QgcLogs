# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_1_2026-1-22-16-23-18 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_1_2026-1-22-16-23-18_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_1_2026-1-22-16-23-18_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_1_2026-1-22-16-23-18_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_1_2026-1-22-16-23-18_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_1_2026-1-22-16-23-18_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_1_2026-1-22-16-23-18_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_1_2026-1-22-16-23-18_actuator_outputs_0.csv, log_1_2026-1-22-16-23-18_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_1_2026-1-22-16-23-18_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_1_2026-1-22-16-23-18_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_1_2026-1-22-16-23-18_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_1_2026-1-22-16-23-18_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_1_2026-1-22-16-23-18_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_1_2026-1-22-16-23-18_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |
| battery_status | log_1_2026-1-22-16-23-18_battery_status_0.csv | timestamp | voltage_v, current_a, current_average_a, discharged_mah, remaining, scale, time_remaining_s, temperature, voltage_cell_v[0], voltage_cell_v[1], voltage_cell_v[2], voltage_cell_v[3], voltage_cell_v[4], voltage_cell_v[5], voltage_cell_v[6], voltage_cell_v[7], voltage_cell_v[8], voltage_cell_v[9], voltage_cell_v[10], voltage_cell_v[11] |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_1_2026-1-22-16-23-18`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 265.734
- nav_state_changes: 2
- arming_state_changes: 1
- nav_state_unique: [3, 15]
- arming_state_unique: [1, 2]
- nav_state_transitions:
  - t=53.720s: {'nav_state': 3}
  - t=171.503s: {'nav_state': 15}
- arming_state_transitions:
  - t=264.733s: {'arming_state': 1}
- gps_summary: {'fix_type': {'mean': '3.56', 'std': '0.496', 'min': '3', 'p5': '3', 'p50': '4', 'p95': '4', 'max': '4'}, 'eph': {'mean': '0.421', 'std': '0.143', 'min': '0.2', 'p5': '0.225', 'p50': '0.449', 'p95': '0.577', 'max': '0.721'}, 'epv': {'mean': '0.637', 'std': '0.201', 'min': '0.271', 'p5': '0.329', 'p50': '0.667', 'p95': '0.853', 'max': '1.04'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s
- battery_source: battery_status.current_a

## 4) Flap Frequency

- count: 4784
- mean_hz: 3.0532376466284323
- std_hz: 1.1287881408412743
- min_hz: -1.4667797
- p5_hz: 0.0
- p50_hz: 3.28248345
- p95_hz: 4.10411785
- max_hz: 4.399905
- anomaly detection rules:
  - gap_threshold_s: 1.0000000000000853
  - step_threshold_hz: 1.2837779999999999
  - dt_median_s: 0.05000000000000426
  - abs_dfreq_median_hz: 0.1283778

Detected step events (|Δf| > step_threshold_hz):
- t=36.559s, Δf=-1.74 Hz
- t=37.019s, Δf=-2.06 Hz
- t=37.069s, Δf=1.6 Hz
- t=37.919s, Δf=-1.43 Hz
- t=41.069s, Δf=-1.81 Hz
- t=41.119s, Δf=1.49 Hz
- t=41.219s, Δf=-3.99 Hz
- t=41.269s, Δf=2.58 Hz
- t=253.219s, Δf=-1.63 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | 0.0291 | 4784 |
| freq_vs_pitch_deg | 0.6477 | 4784 |
| freq_vs_abs(p) | 0.3523 | 4784 |
| freq_vs_abs(q) | 0.1928 | 4784 |
| freq_vs_abs(r) | 0.2376 | 4784 |
| freq_vs_manual_roll | 0.0103 | 2343 |
| freq_vs_output[0] | 0.5110 | 4784 |
| freq_vs_output[1] | -0.2881 | 4784 |
| freq_vs_output[2] | 0.9855 | 4784 |
| freq_vs_output[3] | nan | 4784 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.06882 |  |  |
| manual.roll.max_abs | 1 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0.001669 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.2e+03] |  | top=0.0238, bottom=0.0372 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.02e+03] |  | top=0.000418, bottom=0.122 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.93e+03] |  | top=0.000418, bottom=0.0923 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.000418, bottom=1 (±1% range rule) |
| actuator_outputs.output[4].range | [800, 1.56e+03] |  | top=0.000835, bottom=0.0096 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.000418, bottom=1 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.000418, bottom=1 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.000418, bottom=1 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
