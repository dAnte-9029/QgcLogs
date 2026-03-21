# RTK Accuracy Review

This report uses PX4 GPS / EKF fields from sensor_gps, vehicle_global_position, vehicle_local_position, and estimator_status.

## Summary CSV

log,armed_s,fix_counts,rtk_fixed_ratio_active,rtk_float_or_better_ratio_active,sat_used_p50,eph_p50_m,eph_p95_m,epv_p50_m,epv_p95_m,rtcm_rate_p95,rtcm_msg_used_max,selected_rtcm_instance_values,est_hacc_p50_m,est_hacc_p95_m,raw_gps_stationary_h95_m,raw_gps_stationary_rms_m,local_pos_stationary_h95_m,local_pos_stationary_rms_m
log_0_2026-3-7-17-56-30,86.992,"{3: 112, 4: 1}",0.0,0.0,28.0,2.311,3.372,2.578,3.003,0.16,0.0,0,,,0.385,0.238,1.688,0.819
log_1_2026-3-8-10-02-40,16.001,{3: 28},0.0,0.0,28.0,1.941,2.126,2.414,2.529,0.0,0.0,0,0.484,0.501,,,0.201,0.139
