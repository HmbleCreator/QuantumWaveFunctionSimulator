import numpy as np
import numexpr as ne

def infinite_well_1d(x, xmin, xmax):
    """
    1D infinite square well potential.
    V=0 inside [xmin, xmax], V=inf outside.
    """
    V = np.zeros_like(x)
    V[(x < xmin) | (x > xmax)] = np.inf
    return V

def harmonic_oscillator_1d(x, m=1.0, omega=1.0):
    """
    1D harmonic oscillator potential: V(x) = 0.5 * m * omega^2 * x^2
    """
    return 0.5 * m * omega**2 * x**2

def infinite_well_2d(X, Y, xmin, xmax, ymin, ymax):
    """
    2D infinite square well potential.
    V=0 inside, V=inf outside.
    """
    V = np.zeros_like(X)
    V[(X < xmin) | (X > xmax) | (Y < ymin) | (Y > ymax)] = np.inf
    return V

def harmonic_oscillator_2d(X, Y, m=1.0, omega=1.0):
    """
    2D harmonic oscillator: V(x, y) = 0.5 * m * omega^2 * (x^2 + y^2)
    """
    return 0.5 * m * omega**2 * (X**2 + Y**2)

def finite_square_well_1d(x, xmin, xmax, V0=0.0, V_out=np.inf):
    """
    1D finite square well: V=V0 inside [xmin, xmax], V=V_out outside.
    """
    V = np.full_like(x, V_out)
    V[(x >= xmin) & (x <= xmax)] = V0
    return V

def double_well_1d(x, center1, center2, width, V0=0.0, V_out=np.inf):
    """
    1D double well: two wells at center1 and center2, each of given width.
    """
    V = np.full_like(x, V_out)
    V[(np.abs(x - center1) <= width/2) | (np.abs(x - center2) <= width/2)] = V0
    return V

def finite_square_well_2d(X, Y, xmin, xmax, ymin, ymax, V0=0.0, V_out=np.inf):
    """
    2D finite square well: V=V0 inside, V=V_out outside.
    """
    V = np.full_like(X, V_out)
    mask = (X >= xmin) & (X <= xmax) & (Y >= ymin) & (Y <= ymax)
    V[mask] = V0
    return V

def double_well_2d(X, Y, center1, center2, width, V0=0.0, V_out=np.inf):
    """
    2D double well: two wells at center1 and center2 (tuples), each of given width.
    """
    V = np.full_like(X, V_out)
    well1 = ((X - center1[0])**2 + (Y - center1[1])**2) <= (width/2)**2
    well2 = ((X - center2[0])**2 + (Y - center2[1])**2) <= (width/2)**2
    V[well1 | well2] = V0
    return V

def custom_potential_1d(x, func):
    """
    1D custom potential from a user-supplied function func(x).
    """
    return func(x)

def custom_potential_2d(X, Y, func):
    """
    2D custom potential from a user-supplied function func(X, Y).
    """
    return func(X, Y)

def gaussian_well_1d(x, center, width, depth):
    """
    1D Gaussian well: V(x) = -depth * exp(-((x-center)^2)/(2*width^2))
    """
    return -depth * np.exp(-((x-center)**2) / (2*width**2))

def gaussian_barrier_1d(x, center, width, height):
    """
    1D Gaussian barrier: V(x) = height * exp(-((x-center)^2)/(2*width^2))
    """
    return height * np.exp(-((x-center)**2) / (2*width**2))

def periodic_cosine_1d(x, amplitude, period):
    """
    1D periodic cosine potential: V(x) = amplitude * cos(2*pi*x/period)
    """
    return amplitude * np.cos(2 * np.pi * x / period)

def linear_ramp_1d(x, slope, offset=0.0):
    """
    1D linear ramp: V(x) = slope * x + offset
    """
    return slope * x + offset

def gaussian_well_2d(X, Y, center, width, depth):
    """
    2D Gaussian well: V(x, y) = -depth * exp(-((x-x0)^2 + (y-y0)^2)/(2*width^2))
    """
    return -depth * np.exp(-((X-center[0])**2 + (Y-center[1])**2) / (2*width**2))

def gaussian_barrier_2d(X, Y, center, width, height):
    """
    2D Gaussian barrier: V(x, y) = height * exp(-((x-x0)^2 + (y-y0)^2)/(2*width^2))
    """
    return height * np.exp(-((X-center[0])**2 + (Y-center[1])**2) / (2*width**2))

def periodic_cosine_2d(X, Y, amplitude, period_x, period_y):
    """
    2D periodic cosine: V(x, y) = amplitude * [cos(2*pi*x/period_x) + cos(2*pi*y/period_y)]
    """
    return amplitude * (np.cos(2 * np.pi * X / period_x) + np.cos(2 * np.pi * Y / period_y))

def linear_ramp_2d(X, Y, slope_x, slope_y, offset=0.0):
    """
    2D linear ramp: V(x, y) = slope_x * x + slope_y * y + offset
    """
    return slope_x * X + slope_y * Y + offset

def custom_potential_expr_1d(x, expr, local_dict=None):
    """
    Evaluate a custom 1D potential from a string expression using numexpr.
    Args:
        x (np.ndarray): 1D grid.
        expr (str): Expression, e.g. 'sin(x) + x**2'.
        local_dict (dict): Additional variables for evaluation.
    Returns:
        V (np.ndarray): Evaluated potential.
    Example:
        V = custom_potential_expr_1d(x, 'sin(x) + x**2')
    """
    if local_dict is None:
        local_dict = {}
    local_dict = {**local_dict, 'x': x, 'np': np}
    return ne.evaluate(expr, local_dict=local_dict)

def custom_potential_expr_2d(X, Y, expr, local_dict=None):
    """
    Evaluate a custom 2D potential from a string expression using numexpr.
    Args:
        X, Y (np.ndarray): 2D meshgrid arrays.
        expr (str): Expression, e.g. 'sin(X) + Y**2'.
        local_dict (dict): Additional variables for evaluation.
    Returns:
        V (np.ndarray): Evaluated potential.
    Example:
        V = custom_potential_expr_2d(X, Y, 'sin(X) + Y**2')
    """
    if local_dict is None:
        local_dict = {}
    local_dict = {**local_dict, 'X': X, 'Y': Y, 'np': np}
    return ne.evaluate(expr, local_dict=local_dict)
