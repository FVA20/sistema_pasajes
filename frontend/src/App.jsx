import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import SeleccionAsientos from './pages/SeleccionAsientos'
import RegistroPasajero from './pages/RegistroPasajero'
import Confirmacion from './pages/Confirmacion'

// Páginas de Admin
import AdminPanel from './pages/admin/AdminPanel'
import ListaPasajeros from './pages/admin/ListaPasajeros'
import BuscarDNI from './pages/admin/BuscarDNI'
import ListaPasajes from './pages/admin/ListaPasajes'
import VisualizarAsientos from './pages/admin/VisualizarAsientos'
import Reportes from './pages/admin/Reportes'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas de Ventas */}
        <Route path="/" element={<Home />} />
        <Route path="/asientos" element={<SeleccionAsientos />} />
        <Route path="/registro" element={<RegistroPasajero />} />
        <Route path="/confirmacion" element={<Confirmacion />} />
        
        {/* Rutas de Admin */}
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/admin/pasajeros" element={<ListaPasajeros />} />
        <Route path="/admin/buscar-dni" element={<BuscarDNI />} />
        <Route path="/admin/pasajes" element={<ListaPasajes />} />
        <Route path="/admin/asientos" element={<VisualizarAsientos />} />
        <Route path="/admin/reportes" element={<Reportes />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App