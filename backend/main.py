from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
from backend.utils import grid, numerics
from backend.potentials import basic
from backend.solvers import schrodinger_1d, schrodinger_2d

app = FastAPI()

# Allow all origins for now (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TimeIndep1DRequest(BaseModel):
    xmin: float
    xmax: float
    num_points: int
    potential_expr: str
    mass: float = 1.0
    hbar: float = 1.0
    num_eigen: int = 5

class TimeDep1DRequest(TimeIndep1DRequest):
    psi0_expr: str
    times: list[float]
    method: str = 'crank-nicolson'

class TimeIndep2DRequest(BaseModel):
    xmin: float
    xmax: float
    num_x: int
    ymin: float
    ymax: float
    num_y: int
    potential_expr: str
    mass: float = 1.0
    hbar: float = 1.0
    num_eigen: int = 5

class TimeDep2DRequest(TimeIndep2DRequest):
    psi0_expr: str
    times: list[float]
    method: str = 'crank-nicolson'

class ObservableRequest(BaseModel):
    x: list[float] = None
    X: list[list[float]] = None
    Y: list[list[float]] = None
    psi: list[float] = None
    psi2d: list[list[float]] = None
    expr: str

@app.get("/")
def read_root():
    return {"message": "Quantum Wave Function Simulator API (FastAPI)"}

@app.post("/solve/1d/timeindependent")
def solve_1d_timeindependent(req: TimeIndep1DRequest):
    try:
        x, dx = grid.create_1d_grid(req.xmin, req.xmax, req.num_points)
        V = basic.custom_potential_expr_1d(x, req.potential_expr)
        energies, wavefuncs = schrodinger_1d.solve_time_independent_1d(
            x, V, mass=req.mass, hbar=req.hbar, num_eigen=req.num_eigen)
        return {
            "x": x.tolist(),
            "V": V.tolist(),
            "energies": energies.tolist(),
            "wavefuncs": wavefuncs.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/solve/1d/timedependent")
def solve_1d_timedependent(req: TimeDep1DRequest):
    try:
        x, dx = grid.create_1d_grid(req.xmin, req.xmax, req.num_points)
        V = basic.custom_potential_expr_1d(x, req.potential_expr)
        psi0 = basic.custom_potential_expr_1d(x, req.psi0_expr)
        psi0 = psi0.astype(complex)
        psi0 /= np.sqrt(np.trapz(np.abs(psi0)**2, x))
        times = np.array(req.times)
        psi_t = schrodinger_1d.solve_time_dependent_1d(
            x, psi0, V, times, mass=req.mass, hbar=req.hbar, method=req.method)
        return {
            "x": x.tolist(),
            "V": V.tolist(),
            "times": times.tolist(),
            "psi_t": psi_t.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/solve/2d/timeindependent")
def solve_2d_timeindependent(req: TimeIndep2DRequest):
    try:
        X, Y, dx, dy = grid.create_2d_grid(req.xmin, req.xmax, req.num_x, req.ymin, req.ymax, req.num_y)
        V = basic.custom_potential_expr_2d(X, Y, req.potential_expr)
        energies, wavefuncs = schrodinger_2d.solve_time_independent_2d(
            X, Y, V, mass=req.mass, hbar=req.hbar, num_eigen=req.num_eigen)
        return {
            "X": X.tolist(),
            "Y": Y.tolist(),
            "V": V.tolist(),
            "energies": energies.tolist(),
            "wavefuncs": wavefuncs.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/solve/2d/timedependent")
def solve_2d_timedependent(req: TimeDep2DRequest):
    try:
        X, Y, dx, dy = grid.create_2d_grid(req.xmin, req.xmax, req.num_x, req.ymin, req.ymax, req.num_y)
        V = basic.custom_potential_expr_2d(X, Y, req.potential_expr)
        psi0 = basic.custom_potential_expr_2d(X, Y, req.psi0_expr)
        psi0 = psi0.astype(complex)
        psi0 /= np.sqrt(np.trapz(np.trapz(np.abs(psi0)**2, Y[0,:]), X[:,0]))
        times = np.array(req.times)
        psi_t = schrodinger_2d.solve_time_dependent_2d(
            X, Y, psi0, V, times, mass=req.mass, hbar=req.hbar, method=req.method)
        return {
            "X": X.tolist(),
            "Y": Y.tolist(),
            "V": V.tolist(),
            "times": times.tolist(),
            "psi_t": psi_t.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/observable/eval")
def eval_observable(req: ObservableRequest):
    try:
        if req.x and req.psi:
            x = np.array(req.x)
            psi = np.array(req.psi)
            val = numerics.expectation_custom_expr_1d(x, psi, req.expr)
            return {"value": float(val)}
        elif req.X and req.Y and req.psi2d:
            X = np.array(req.X)
            Y = np.array(req.Y)
            psi2d = np.array(req.psi2d)
            val = numerics.expectation_custom_expr_2d(X, Y, psi2d, req.expr)
            return {"value": float(val)}
        else:
            raise ValueError("Invalid input for observable evaluation.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
