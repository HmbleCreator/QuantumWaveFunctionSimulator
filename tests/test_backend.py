import numpy as np
import pytest
from backend.utils import grid, numerics
from backend.potentials import basic
from backend.solvers import schrodinger_1d, schrodinger_2d

def test_grid_1d():
    x, dx = grid.create_1d_grid(-1, 1, 100)
    assert x.shape == (100,)
    assert np.isclose(dx, 2/99)

def test_grid_2d():
    X, Y, dx, dy = grid.create_2d_grid(-1, 1, 50, -1, 1, 50)
    assert X.shape == Y.shape == (50, 50)
    assert np.isclose(dx, 2/49)
    assert np.isclose(dy, 2/49)

def test_potentials_1d():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    V_inf = basic.infinite_well_1d(x, -0.5, 0.5)
    V_ho = basic.harmonic_oscillator_1d(x)
    V_finite = basic.finite_square_well_1d(x, -0.5, 0.5, V0=-2, V_out=5)
    V_double = basic.double_well_1d(x, -0.5, 0.5, 0.2)
    V_gauss = basic.gaussian_well_1d(x, 0, 0.2, 5)
    V_cos = basic.periodic_cosine_1d(x, 1, 1)
    V_ramp = basic.linear_ramp_1d(x, 2)
    assert V_inf.shape == x.shape
    assert V_ho.shape == x.shape
    assert V_finite.shape == x.shape
    assert V_double.shape == x.shape
    assert V_gauss.shape == x.shape
    assert V_cos.shape == x.shape
    assert V_ramp.shape == x.shape

def test_potentials_2d():
    X, Y, _, _ = grid.create_2d_grid(-1, 1, 30, -1, 1, 30)
    V_inf = basic.infinite_well_2d(X, Y, -0.5, 0.5, -0.5, 0.5)
    V_ho = basic.harmonic_oscillator_2d(X, Y)
    V_finite = basic.finite_square_well_2d(X, Y, -0.5, 0.5, -0.5, 0.5, V0=-2, V_out=5)
    V_double = basic.double_well_2d(X, Y, (-0.5, 0), (0.5, 0), 0.2)
    V_gauss = basic.gaussian_well_2d(X, Y, (0,0), 0.2, 5)
    V_cos = basic.periodic_cosine_2d(X, Y, 1, 1, 1)
    V_ramp = basic.linear_ramp_2d(X, Y, 2, 2)
    assert V_inf.shape == X.shape
    assert V_ho.shape == X.shape
    assert V_finite.shape == X.shape
    assert V_double.shape == X.shape
    assert V_gauss.shape == X.shape
    assert V_cos.shape == X.shape
    assert V_ramp.shape == X.shape

def test_numerics_1d():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    psi = np.exp(-x**2)
    psi /= np.sqrt(np.trapz(np.abs(psi)**2, x))
    assert np.isclose(np.trapz(np.abs(psi)**2, x), 1, atol=1e-2)
    pd = numerics.probability_density(psi)
    ex = numerics.expectation_x(x, psi)
    ep = numerics.expectation_p(x, psi)
    assert pd.shape == x.shape
    assert np.abs(ex) < 0.1
    assert np.abs(ep) < 1

def test_numerics_2d():
    X, Y, dx, dy = grid.create_2d_grid(-1, 1, 30, -1, 1, 30)
    psi = np.exp(-X**2 - Y**2)
    psi /= np.sqrt(np.trapz(np.trapz(np.abs(psi)**2, Y[0,:]), X[:,0]))
    pd = numerics.probability_density(psi)
    ex = numerics.expectation_x_2d(X, Y, psi)
    ey = numerics.expectation_y_2d(X, Y, psi)
    assert pd.shape == X.shape
    assert np.abs(ex) < 0.1
    assert np.abs(ey) < 0.1

def test_solvers_1d():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    V = basic.infinite_well_1d(x, -1, 1)
    energies, wavefuncs = schrodinger_1d.solve_time_independent_1d(x, V, num_eigen=3)
    assert energies.shape == (3,)
    assert wavefuncs.shape == (100, 3)
    # Time-dependent: free evolution
    psi0 = np.exp(-10*(x+0.5)**2)
    psi0 /= np.sqrt(np.trapz(np.abs(psi0)**2, x))
    times = np.linspace(0, 0.01, 5)
    psi_t = schrodinger_1d.solve_time_dependent_1d(x, psi0, V, times)
    assert psi_t.shape == (5, 100)

def test_solvers_2d():
    X, Y, _, _ = grid.create_2d_grid(-1, 1, 20, -1, 1, 20)
    V = basic.infinite_well_2d(X, Y, -1, 1, -1, 1)
    energies, wavefuncs = schrodinger_2d.solve_time_independent_2d(X, Y, V, num_eigen=2)
    assert energies.shape == (2,)
    assert wavefuncs.shape == (2, 20, 20)
    # Time-dependent: free evolution
    psi0 = np.exp(-10*((X+0.5)**2 + (Y+0.5)**2))
    psi0 /= np.sqrt(np.trapz(np.trapz(np.abs(psi0)**2, Y[0,:]), X[:,0]))
    times = np.linspace(0, 0.01, 3)
    psi_t = schrodinger_2d.solve_time_dependent_2d(X, Y, psi0, V, times)
    assert psi_t.shape == (3, 20, 20)

def test_custom_potential_expr():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    V = basic.custom_potential_expr_1d(x, 'x**2 + 2')
    assert np.allclose(V, x**2 + 2)
    X, Y, _, _ = grid.create_2d_grid(-1, 1, 20, -1, 1, 20)
    V2 = basic.custom_potential_expr_2d(X, Y, 'X**2 + Y**2')
    assert np.allclose(V2, X**2 + Y**2)

def test_custom_observable_expr():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    psi = np.exp(-x**2)
    psi /= np.sqrt(np.trapz(np.abs(psi)**2, x))
    val = numerics.expectation_custom_expr_1d(x, psi, 'x * abs(psi)**2')
    assert np.abs(val) < 0.1
    X, Y, _, _ = grid.create_2d_grid(-1, 1, 20, -1, 1, 20)
    psi2 = np.exp(-X**2 - Y**2)
    psi2 /= np.sqrt(np.trapz(np.trapz(np.abs(psi2)**2, Y[0,:]), X[:,0]))
    val2 = numerics.expectation_custom_expr_2d(X, Y, psi2, 'X * abs(psi)**2')
    assert np.abs(val2) < 0.1

def test_save_load():
    x, _ = grid.create_1d_grid(-1, 1, 100)
    psi = np.exp(-x**2)
    numerics.save_simulation('test_save.npz', x=x, psi=psi)
    data = numerics.load_simulation('test_save.npz')
    assert 'x' in data and 'psi' in data
    assert np.allclose(data['x'], x)
    assert np.allclose(data['psi'], psi) 