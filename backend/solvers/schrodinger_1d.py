import numpy as np
from scipy.sparse import diags
from scipy.linalg import eigh
from scipy.sparse.linalg import splu

def solve_time_independent_1d(x, V, mass=1.0, hbar=1.0, num_eigen=5):
    """
    Solve the 1D time-independent Schrodinger equation using finite difference.
    Args:
        x (np.ndarray): 1D grid.
        V (np.ndarray): Potential array.
        mass (float): Particle mass.
        hbar (float): Planck's constant.
        num_eigen (int): Number of eigenstates to compute.
    Returns:
        energies (np.ndarray): Eigenvalues.
        wavefuncs (np.ndarray): Eigenfunctions (columns).
    """
    N = len(x)
    dx = x[1] - x[0]
    # Kinetic energy operator (finite difference, central)
    main_diag = np.full(N, -2.0)
    off_diag = np.ones(N-1)
    laplacian = diags([off_diag, main_diag, off_diag], [-1, 0, 1]) / dx**2
    T = -(hbar**2) / (2 * mass) * laplacian
    # Potential energy operator
    V_op = diags(V, 0)
    # Hamiltonian
    H = T + V_op
    # Convert to dense for eigenvalue solver
    H_dense = H.toarray()
    # Solve eigenvalue problem
    energies, wavefuncs = eigh(H_dense)
    # Select lowest num_eigen states
    energies = energies[:num_eigen]
    wavefuncs = wavefuncs[:, :num_eigen]
    # Normalize wavefunctions
    for n in range(num_eigen):
        norm = np.sqrt(np.trapz(np.abs(wavefuncs[:, n])**2, x))
        wavefuncs[:, n] /= norm
    return energies, wavefuncs

def solve_time_dependent_1d(x, psi0, V, times, mass=1.0, hbar=1.0, method='crank-nicolson'):
    """
    Solve the 1D time-dependent Schrodinger equation using Crank-Nicolson.
    Args:
        x (np.ndarray): 1D grid.
        psi0 (np.ndarray): Initial wave function.
        V (np.ndarray): Potential array.
        times (np.ndarray): Array of time points.
        mass (float): Particle mass.
        hbar (float): Planck's constant.
        method (str): Numerical method.
    Returns:
        psi_t (np.ndarray): Wave function at each time (shape: [len(times), len(x)]).
    """
    if method != 'crank-nicolson':
        raise NotImplementedError("Only Crank-Nicolson is implemented.")
    N = len(x)
    dx = x[1] - x[0]
    dt = times[1] - times[0]
    psi_t = np.zeros((len(times), N), dtype=complex)
    psi_t[0] = psi0
    # Hamiltonian
    main_diag = np.full(N, -2.0)
    off_diag = np.ones(N-1)
    laplacian = diags([off_diag, main_diag, off_diag], [-1, 0, 1]) / dx**2
    T = -(hbar**2) / (2 * mass) * laplacian
    V_op = diags(V, 0)
    H = T + V_op
    I = diags([np.ones(N)], [0])
    A = (I + 1j * dt * H / (2 * hbar)).tocsc()
    B = (I - 1j * dt * H / (2 * hbar)).tocsc()
    lu = splu(A)
    for n in range(1, len(times)):
        b = B.dot(psi_t[n-1])
        psi_t[n] = lu.solve(b)
        # Normalize
        norm = np.sqrt(np.trapz(np.abs(psi_t[n])**2, x))
        psi_t[n] /= norm
    return psi_t
