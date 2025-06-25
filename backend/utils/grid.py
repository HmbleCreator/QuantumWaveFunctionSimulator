import numpy as np

def create_1d_grid(xmin, xmax, num_points):
    """
    Create a 1D spatial grid.
    Args:
        xmin (float): Minimum x value.
        xmax (float): Maximum x value.
        num_points (int): Number of grid points.
    Returns:
        x (np.ndarray): 1D array of grid points.
        dx (float): Grid spacing.
    """
    if num_points < 2:
        raise ValueError("num_points must be at least 2.")
    x = np.linspace(xmin, xmax, num_points)
    dx = x[1] - x[0]
    return x, dx

def create_2d_grid(xmin, xmax, num_x, ymin, ymax, num_y):
    """
    Create a 2D spatial grid.
    Args:
        xmin, xmax (float): x range.
        num_x (int): Number of x grid points.
        ymin, ymax (float): y range.
        num_y (int): Number of y grid points.
    Returns:
        X, Y (np.ndarray): 2D meshgrid arrays.
        dx, dy (float): Grid spacings.
    """
    if num_x < 2 or num_y < 2:
        raise ValueError("num_x and num_y must be at least 2.")
    x = np.linspace(xmin, xmax, num_x)
    y = np.linspace(ymin, ymax, num_y)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    X, Y = np.meshgrid(x, y, indexing='ij')
    return X, Y, dx, dy
