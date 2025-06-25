import React, { useState } from 'react';
import { Box, Paper, Typography, TextField, Button, Stack, CircularProgress } from '@mui/material';
import Plot from 'react-plotly.js';
import axios from 'axios';

const Quantum1DPanel = () => {
  const [xmin, setXmin] = useState(-1);
  const [xmax, setXmax] = useState(1);
  const [numPoints, setNumPoints] = useState(200);
  const [potentialExpr, setPotentialExpr] = useState('0');
  const [psi0Expr, setPsi0Expr] = useState('exp(-10*(x+0.5)**2)');
  const [times, setTimes] = useState('0,0.01,0.02,0.03,0.04');
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(null);
  const [error, setError] = useState('');
  const [frame, setFrame] = useState(0);

  const handleRun = async () => {
    setLoading(true);
    setError('');
    setPlotData(null);
    try {
      const timesArr = times.split(',').map(Number);
      const res = await axios.post('http://localhost:8000/solve/1d/timedependent', {
        xmin,
        xmax,
        num_points: numPoints,
        potential_expr: potentialExpr,
        psi0_expr: psi0Expr,
        times: timesArr
      });
      setPlotData(res.data);
      setFrame(0);
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFrameChange = (e, value) => {
    setFrame(Number(value));
  };

  return (
    <Box sx={{ height: '100vh', width: '100vw', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', p: 0, m: 0 }}>
      <Box sx={{ width: '100vw', height: '70vh', display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 0, p: 0 }}>
        <Paper elevation={3} sx={{ width: '100vw', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', p: 0, m: 0, borderRadius: 0 }}>
          <Typography variant="h5" gutterBottom align="center">1D Quantum Simulator</Typography>
          <Box sx={{ width: '100vw', height: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 0, m: 0 }}>
            {plotData ? (
              <Plot
                data={[
                  {
                    x: plotData.x,
                    y: plotData.psi_t[frame].map(v => Math.abs(v) ** 2),
                    type: 'scatter',
                    mode: 'lines',
                    name: `t=${plotData.times[frame]}`
                  }
                ]}
                layout={{
                  title: '|ψ(x, t)|²',
                  xaxis: { title: 'x', showgrid: true, zeroline: true, gridcolor: '#e0e0e0', tickformat: '.2f' },
                  yaxis: { title: '|ψ(x, t)|²', showgrid: true, zeroline: true, gridcolor: '#e0e0e0', tickformat: '.2e' },
                  autosize: true,
                  margin: { l: 60, r: 30, t: 30, b: 60 },
                  width: window.innerWidth,
                  height: 0.6 * window.innerHeight,
                  dragmode: 'pan',
                  hovermode: 'closest',
                  uirevision: 'static',
                }}
                config={{
                  responsive: true,
                  displayModeBar: true,
                  scrollZoom: true,
                  doubleClick: 'reset',
                  displaylogo: false,
                  toImageButtonOptions: { format: 'png', filename: 'quantum1d', height: 500, width: 800, scale: 2 }
                }}
                style={{ width: '100vw', height: '100%' }}
              />
            ) : (
              <Box sx={{ width: '100vw', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#f5f5f5', borderRadius: 2 }}>
                <Typography variant="h6" color="textSecondary">Run a simulation to see the plot</Typography>
              </Box>
            )}
          </Box>
          {plotData && plotData.times.length > 1 && (
            <Box sx={{ width: '100%', maxWidth: 700, mt: 2 }}>
              <input
                type="range"
                min={0}
                max={plotData.times.length - 1}
                value={frame}
                onChange={e => handleFrameChange(e, e.target.value)}
                style={{ width: '100%' }}
              />
              <Typography align="center">t = {plotData.times[frame]}</Typography>
            </Box>
          )}
        </Paper>
      </Box>
      <Paper elevation={3} sx={{ width: '100vw', p: 4, mt: 0, borderRadius: 0 }}>
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mb: 2 }}>
          <TextField label="x min" type="number" value={xmin} onChange={e => setXmin(Number(e.target.value))} fullWidth />
          <TextField label="x max" type="number" value={xmax} onChange={e => setXmax(Number(e.target.value))} fullWidth />
          <TextField label="# grid points" type="number" value={numPoints} onChange={e => setNumPoints(Number(e.target.value))} fullWidth />
        </Stack>
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mb: 2 }}>
          <TextField label="Potential (expr in x)" value={potentialExpr} onChange={e => setPotentialExpr(e.target.value)} fullWidth />
          <TextField label="Initial State (expr in x)" value={psi0Expr} onChange={e => setPsi0Expr(e.target.value)} fullWidth />
        </Stack>
        <TextField label="Times (comma-separated)" value={times} onChange={e => setTimes(e.target.value)} fullWidth sx={{ mb: 2 }} />
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Button variant="contained" onClick={handleRun} disabled={loading}>Run Simulation</Button>
        </Box>
        {loading && <Box sx={{ mt: 2, textAlign: 'center' }}><CircularProgress /></Box>}
        {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
      </Paper>
    </Box>
  );
};

export default Quantum1DPanel; 