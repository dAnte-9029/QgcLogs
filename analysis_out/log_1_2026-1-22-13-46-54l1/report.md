# Flight Analysis Report

## 1) Run Command

```bash
python3 analyze_flight.py --logdir csv/log_1_2026-1-22-13-46-54l1 --plots --report
```

## 2) Detected Topics

| logical | file(s) | timestamp_col | key_fields |
| --- | --- | --- | --- |
| flap_frequency | log_1_2026-1-22-13-46-54l1_flap_frequency_0.csv | timestamp | frequency_hz |
| manual_control_setpoint | log_1_2026-1-22-13-46-54l1_manual_control_setpoint_0.csv | timestamp | timestamp_sample, roll, pitch, yaw, throttle, flaps, aux1, aux2, aux3, aux4, aux5, aux6, buttons, valid, data_source, sticks_moving |
| vehicle_attitude | log_1_2026-1-22-13-46-54l1_vehicle_attitude_0.csv | timestamp | timestamp_sample, q[0], q[1], q[2], q[3], delta_q_reset[0], delta_q_reset[1], delta_q_reset[2], delta_q_reset[3], quat_reset_counter |
| vehicle_angular_velocity | log_1_2026-1-22-13-46-54l1_vehicle_angular_velocity_0.csv | timestamp | timestamp_sample, xyz[0], xyz[1], xyz[2], xyz_derivative[0], xyz_derivative[1], xyz_derivative[2] |
| vehicle_attitude_setpoint | log_1_2026-1-22-13-46-54l1_vehicle_attitude_setpoint_0.csv | timestamp | yaw_sp_move_rate, q_d[0], q_d[1], q_d[2], q_d[3], thrust_body[0], thrust_body[1], thrust_body[2], reset_integral, fw_control_yaw_wheel |
| vehicle_rates_setpoint | log_1_2026-1-22-13-46-54l1_vehicle_rates_setpoint_0.csv | timestamp | roll, pitch, yaw, thrust_body[0], thrust_body[1], thrust_body[2], reset_integral |
| actuator_outputs | log_1_2026-1-22-13-46-54l1_actuator_outputs_0.csv, log_1_2026-1-22-13-46-54l1_actuator_outputs_1.csv | timestamp | noutputs, output[0], output[1], output[2], output[3], output[4], output[5], output[6], output[7], output[8], output[9], output[10], output[11], output[12], output[13], output[14], output[15] |
| vehicle_local_position | log_1_2026-1-22-13-46-54l1_vehicle_local_position_0.csv | timestamp | timestamp_sample, ref_timestamp, ref_lat, ref_lon, x, y, z, delta_xy[0], delta_xy[1], delta_z, vx, vy, vz, z_deriv, delta_vxy[0], delta_vxy[1], delta_vz, ax, ay, az |
| vehicle_global_position | log_1_2026-1-22-13-46-54l1_vehicle_global_position_0.csv | timestamp | timestamp_sample, lat, lon, alt, alt_ellipsoid, delta_alt, delta_terrain, eph, epv, terrain_alt, lat_lon_valid, alt_valid, lat_lon_reset_counter, alt_reset_counter, terrain_reset_counter, terrain_alt_valid, dead_reckoning |
| vehicle_status | log_1_2026-1-22-13-46-54l1_vehicle_status_0.csv | timestamp | armed_time, takeoff_time, nav_state_timestamp, valid_nav_states_mask, can_set_nav_states_mask, failure_detector_status, arming_state, latest_arming_reason, latest_disarming_reason, nav_state_user_intention, nav_state, executor_in_charge, hil_state, vehicle_type, failsafe, failsafe_and_user_took_over, failsafe_defer_state, gcs_connection_lost, gcs_connection_lost_counter, high_latency_data_link_lost |
| sensor_gps | log_1_2026-1-22-13-46-54l1_vehicle_gps_position_0.csv | timestamp | timestamp_sample, latitude_deg, longitude_deg, altitude_msl_m, altitude_ellipsoid_m, time_utc_usec, device_id, s_variance_m_s, c_variance_rad, eph, epv, hdop, vdop, noise_per_ms, jamming_indicator, vel_m_s, vel_n_m_s, vel_e_m_s, vel_d_m_s, cog_rad |
| vehicle_air_data | log_1_2026-1-22-13-46-54l1_vehicle_air_data_0.csv | timestamp | timestamp_sample, baro_device_id, baro_alt_meter, baro_pressure_pa, ambient_temperature, rho, temperature_source, calibration_count |
| airspeed_validated | log_1_2026-1-22-13-46-54l1_airspeed_validated_0.csv | timestamp | indicated_airspeed_m_s, calibrated_airspeed_m_s, true_airspeed_m_s, calibrated_ground_minus_wind_m_s, true_ground_minus_wind_m_s, airspeed_derivative_filtered, throttle_filtered, pitch_filtered, airspeed_sensor_measurement_valid, selected_airspeed_index |

