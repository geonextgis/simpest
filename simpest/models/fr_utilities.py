"""
utilities.py – Biophysical helper functions for the FraNchEstYN model.

Translated from utilities.cs.

ReadFileOrExitsParameters was intentionally skipped in utilities.py. The C# ReadFileOrExitsParameters 
in utilities.cs is just a thin wrapper: In the Python rewrite, calibrated_read() was translated 
directly into param_reader.py:87 as a standalone function. Since the wrapper added no logic 
(the variety argument was even noted as "currently unused"), there was no need to reproduce 
it in utilities.py.

"""

from __future__ import annotations
import math


def t_response(t_ave: float, t_base: float, t_opt: float, t_max: float) -> float:
    """Beta-shaped temperature response function.

    Returns a dimensionless efficiency in [0, 1] as a function of the average
    temperature *t_ave* relative to the cardinal temperatures *t_base*
    (minimum), *t_opt* (optimum), and *t_max* (maximum).

    Formula (when t_base < t_ave < t_max):
        f = ((t_max - t_ave) / (t_max - t_opt))
            * ((t_ave - t_base) / (t_opt - t_base)) ** ((t_opt - t_base) / (t_max - t_opt))

    Returns 0 outside [t_base, t_max].
    """
    if t_ave <= t_base or t_ave >= t_max:
        return 0.0

    first_term = (t_max - t_ave) / (t_max - t_opt)
    second_term = (t_ave - t_base) / (t_opt - t_base)
    exponent = (t_opt - t_base) / (t_max - t_opt)

    return first_term * math.pow(second_term, exponent)


def rain_detachment(rainfall: float, rain50: float, f_int: float) -> float:
    """Rain-driven spore detachment index (dimensionless, 0–1).

    Saturates as rainfall increases relative to the capacity term (rain50 × fInt).

    Formula:
        detachment = rainfall / (rain50 * f_int + rainfall)

    Args:
        rainfall:  precipitation (mm) over the time step
        rain50:    half-saturation parameter (mm) – rainfall giving ~0.5 when fInt = 1
        f_int:     light interception fraction

    Returns 0.0 when rainfall is 0 or denominator is 0.
    """
    denominator = (rain50 * f_int) + rainfall
    if denominator == 0.0:
        return 0.0
    return rainfall / denominator
