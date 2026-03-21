# 2026-03-03 Flight Analysis

## Real-flight logs (auto-classified)
- log_21_2026-3-3-10-29-26
- log_24_2026-3-3-11-32-52
- log_29_2026-3-3-16-42-00

Latest real flight treated as new-parts flight: **log_29_2026-3-3-16-42-00**

## Key metrics (active flight windows)

log,active_duration_s,ias_p50,ias_p95,cas_p50,cas_p95,tas_p50,tas_p95,throttle_p50,throttle_p95,flap_p50_hz,flap_p95_hz,airspeed_deriv_raw_std,airspeed_deriv_filt_std,deriv_filter_std_ratio,airspeed_source_values,airspeed_source_transitions,throttle_vs_flap_r,throttle_vs_flap_best_lag_s,throttle_out_channel,throttle_out_corr
log_21_2026-3-3-10-29-26,86.4,6.652,9.343,6.811,9.567,6.732,9.457,0.689,0.729,4.038,4.356,14.742,0.0,0.0,1,0,0.992,-0.4,output[2],0.961
log_24_2026-3-3-11-32-52,26.4,6.996,10.318,7.163,10.565,7.095,10.459,0.632,0.64,3.717,4.081,17.918,0.0,0.0,1,0,0.951,-0.3,,
log_29_2026-3-3-16-42-00,44.4,7.409,9.906,7.586,10.141,7.531,10.065,0.631,0.651,3.76,4.068,8.461,0.0,0.0,1,0,0.963,-0.4,output[2],0.94


## Notes
- log_21_2026-3-3-10-29-26: TAS p95=9.46 m/s, throttle p95=0.729, flap p95=4.36 Hz; filtered derivative is much smoother (ratio=0.00); throttle-flap r=0.99 at lag -0.4s
- log_24_2026-3-3-11-32-52: TAS p95=10.46 m/s, throttle p95=0.640, flap p95=4.08 Hz; filtered derivative is much smoother (ratio=0.00); throttle-flap r=0.95 at lag -0.3s
- log_29_2026-3-3-16-42-00: TAS p95=10.06 m/s, throttle p95=0.651, flap p95=4.07 Hz; filtered derivative is much smoother (ratio=0.00); throttle-flap r=0.96 at lag -0.4s