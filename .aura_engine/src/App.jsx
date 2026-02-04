import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import About from './pages/About';
import Demo from './pages/Demo';
import Demofull from './pages/Demofull';
import Example from './pages/Example';
import Good from './pages/Good';
import Newapp from './pages/Newapp';
import Test from './pages/Test';
import Testnl from './pages/Testnl';
import Testthen from './pages/Testthen';

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<About />} />
<Route path="/demo" element={<Demo />} />
<Route path="/demo_full" element={<Demofull />} />
<Route path="/example" element={<Example />} />
<Route path="/good" element={<Good />} />
<Route path="/new_app" element={<Newapp />} />
<Route path="/test" element={<Test />} />
<Route path="/test_nl" element={<Testnl />} />
<Route path="/test_then" element={<Testthen />} />
        <Route path="*" element={<About />} />
      </Routes>
    </>
  );
}
