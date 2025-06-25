import numpy as np
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh, splu

def solve_time_independent_2d(X, Y, V, mass=1.0, hbar=1.0, num_eigen=5):
    """
    Solve the 2D time-independent Schrodinger equation using finite difference.
    Args:
        X, Y (np.ndarray): 2D meshgrid arrays.
        V (np.ndarray): 2D potential array.
        mass (float): Particle mass.
        hbar (float): Planck's constant.
        num_eigen (int): Number of eigenstates to compute.
    Returns:
        energies (np.ndarray): Eigenvalues.
        wavefuncs (np.ndarray): Eigenfunctions (shape: [num_eigen, X.shape[0], X.shape[1]]).
    """
    Nx, Ny = X.shape
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    # 1D Laplacians
    main_x = np.full(Nx, -2.0)
    off_x = np.ones(Nx-1)
    Lx = diags([off_x, main_x, off_x], [-1, 0, 1]) / dx**2
    main_y = np.full(Ny, -2.0)
    off_y = np.ones(Ny-1)
    Ly = diags([off_y, main_y, off_y], [-1, 0, 1]) / dy**2
    # 2D Laplacian
    Lap = kron(identity(Ny), Lx) + kron(Ly, identity(Nx))
    T = -(hbar**2) / (2 * mass) * Lap
    V_flat = V.ravel()
    V_op = diags(V_flat, 0)
    H = T + V_op
    # Solve sparse eigenvalue problem
    energies, wavefuncs = eigsh(H, k=num_eigen, which='SM')
    # Reshape eigenfunctions
    wavefuncs_reshaped = np.zeros((num_eigen, Nx, Ny), dtype=np.complex128)
    for n in range(num_eigen):
        wf = wavefuncs[:, n].reshape((Nx, Ny))
        # Normalize
        norm = np.sqrt(np.trapz(np.trapz(np.abs(wf)**2, Y[0,:]), X[:,0]))
        wavefuncs_reshaped[n] = wf / norm
    return energies, wavefuncs_reshaped

def solve_time_dependent_2d(X, Y, psi0, V, times, mass=1.0, hbar=1.0, method='crank-nicolson'):
    """
    Solve the 2D time-dependent Schrodinger equation using Crank-Nicolson.
    Args:
        X, Y (np.ndarray): 2D meshgrid arrays.
        psi0 (np.ndarray): Initial wave function (2D array).
        V (np.ndarray): 2D potential array.
        times (np.ndarray): Array of time points.
        mass (float): Particle mass.
        hbar (float): Planck's constant.
        method (str): Numerical method.
    Returns:
        psi_t (np.ndarray): Wave function at each time (shape: [len(times), X.shape[0], X.shape[1]]).
    """
    if method != 'crank-nicolson':
        raise NotImplementedError("Only Crank-Nicolson is implemented.")
    Nx, Ny = X.shape
    N = Nx * Ny
    dx = X[1,0] - X[0,0]
    dy = Y[0,1] - Y[0,0]
    dt = times[1] - times[0]
    psi_t = np.zeros((len(times), Nx, Ny), dtype=complex)
    psi_t[0] = psi0
    # 1D Laplacians
    main_x = np.full(Nx, -2.0)
    off_x = np.ones(Nx-1)
    Lx = diags([off_x, main_x, off_x], [-1, 0, 1]) / dx**2
    main_y = np.full(Ny, -2.0)
    off_y = np.ones(Ny-1)
    Ly = diags([off_y, main_y, off_y], [-1, 0, 1]) / dy**2
    Lap = kron(identity(Ny), Lx) + kron(Ly, identity(Nx))
    T = -(hbar**2) / (2 * mass) * Lap
    V_flat = V.ravel()
    V_op = diags(V_flat, 0)
    H = T + V_op
    I = diags([np.ones(N)], [0])
    A = (I + 1j * dt * H / (2 * hbar)).tocsc()
    B = (I - 1j * dt * H / (2 * hbar)).tocsc()
    lu = splu(A)
    psi_vec = psi0.ravel()
    for n in range(1, len(times)):
        b = B.dot(psi_vec)
        psi_vec = lu.solve(b)
        # Normalize
        norm = np.sqrt(np.trapz(np.trapz(np.abs(psi_vec.reshape((Nx, Ny)))**2, Y[0,:]), X[:,0]))
        psi_vec /= norm
        psi_t[n] = psi_vec.reshape((Nx, Ny))
    return psi_t
