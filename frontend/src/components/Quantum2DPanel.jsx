import React, { useState, useRef, useEffect } from 'react';
import { Box, Paper, Typography, TextField, Button, Stack, CircularProgress, IconButton, Slider } from '@mui/material';
import { PlayArrow, Pause } from '@mui/icons-material';
import Plot from 'react-plotly.js';
import axios from 'axios';

const Quantum2DPanel = () => {
  const [xmin, setXmin] = useState(-1);
  const [xmax, setXmax] = useState(1);
  const [numX, setNumX] = useState(40);
  const [ymin, setYmin] = useState(-1);
  const [ymax, setYmax] = useState(1);
  const [numY, setNumY] = useState(40);
  const [potentialExpr, setPotentialExpr] = useState('0');
  const [psi0Expr, setPsi0Expr] = useState('exp(-10*((X+0.5)**2 + (Y+0.5)**2))');
  const [times, setTimes] = useState('0,0.01,0.02');
  const [loading, setLoading] = useState(false);
  const [plotData, setPlotData] = useState(null);
  const [error, setError] = useState('');
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (playing && plotData) {
      intervalRef.current = setInterval(() => {
        setFrame(prev => (prev + 1) % plotData.times.length);
      }, 400);
    } else {
      clearInterval(intervalRef.current);
    }
    return () => clearInterval(intervalRef.current);
  }, [playing, plotData]);

  const handleRun = async () => {
    setLoading(true);
    setError('');
    setPlotData(null);
    try {
      const timesArr = times.split(',').map(Number);
      const res = await axios.post('http://localhost:8000/solve/2d/timedependent', {
        xmin,
        xmax,
        num_x: numX,
        ymin,
        ymax,
        num_y: numY,
        potential_expr: potentialExpr,
        psi0_expr: psi0Expr,
        times: timesArr
      });
      setPlotData(res.data);
      setFrame(0);
      setPlaying(false);
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFrameChange = (e, value) => {
    setFrame(Number(value));
    setPlaying(false);
  };

  return (
    <Box sx={{ height: '100vh', width: '100vw', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', p: 0, m: 0 }}>
      <Box sx={{ width: '100vw', height: '70vh', display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 0, p: 0 }}>
        <Paper elevation={3} sx={{ width: '100vw', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', p: 0, m: 0, borderRadius: 0 }}>
          <Typography variant="h5" gutterBottom align="center">2D Quantum Simulator</Typography>
          <Box sx={{ width: '100vw', height: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center', p: 0, m: 0 }}>
            {plotData ? (
              <Plot
                data={[{
                  z: plotData.psi_t[frame],
                  x: plotData.X.map(row => row[0]),
                  y: plotData.Y[0],
                  type: 'heatmap',
                  colorscale: 'Viridis',
                  colorbar: { title: '|ψ|²' },
                  hoverongaps: false
                }]}
                layout={{
                  title: '|ψ(x, y, t)|²',
                  xaxis: { title: 'x', showgrid: true, zeroline: true, gridcolor: '#e0e0e0', tickformat: '.2f' },
                  yaxis: { title: 'y', showgrid: true, zeroline: true, gridcolor: '#e0e0e0', tickformat: '.2f' },
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
                  toImageButtonOptions: { format: 'png', filename: 'quantum2d', height: 500, width: 800, scale: 2 }
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
              <Stack direction="row" spacing={2} alignItems="center">
                <IconButton onClick={() => setPlaying(p => !p)} color="primary">
                  {playing ? <Pause /> : <PlayArrow />}
                </IconButton>
                <Slider
                  min={0}
                  max={plotData.times.length - 1}
                  value={frame}
                  onChange={handleFrameChange}
                  marks
                  step={1}
                  valueLabelDisplay="auto"
                  sx={{ flex: 1 }}
                />
                <Typography sx={{ minWidth: 80 }}>
                  t = {plotData.times[frame]}
                </Typography>
              </Stack>
            </Box>
          )}
        </Paper>
      </Box>
      <Paper elevation={3} sx={{ width: '100vw', p: 4, mt: 0, borderRadius: 0 }}>
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mb: 2 }}>
          <TextField label="x min" type="number" value={xmin} onChange={e => setXmin(Number(e.target.value))} fullWidth />
          <TextField label="x max" type="number" value={xmax} onChange={e => setXmax(Number(e.target.value))} fullWidth />
          <TextField label="# x grid points" type="number" value={numX} onChange={e => setNumX(Number(e.target.value))} fullWidth />
          <TextField label="y min" type="number" value={ymin} onChange={e => setYmin(Number(e.target.value))} fullWidth />
          <TextField label="y max" type="number" value={ymax} onChange={e => setYmax(Number(e.target.value))} fullWidth />
          <TextField label="# y grid points" type="number" value={numY} onChange={e => setNumY(Number(e.target.value))} fullWidth />
        </Stack>
        <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mb: 2 }}>
          <TextField label="Potential (expr in X,Y)" value={potentialExpr} onChange={e => setPotentialExpr(e.target.value)} fullWidth />
          <TextField label="Initial State (expr in X,Y)" value={psi0Expr} onChange={e => setPsi0Expr(e.target.value)} fullWidth />
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

export default Quantum2DPanel; 