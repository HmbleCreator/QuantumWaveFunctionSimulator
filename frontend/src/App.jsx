import React, { useState } from 'react';
import Quantum1DPanel from './components/Quantum1DPanel';
import Quantum2DPanel from './components/Quantum2DPanel';

function App() {
  const [panel, setPanel] = useState('1d');

  return (
    <div style={{ width: '100vw', height: '100vh', overflow: 'hidden', background: '#f7f7f7' }}>
      <nav style={{ width: '100vw', background: '#222', color: '#fff', padding: '1rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <button onClick={() => setPanel('1d')} style={{ marginRight: 16, padding: '0.5rem 1.5rem', fontWeight: panel === '1d' ? 'bold' : 'normal', background: panel === '1d' ? '#444' : '#222', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>1D Simulator</button>
        <button onClick={() => setPanel('2d')} style={{ padding: '0.5rem 1.5rem', fontWeight: panel === '2d' ? 'bold' : 'normal', background: panel === '2d' ? '#444' : '#222', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>2D Simulator</button>
      </nav>
      <div style={{ width: '100vw', height: 'calc(100vh - 64px)', overflow: 'auto' }}>
        {panel === '1d' ? <Quantum1DPanel /> : <Quantum2DPanel />}
      </div>
    </div>
  );
}

export default App;
