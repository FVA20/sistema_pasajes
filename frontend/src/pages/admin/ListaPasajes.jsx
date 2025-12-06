import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, FileText } from 'lucide-react';

export default function ListaPasajes() {
  const navigate = useNavigate();
  const [pasajes, setPasajes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    cargarPasajes();
  }, []);

  const cargarPasajes = async () => {
    try {
      const response = await fetch('http://localhost:8000/pasajes/api/admin/pasajes/');
      const data = await response.json();

      if (data.success) {
        setPasajes(data.pasajes);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al cargar los pasajes');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f3f4f6' }}>
      <header style={{ background: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '32px' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '16px' }}>
          <button
            onClick={() => navigate('/admin')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: 'none',
              border: 'none',
              color: '#6b7280',
              cursor: 'pointer',
              fontSize: '16px',
              marginBottom: '8px'
            }}
          >
            <ArrowLeft className="w-5 h-5" />
            Volver al panel
          </button>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1f2937' }}>
            📋 Lista de Pasajes Vendidos
          </h1>
        </div>
      </header>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 16px' }}>
        <div style={{ background: 'white', borderRadius: '12px', overflow: 'hidden' }}>
          {loading ? (
            <div style={{ padding: '48px', textAlign: 'center' }}>
              <p>Cargando pasajes...</p>
            </div>
          ) : pasajes.length === 0 ? (
            <div style={{ padding: '48px', textAlign: 'center' }}>
              <FileText className="w-16 h-16" style={{ margin: '0 auto', color: '#d1d5db' }} />
              <p style={{ color: '#6b7280', marginTop: '16px' }}>No hay pasajes registrados</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Código</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Pasajero</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>DNI</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Ruta</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Fecha Viaje</th>
                    <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Asiento</th>
                    <th style={{ padding: '16px', textAlign: 'right', fontWeight: '600' }}>Precio</th>
                    <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {pasajes.map((pasaje, index) => (
                    <tr
                      key={pasaje.id}
                      style={{
                        borderBottom: '1px solid #e5e7eb',
                        background: index % 2 === 0 ? 'white' : '#f9fafb'
                      }}
                    >
                      <td style={{ padding: '16px' }}>{pasaje.codigo_ticket}</td>
                      <td style={{ padding: '16px' }}>
                        {pasaje.pasajero.nombres} {pasaje.pasajero.apellidos}
                      </td>
                      <td style={{ padding: '16px' }}>{pasaje.pasajero.dni}</td>
                      <td style={{ padding: '16px' }}>
                        {pasaje.origen} → {pasaje.destino}
                      </td>
                      <td style={{ padding: '16px' }}>{pasaje.fecha_viaje}</td>
                      <td style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>
                        {pasaje.numero_asiento}
                      </td>
                      <td style={{ padding: '16px', textAlign: 'right', fontWeight: '600' }}>
                        S/ {pasaje.precio}
                      </td>
                      <td style={{ padding: '16px', textAlign: 'center' }}>
                        <span style={{
                          padding: '6px 12px',
                          borderRadius: '12px',
                          fontSize: '13px',
                          fontWeight: '600',
                          background: pasaje.estado === 'vendido' ? '#dcfce7' : '#fee2e2',
                          color: pasaje.estado === 'vendido' ? '#166534' : '#991b1b'
                        }}>
                          {pasaje.estado}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div style={{ marginTop: '16px', textAlign: 'center', color: '#6b7280' }}>
          Total: {pasajes.length} pasajes
        </div>
      </div>
    </div>
  );
}