Missing topics:
- actuator_controls_0

## 3) Flight Overview

- logdir: `/home/honor/QgcLogs/csv/log_1_2026-1-22-13-46-54l1`
- analysis window: start=auto s, end=auto s (relative)
- duration_s: 556.176
- nav_state_changes: 5
- arming_state_changes: 0
- nav_state_unique: [0, 3, 15]
- arming_state_unique: [2]
- nav_state_transitions:
  - t=219.840s: {'nav_state': 0}
  - t=257.594s: {'nav_state': 15}
  - t=276.824s: {'nav_state': 3}
  - t=289.925s: {'nav_state': 15}
  - t=421.239s: {'nav_state': 0}
- arming_state_transitions:
- gps_summary: {'fix_type': {'mean': '3.4', 'std': '0.491', 'min': '3', 'p5': '3', 'p50': '3', 'p95': '4', 'max': '4'}, 'eph': {'mean': '0.407', 'std': '0.133', 'min': '0.158', 'p5': '0.17', 'p50': '0.425', 'p95': '0.575', 'max': '0.581'}, 'epv': {'mean': '0.606', 'std': '0.226', 'min': '0.224', 'p5': '0.243', 'p50': '0.64', 'p95': '0.898', 'max': '0.904'}}
- position_source: vehicle_local_position (x,y)
- altitude_source: vehicle_air_data.baro_alt_meter
- speed_source: sensor_gps.vel_m_s

## 4) Flap Frequency

- count: 7983
- mean_hz: 1.2692254269876808
- std_hz: 1.5768514112271625
- min_hz: -2.19221
- p5_hz: -0.005418182769999998
- p50_hz: 0.00048652923
- p95_hz: 3.78065277
- max_hz: 4.655859
- anomaly detection rules:
  - gap_threshold_s: 1.0000000000002274
  - step_threshold_hz: 1.0
  - dt_median_s: 0.05000000000001137
  - abs_dfreq_median_hz: 0.00629921045

