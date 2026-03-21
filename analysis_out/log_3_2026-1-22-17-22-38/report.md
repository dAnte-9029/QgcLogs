# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_3_2026-1-22-17-22-38 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_3_2026-1-22-17-22-38_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_3_2026-1-22-17-22-38_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_3_2026-1-22-17-22-38_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_3_2026-1-22-17-22-38_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_3_2026-1-22-17-22-38_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_3_2026-1-22-17-22-38_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_3_2026-1-22-17-22-38_actuator_outputs_0.csv, log_3_2026-1-22-17-22-38_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_3_2026-1-22-17-22-38_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_3_2026-1-22-17-22-38_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_3_2026-1-22-17-22-38_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_3_2026-1-22-17-22-38_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_3_2026-1-22-17-22-38_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_3_2026-1-22-17-22-38_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |
| battery_status | log_3_2026-1-22-17-22-38_battery_status_0.csv | timestamp | voltage_v, current_a, current_average_a, discharged_mah, remaining, scale, time_remaining_s, temperature, voltage_cell_v[0], voltage_cell_v[1], voltage_cell_v[2], voltage_cell_v[3], voltage_cell_v[4], voltage_cell_v[5], voltage_cell_v[6], voltage_cell_v[7], voltage_cell_v[8], voltage_cell_v[9], voltage_cell_v[10], voltage_cell_v[11] |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_3_2026-1-22-17-22-38`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 372.106
- nav_state_changes: 5
- arming_state_changes: 0
- nav_state_unique: [0, 3, 4, 15]
- arming_state_unique: [2]
- nav_state_transitions:
  - t=114.022s: {'nav_state': 15}
  - t=222.542s: {'nav_state': 3}
  - t=276.399s: {'nav_state': 4}
  - t=283.299s: {'nav_state': 15}
  - t=323.822s: {'nav_state': 0}
- arming_state_transitions:
- gps_summary: {'fix_type': {'mean': '3.22', 'std': '0.416', 'min': '3', 'p5': '3', 'p50': '3', 'p95': '4', 'max': '4'}, 'eph': {'mean': '0.474', 'std': '0.117', 'min': '0.285', 'p5': '0.306', 'p50': '0.524', 'p95': '0.624', 'max': '0.632'}, 'epv': {'mean': '0.676', 'std': '0.148', 'min': '0.441', 'p5': '0.463', 'p50': '0.751', 'p95': '0.864', 'max': '0.876'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s
- battery_source: battery_status.current_a

## 4) Flap Frequency

- count: 5176
- mean_hz: 2.55465170998628
- std_hz: 1.6588066325772477
- min_hz: -1.9692786
- p5_hz: -1.6806523e-17
- p50_hz: 3.2675376
- p95_hz: 4.205919175
- max_hz: 4.5306015
- anomaly detection rules:
  - gap_threshold_s: 1.0
  - step_threshold_hz: 1.2821049999999978
  - dt_median_s: 0.04999999999999716
  - abs_dfreq_median_hz: 0.12821049999999978

Detected step events (|Δf| > step_threshold_hz):
- t=128.598s, Δf=-1.75 Hz
- t=128.648s, Δf=1.46 Hz
- t=129.048s, Δf=-1.43 Hz
- t=129.298s, Δf=-1.73 Hz
- t=129.348s, Δf=1.55 Hz
- t=129.598s, Δf=-2.38 Hz
- t=129.698s, Δf=1.62 Hz
- t=130.448s, Δf=-1.44 Hz
- t=130.848s, Δf=-2.06 Hz
- t=131.648s, Δf=-1.33 Hz
- t=131.698s, Δf=-1.48 Hz
- t=132.298s, Δf=-2.51 Hz
- t=132.348s, Δf=1.71 Hz
- t=132.598s, Δf=-2.7 Hz
- t=132.618s, Δf=1.51 Hz
- t=132.748s, Δf=1.78 Hz
- t=141.548s, Δf=-2.2 Hz
- t=141.598s, Δf=1.68 Hz
- t=155.148s, Δf=-2.57 Hz
- t=155.398s, Δf=-1.58 Hz
- t=155.448s, Δf=1.37 Hz
- t=155.648s, Δf=-3.05 Hz
- t=155.698s, Δf=2.28 Hz
- t=155.898s, Δf=-1.39 Hz
- t=156.448s, Δf=-1.78 Hz
- t=156.898s, Δf=-3.01 Hz
- t=156.948s, Δf=1.84 Hz
- t=157.847s, Δf=-1.59 Hz
- t=158.398s, Δf=-1.36 Hz
- t=158.498s, Δf=1.82 Hz
- t=158.848s, Δf=-1.99 Hz
- t=158.898s, Δf=1.48 Hz
- t=159.198s, Δf=-2.51 Hz
- t=159.298s, Δf=1.38 Hz
- t=161.398s, Δf=-2.47 Hz
- t=161.448s, Δf=1.75 Hz
- t=161.848s, Δf=-2.41 Hz
- t=161.898s, Δf=1.67 Hz
- t=162.398s, Δf=-1.64 Hz
- t=162.548s, Δf=-2.16 Hz
- t=162.598s, Δf=1.7 Hz
- t=162.998s, Δf=-1.53 Hz
- t=163.098s, Δf=1.64 Hz
- t=166.048s, Δf=-1.44 Hz
- t=166.248s, Δf=-3.23 Hz
- t=166.298s, Δf=1.33 Hz
- t=166.598s, Δf=1.4 Hz
- t=166.748s, Δf=-2.9 Hz
- t=166.848s, Δf=2.33 Hz
- t=167.198s, Δf=-3.83 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | 0.7208 | 5176 |
| freq_vs_pitch_deg | 0.7571 | 5176 |
| freq_vs_abs(p) | 0.4457 | 5176 |
| freq_vs_abs(q) | 0.3208 | 5176 |
| freq_vs_abs(r) | 0.3703 | 5176 |
| freq_vs_manual_roll | 0.0895 | 2542 |
| freq_vs_output[0] | 0.2141 | 5167 |
| freq_vs_output[1] | -0.1193 | 5167 |
| freq_vs_output[2] | 0.9326 | 5167 |
| freq_vs_output[3] | nan | 5167 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.08625 |  |  |
| manual.roll.max_abs | 0.9901 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0.006944 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.2e+03] |  | top=0.0104, bottom=0.143 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.2e+03] |  | top=0.0243, bottom=0.0548 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.91e+03] |  | top=0.174, bottom=0.255 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.000386, bottom=1 (±1% range rule) |
| actuator_outputs.output[4].range | [800, 1.8e+03] |  | top=0.0544, bottom=0.00463 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.000386, bottom=1 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.000386, bottom=1 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.000386, bottom=1 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
