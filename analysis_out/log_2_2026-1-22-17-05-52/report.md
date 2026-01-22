# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_2_2026-1-22-17-05-52 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_2_2026-1-22-17-05-52_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_2_2026-1-22-17-05-52_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_2_2026-1-22-17-05-52_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_2_2026-1-22-17-05-52_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_2_2026-1-22-17-05-52_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_2_2026-1-22-17-05-52_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_2_2026-1-22-17-05-52_actuator_outputs_0.csv, log_2_2026-1-22-17-05-52_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_2_2026-1-22-17-05-52_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_2_2026-1-22-17-05-52_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_2_2026-1-22-17-05-52_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_2_2026-1-22-17-05-52_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_2_2026-1-22-17-05-52_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_2_2026-1-22-17-05-52_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_2_2026-1-22-17-05-52`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 347.807
- nav_state_changes: 11
- arming_state_changes: 1
- nav_state_unique: [0, 3, 15]
- arming_state_unique: [1, 2]
- nav_state_transitions:
  - t=133.685s: {'nav_state': 15}
  - t=133.773s: {'nav_state': 3}
  - t=134.323s: {'nav_state': 15}
  - t=134.389s: {'nav_state': 0}
  - t=135.203s: {'nav_state': 15}
  - t=148.239s: {'nav_state': 3}
  - t=166.262s: {'nav_state': 15}
  - t=226.167s: {'nav_state': 3}
  - t=271.790s: {'nav_state': 15}
  - t=341.903s: {'nav_state': 3}
  - t=343.080s: {'nav_state': 0}
- arming_state_transitions:
  - t=346.810s: {'arming_state': 1}
- gps_summary: {'fix_type': {'mean': '4', 'std': '0', 'min': '4', 'p5': '4', 'p50': '4', 'p95': '4', 'max': '4'}, 'eph': {'mean': '0.342', 'std': '0.0485', 'min': '0.19', 'p5': '0.267', 'p50': '0.349', 'p95': '0.419', 'max': '0.445'}, 'epv': {'mean': '0.493', 'std': '0.0774', 'min': '0.291', 'p5': '0.355', 'p50': '0.509', 'p95': '0.589', 'max': '0.608'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s

## 4) Flap Frequency

- count: 4288
- mean_hz: 3.527401100421493
- std_hz: 1.0491744207822213
- min_hz: -0.012007254
- p5_hz: 0.00015246362100000005
- p50_hz: 3.8975604
- p95_hz: 4.349546409999999
- max_hz: 4.4989076
- anomaly detection rules:
  - gap_threshold_s: 1.0000000000002274
  - step_threshold_hz: 1.2126600000000032
  - dt_median_s: 0.05000000000001137
  - abs_dfreq_median_hz: 0.12126600000000032

Detected step events (|Δf| > step_threshold_hz):
- t=134.008s, Δf=1.38 Hz
- t=134.408s, Δf=-1.76 Hz
- t=343.158s, Δf=-1.91 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | 0.0177 | 4288 |
| freq_vs_pitch_deg | 0.5614 | 4288 |
| freq_vs_abs(p) | 0.3198 | 4288 |
| freq_vs_abs(q) | -0.0106 | 4288 |
| freq_vs_abs(r) | 0.0835 | 4288 |
| freq_vs_manual_roll | 0.1384 | 2138 |
| freq_vs_output[0] | -0.1571 | 4286 |
| freq_vs_output[1] | -0.1233 | 4286 |
| freq_vs_output[2] | 0.9860 | 4286 |
| freq_vs_output[3] | nan | 4286 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.1246 |  |  |
| manual.roll.max_abs | 1 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0.01678 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.2e+03] |  | top=0.014, bottom=0.124 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.2e+03] |  | top=0.00513, bottom=0.0443 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 2e+03] |  | top=0.0531, bottom=0.061 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.000466, bottom=1 (±1% range rule) |
| actuator_outputs.output[4].range | [800, 1.8e+03] |  | top=0.013, bottom=0.0224 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.000466, bottom=1 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.000466, bottom=1 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.000466, bottom=1 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
