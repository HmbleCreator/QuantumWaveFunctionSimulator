import numpy as np
import numexpr as ne

def probability_density(psi):
    """
    Compute probability density |psi|^2.
    """
    return np.abs(psi)**2

def expectation_x(x, psi):
    """
    Expectation value of position <x>.
    """
    dens = probability_density(psi)
    return np.sum(x * dens) / np.sum(dens)

def expectation_p(x, psi, hbar=1.0):
    """
    Expectation value of momentum <p> using finite difference.
    """
    dx = x[1] - x[0]
    dpsi_dx = np.gradient(psi, dx)
    p_op_psi = -1j * hbar * dpsi_dx
    return np.sum(np.conj(psi) * p_op_psi).real * dx / np.sum(np.abs(psi)**2 * dx)

def expectation_energy(x, psi, V, mass=1.0, hbar=1.0):
    """
    Expectation value of energy <E>.
    """
    dx = x[1] - x[0]
    d2psi_dx2 = np.gradient(np.gradient(psi, dx), dx)
    kinetic = -0.5 * hbar**2 / mass * d2psi_dx2
    E = np.sum(np.conj(psi) * (kinetic + V * psi)) * dx / np.sum(np.abs(psi)**2 * dx)
    return E.real

def expectation_observable(x, psi, op):
    """
    General expectation value <O> for operator op (function taking psi and x).
    """
    Opsi = op(x, psi)
    dx = x[1] - x[0]
    return np.sum(np.conj(psi) * Opsi) * dx / np.sum(np.abs(psi)**2 * dx)

def expectation_x_2d(X, Y, psi):
    """
    Expectation value of x in 2D.
    """
    dens = np.abs(psi)**2
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    return np.sum(X * dens) * dx * dy / np.sum(dens * dx * dy)

def expectation_y_2d(X, Y, psi):
    """
    Expectation value of y in 2D.
    """
    dens = np.abs(psi)**2
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    return np.sum(Y * dens) * dx * dy / np.sum(dens * dx * dy)

def expectation_px_2d(X, Y, psi, hbar=1.0):
    """
    Expectation value of p_x in 2D using finite difference.
    """
    dx = X[1,0] - X[0,0]
    dpsi_dx = np.gradient(psi, dx, axis=0)
    p_op_psi = -1j * hbar * dpsi_dx
    dens = np.abs(psi)**2
    dy = Y[0,1] - Y[0,0]
    return np.sum(np.conj(psi) * p_op_psi).real * dx * dy / np.sum(dens * dx * dy)

def expectation_py_2d(X, Y, psi, hbar=1.0):
    """
    Expectation value of p_y in 2D using finite difference.
    """
    dy = Y[0,1] - Y[0,0]
    dpsi_dy = np.gradient(psi, dy, axis=1)
    p_op_psi = -1j * hbar * dpsi_dy
    dens = np.abs(psi)**2
    dx = X[1,0] - X[0,0]
    return np.sum(np.conj(psi) * p_op_psi).real * dx * dy / np.sum(dens * dx * dy)

def expectation_energy_2d(X, Y, psi, V, mass=1.0, hbar=1.0):
    """
    Expectation value of energy <E> in 2D.
    """
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    d2psi_dx2 = np.gradient(np.gradient(psi, dx, axis=0), dx, axis=0)
    d2psi_dy2 = np.gradient(np.gradient(psi, dy, axis=1), dy, axis=1)
    kinetic = -0.5 * hbar**2 / mass * (d2psi_dx2 + d2psi_dy2)
    E = np.sum(np.conj(psi) * (kinetic + V * psi)) * dx * dy / np.sum(np.abs(psi)**2 * dx * dy)
    return E.real

def expectation_observable_2d(X, Y, psi, op):
    """
    General expectation value <O> for operator op(X, Y, psi).
    """
    Opsi = op(X, Y, psi)
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    return np.sum(np.conj(psi) * Opsi) * dx * dy / np.sum(np.abs(psi)**2 * dx * dy)

def expectation_custom_expr_1d(x, psi, expr, local_dict=None):
    """
    Compute expectation value of a custom 1D observable from a string expression using numexpr.
    Args:
        x (np.ndarray): 1D grid.
        psi (np.ndarray): Wave function.
        expr (str): Expression, e.g. 'x * abs(psi)**2'.
        local_dict (dict): Additional variables for evaluation.
    Returns:
        float: Expectation value.
    Example:
        val = expectation_custom_expr_1d(x, psi, 'x * abs(psi)**2')
    """
    if local_dict is None:
        local_dict = {}
    local_dict = {**local_dict, 'x': x, 'psi': psi, 'abs': np.abs, 'real': np.real, 'imag': np.imag, 'conj': np.conj, 'np': np}
    dx = x[1] - x[0]
    O = ne.evaluate(expr, local_dict=local_dict)
    return np.sum(O) * dx / np.sum(np.abs(psi)**2 * dx)

def expectation_custom_expr_2d(X, Y, psi, expr, local_dict=None):
    """
    Compute expectation value of a custom 2D observable from a string expression using numexpr.
    Args:
        X, Y (np.ndarray): 2D meshgrid arrays.
        psi (np.ndarray): Wave function.
        expr (str): Expression, e.g. 'X * abs(psi)**2'.
        local_dict (dict): Additional variables for evaluation.
    Returns:
        float: Expectation value.
    Example:
        val = expectation_custom_expr_2d(X, Y, psi, 'X * abs(psi)**2')
    """
    if local_dict is None:
        local_dict = {}
    local_dict = {**local_dict, 'X': X, 'Y': Y, 'psi': psi, 'abs': np.abs, 'real': np.real, 'imag': np.imag, 'conj': np.conj, 'np': np}
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    O = ne.evaluate(expr, local_dict=local_dict)
    return np.sum(O) * dx * dy / np.sum(np.abs(psi)**2 * dx * dy)

def save_simulation(filename, **kwargs):
    """
    Save simulation data (wavefunctions, grids, etc.) to a .npz file.
    """
    np.savez_compressed(filename, **kwargs)

def load_simulation(filename):
    """
    Load simulation data from a .npz file.
    Returns a dict-like object.
    """
    return np.load(filename, allow_pickle=True)