Detected step events (|Δf| > step_threshold_hz):
- t=172.249s, Δf=-2.49 Hz
- t=172.289s, Δf=1.65 Hz
- t=173.089s, Δf=1.34 Hz
- t=175.049s, Δf=-1.18 Hz
- t=222.819s, Δf=1.06 Hz
- t=223.239s, Δf=1.04 Hz
- t=225.289s, Δf=1.02 Hz
- t=225.339s, Δf=-1.1 Hz
- t=236.389s, Δf=-1.09 Hz
- t=240.289s, Δf=-2.14 Hz
- t=240.339s, Δf=1.38 Hz
- t=252.399s, Δf=1.5 Hz
- t=262.549s, Δf=1.02 Hz
- t=262.589s, Δf=-1.13 Hz
- t=264.889s, Δf=-1.41 Hz
- t=264.939s, Δf=1.31 Hz
- t=265.139s, Δf=-1.03 Hz
- t=265.189s, Δf=1.21 Hz
- t=266.289s, Δf=-1.13 Hz
- t=266.339s, Δf=1.2 Hz
- t=268.339s, Δf=-2.06 Hz
- t=268.389s, Δf=2.01 Hz
- t=270.249s, Δf=1.21 Hz
- t=270.529s, Δf=-1.96 Hz
- t=270.599s, Δf=1.14 Hz
- t=270.639s, Δf=-1.37 Hz
- t=270.689s, Δf=1.1 Hz
- t=270.889s, Δf=-1.62 Hz
- t=270.939s, Δf=1.5 Hz
- t=271.839s, Δf=-1.72 Hz
- t=272.389s, Δf=-2.12 Hz
- t=272.439s, Δf=1.45 Hz
- t=272.639s, Δf=-2.11 Hz
- t=273.189s, Δf=-1.22 Hz
- t=273.239s, Δf=1.29 Hz
- t=273.989s, Δf=-1.04 Hz
- t=274.039s, Δf=1.3 Hz
- t=274.679s, Δf=-1.59 Hz
- t=274.739s, Δf=1.23 Hz
- t=274.939s, Δf=-1.4 Hz
- t=274.989s, Δf=1.02 Hz
- t=275.149s, Δf=-2.02 Hz
- t=275.239s, Δf=1.22 Hz
- t=275.728s, Δf=-1.02 Hz
- t=275.849s, Δf=1.14 Hz
- t=275.989s, Δf=-1.24 Hz
- t=276.039s, Δf=1.09 Hz
- t=276.439s, Δf=-3.7 Hz
- t=276.488s, Δf=1.24 Hz
- t=276.549s, Δf=1.29 Hz

## 5) Correlations

| metric | pearson_r | n |
| --- | --- | --- |
| freq_vs_roll_deg | -0.0511 | 7983 |
| freq_vs_pitch_deg | -0.0789 | 7983 |
| freq_vs_abs(p) | 0.4836 | 7983 |
| freq_vs_abs(q) | 0.2262 | 7983 |
| freq_vs_abs(r) | 0.2413 | 7983 |
| freq_vs_manual_roll | -0.0010 | 3930 |
| freq_vs_output[0] | 0.1902 | 7977 |
| freq_vs_output[1] | -0.3037 | 7977 |
| freq_vs_output[2] | 0.9768 | 7977 |
| freq_vs_output[3] | nan | 7977 |

- Interpretation: |r| < 0.3 weak, 0.3–0.7 moderate, > 0.7 strong.

## 6) Control Link Diagnostics

| metric | value | unit | notes |
| --- | --- | --- | --- |
| manual.roll.mean | -0.1562 |  |  |
| manual.roll.max_abs | 1 |  |  |
| manual.roll.sat_ratio(|roll|>=0.95) | 0.02303 |  |  |
| actuator_outputs.output[0].range | [1e+03, 2.15e+03] |  | top=0.00025, bottom=0.0493 (±1% range rule) |
| actuator_outputs.output[1].range | [1e+03, 2.11e+03] |  | top=0.00025, bottom=0.116 (±1% range rule) |
| actuator_outputs.output[2].range | [1e+03, 1.98e+03] |  | top=0.00175, bottom=0.581 (±1% range rule) |
| actuator_outputs.output[3].range | [0, 1e+03] |  | top=0.00025, bottom=1 (±1% range rule) |
| actuator_outputs.output[4].range | [800, 1.8e+03] |  | top=0.0015, bottom=0.0268 (±1% range rule) |
| actuator_outputs.output[5].range | [0, 1e+03] |  | top=0.00025, bottom=1 (±1% range rule) |
| actuator_outputs.output[6].range | [0, 1e+03] |  | top=0.00025, bottom=1 (±1% range rule) |
| actuator_outputs.output[7].range | [0, 1e+03] |  | top=0.00025, bottom=1 (±1% range rule) |

- Conclusions: Based on the above statistics and plots only.

## 7) Unfinished Items (Missing Topics/Fields)

- None

## Notes

- vehicle_attitude: Computed roll/pitch/yaw from quaternion q[0..3].
- vehicle_attitude_setpoint: Computed roll/pitch/yaw setpoint from quaternion q_d[0..3].
