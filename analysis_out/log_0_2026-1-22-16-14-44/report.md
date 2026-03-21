# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_0_2026-1-22-16-14-44 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_0_2026-1-22-16-14-44_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_0_2026-1-22-16-14-44_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_0_2026-1-22-16-14-44_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_0_2026-1-22-16-14-44_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_0_2026-1-22-16-14-44_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_0_2026-1-22-16-14-44_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_0_2026-1-22-16-14-44_actuator_outputs_0.csv, log_0_2026-1-22-16-14-44_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_0_2026-1-22-16-14-44_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_0_2026-1-22-16-14-44_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_0_2026-1-22-16-14-44_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_0_2026-1-22-16-14-44_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_0_2026-1-22-16-14-44_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_0_2026-1-22-16-14-44_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |
| battery_status | log_0_2026-1-22-16-14-44_battery_status_0.csv | timestamp | voltage_v, current_a, current_average_a, discharged_mah, remaining, scale, time_remaining_s, temperature, voltage_cell_v[0], voltage_cell_v[1], voltage_cell_v[2], voltage_cell_v[3], voltage_cell_v[4], voltage_cell_v[5], voltage_cell_v[6], voltage_cell_v[7], voltage_cell_v[8], voltage_cell_v[9], voltage_cell_v[10], voltage_cell_v[11] |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_0_2026-1-22-16-14-44`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 112.900
- nav_state_changes: 0
- arming_state_changes: 1
- nav_state_unique: [15]
- arming_state_unique: [1, 2]
- nav_state_transitions:
- arming_state_transitions:
  - t=111.903s: {'arming_state': 1}
- gps_summary: {'fix_type': {'mean': '3', 'std': '0', 'min': '3', 'p5': '3', 'p50': '3', 'p95': '3', 'max': '3'}, 'eph': {'mean': '0.412', 'std': '0.0281', 'min': '0.378', 'p5': '0.379', 'p50': '0.406', 'p95': '0.473', 'max': '0.478'}, 'epv': {'mean': '0.604', 'std': '0.0394', 'min': '0.556', 'p5': '0.557', 'p50': '0.595', 'p95': '0.688', 'max': '0.695'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s
- battery_source: battery_status.current_a

## 4) Flap Frequency

- count: 817
- mean_hz: 0.7837456513640726
- std_hz: 1.3456074368212094
- min_hz: -2.3211496
- p5_hz: -0.05039157439999999
- p50_hz: 0.0005159499
- p95_hz: 3.71118838
- max_hz: 3.9430873
- anomaly detection rules:
  - gap_threshold_s: 1.0
  - step_threshold_hz: 1.0
  - dt_median_s: 0.04999999999999716
  - abs_dfreq_median_hz: 0.01435837375

Detected step events (|Δf| > step_threshold_hz):
- t=79.098s, Δf=1.78 Hz
- t=79.148s, Δf=-1.13 Hz
- t=79.188s, Δf=-1.31 Hz
- t=90.998s, Δf=1.72 Hz
- t=91.048s, Δf=-1.15 Hz
- t=95.147s, Δf=1.1 Hz
- t=95.397s, Δf=-1.06 Hz
- t=95.748s, Δf=-2.25 Hz
- t=95.798s, Δf=1.37 Hz
- t=96.698s, Δf=1.14 Hz
- t=96.898s, Δf=1.41 Hz
- t=97.418s, Δf=-1.35 Hz
- t=98.047s, Δf=-2.5 Hz
- t=98.098s, Δf=2.56 Hz
- t=98.148s, Δf=1.44 Hz
- t=98.297s, Δf=-1.09 Hz
- t=98.698s, Δf=-1.5 Hz
- t=98.838s, Δf=-1.63 Hz
- t=99.198s, Δf=-1.4 Hz
- t=99.248s, Δf=1.06 Hz
- t=99.298s, Δf=-1.03 Hz
- t=99.548s, Δf=-2.64 Hz
- t=99.598s, Δf=1.45 Hz
- t=99.898s, Δf=1.4 Hz
- t=100.087s, Δf=-1.69 Hz
- t=100.148s, Δf=1.01 Hz
- t=100.248s, Δf=-1.55 Hz
- t=100.348s, Δf=1.55 Hz
- t=100.448s, Δf=-1.63 Hz
- t=100.498s, Δf=1.23 Hz
- t=100.547s, Δf=-1.43 Hz
- t=100.598s, Δf=1.37 Hz
- t=100.698s, Δf=-1.65 Hz
- t=100.748s, Δf=1.18 Hz
- t=104.048s, Δf=-1.88 Hz
- t=104.098s, Δf=1.43 Hz
- t=104.848s, Δf=-2.43 Hz
- t=104.898s, Δf=1.74 Hz
- t=105.198s, Δf=-1.23 Hz
- t=105.998s, Δf=-1.75 Hz
- t=106.248s, Δf=-1.69 Hz
- t=107.248s, Δf=-1.59 Hz
- t=107.298s, Δf=1.18 Hz
- t=107.497s, Δf=-1.74 Hz
- t=107.598s, Δf=-1.93 Hz
- t=107.648s, Δf=1.5 Hz
- t=107.848s, Δf=-2.04 Hz
- t=107.898s, Δf=1.06 Hz
- t=108.097s, Δf=-3.06 Hz
- t=108.148s, Δf=1.82 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | -0.2048 | 817 |
| freq_vs_pitch_deg | 0.5194 | 817 |
| freq_vs_abs(p) | 0.2627 | 817 |
| freq_vs_abs(q) | 0.2120 | 817 |
| freq_vs_abs(r) | 0.0101 | 817 |
| freq_vs_manual_roll | 0.8483 | 406 |
| freq_vs_output[0] | 0.1525 | 815 |
| freq_vs_output[1] | 0.1654 | 815 |
| freq_vs_output[2] | 0.9402 | 815 |
| freq_vs_output[3] | nan | 815 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.1203 |  |  |
| manual.roll.max_abs | 0.1605 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0 |  |  |
| actuator_outputs.output[0].range | [1e+03, 1.82e+03] |  | top=0.00488, bottom=0.595 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 1.69e+03] |  | top=0.00244, bottom=0.107 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.81e+03] |  | top=0.0585, bottom=0.668 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.00244, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[4].range | [989, 1.75e+03] |  | top=0.00244, bottom=0.00488 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.00244, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.00244, bottom=0.998 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.00244, bottom=0.998 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
