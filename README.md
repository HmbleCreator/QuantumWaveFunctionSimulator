# Quantum Wave Function Simulator

**Quantum Wave Function Simulator** is an interactive, full-stack web application for simulating and visualizing quantum systems in 1D and 2D. It numerically solves the time-dependent and time-independent Schrödinger equations, allowing users to explore quantum dynamics, stationary states, and a wide variety of potential landscapes.

## ✨ Features

- **1D & 2D Quantum Simulation:**  
  Solve the time-dependent and time-independent Schrödinger equations for custom or built-in potentials.
- **Custom Potentials:**  
  Enter mathematical expressions for potential energy (e.g., `x**2`, `sin(X) + cos(Y)`, `10*((X**2-1)**2 + Y**2)`).
- **Flexible Initial States:**  
  Specify initial wave functions as expressions (e.g., `exp(-10*(x+0.5)**2)`).
- **Real-Time Visualization:**  
  Interactive, animated plots of probability density |ψ|², with zoom, pan, and time evolution controls.
- **Modern UI:**  
  Responsive, full-screen layout with easy navigation between 1D and 2D panels.
- **Robust Backend:**  
  Python (FastAPI) backend with NumPy/SciPy for numerics, safe expression parsing, and error handling.
- **Frontend:**  
  React + Vite + Plotly.js + Material-UI for a beautiful, interactive user experience.

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quantum-wave-simulator.git
cd quantum-wave-simulator
```

### 2. Backend (Python/FastAPI)

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload
```
- The backend runs at `http://localhost:8000`

### 3. Frontend (React/Vite)

```bash
cd ../frontend
npm install
npm run dev
```
- The frontend runs at `http://localhost:5173`

### 4. Usage

- Open your browser at `http://localhost:5173`
- Use the navigation bar to switch between 1D and 2D simulators.
- Enter grid parameters, potential, initial state, and times.
- Click **Run Simulation** to visualize quantum evolution.

## 🖥️ Example Inputs

**1D Harmonic Oscillator**
- Potential: `x**2`
- Initial State: `exp(-10*(x+0.5)**2)`

**2D Double Well**
- Potential: `10*((X**2-1)**2 + Y**2)`
- Initial State: `exp(-5*(X**2 + Y**2))`

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, NumPy, SciPy
- **Frontend:** React, Vite, Plotly.js, Material-UI
- **API:** REST (JSON)

## 📁 Project Structure

```
backend/
  main.py           # FastAPI backend
  solvers/          # Schrödinger equation solvers
  potentials/       # Built-in and custom potentials
  utils/            # Grids, numerics, helpers

frontend/
  src/
    components/     # 1D/2D panels, UI components
    App.jsx         # Main app with navigation
    main.jsx        # Entry point
```

## 🧑‍💻 Contributing

Pull requests and suggestions are welcome! Please open an issue to discuss major changes.

## 📄 License

MIT License

---

**Enjoy exploring quantum mechanics interactively!**



#
