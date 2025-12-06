import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, User } from 'lucide-react';

export default function BuscarDNI() {
  const navigate = useNavigate();
  const [dni, setDni] = useState('');
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const buscar = async () => {
    if (!dni.trim()) {
      setError('Por favor ingresa un DNI');
      return;
    }

    setLoading(true);
    setError('');
    setResultado(null);

    try {
      const response = await fetch(`http://localhost:8000/pasajes/api/admin/buscar-dni/?dni=${dni}`);
      const data = await response.json();

      if (data.success) {
        setResultado(data);
      } else {
        setError(data.error || 'No se encontró el pasajero');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Error al buscar el pasajero');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#f3f4f6' }}>
      <header style={{ background: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '32px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px' }}>
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
            🔍 Buscar por DNI
          </h1>
        </div>
      </header>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
        {/* Buscador */}
        <div style={{ background: 'white', padding: '32px', borderRadius: '12px', marginBottom: '24px' }}>
          <div style={{ display: 'flex', gap: '12px', maxWidth: '600px', margin: '0 auto' }}>
            <input
              type="text"
              placeholder="Ingrese el DNI del pasajero..."
              value={dni}
              onChange={(e) => setDni(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && buscar()}
              maxLength="8"
              style={{
                flex: 1,
                padding: '16px',
                border: '2px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '18px'
              }}
            />
            <button
              onClick={buscar}
              disabled={loading}
              style={{
                background: '#8b5cf6',
                color: 'white',
                padding: '16px 32px',
                borderRadius: '8px',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '16px',
                fontWeight: '600'
              }}
            >
              <Search className="w-5 h-5" />
              {loading ? 'Buscando...' : 'Buscar'}
            </button>
          </div>

          {error && (
            <div style={{
              marginTop: '16px',
              padding: '12px',
              background: '#fee2e2',
              color: '#991b1b',
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}
        </div>

        {/* Resultado */}
        {resultado && (
          <div>
            {/* Información del pasajero */}
            <div style={{ background: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
                <div style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: '50%',
                  background: '#8b5cf6',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <User className="w-8 h-8" />
                </div>
                <div>
                  <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '4px' }}>
                    {resultado.pasajero.nombres} {resultado.pasajero.apellidos}
                  </h2>
                  <p style={{ color: '#6b7280' }}>DNI: {resultado.pasajero.dni}</p>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
                <div>
                  <p style={{ color: '#6b7280', fontSize: '14px', marginBottom: '4px' }}>Correo</p>
                  <p style={{ fontWeight: '600' }}>{resultado.pasajero.correo}</p>
                </div>
                <div>
                  <p style={{ color: '#6b7280', fontSize: '14px', marginBottom: '4px' }}>Teléfono</p>
                  <p style={{ fontWeight: '600' }}>{resultado.pasajero.telefono}</p>
                </div>
              </div>
            </div>

            {/* Historial de pasajes */}
            <div style={{ background: 'white', padding: '24px', borderRadius: '12px' }}>
              <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
                📋 Historial de Pasajes ({resultado.total_pasajes})
              </h3>

              {resultado.pasajes.length === 0 ? (
                <p style={{ color: '#6b7280', textAlign: 'center', padding: '32px' }}>
                  Este pasajero no tiene pasajes registrados
                </p>
              ) : (
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                        <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px' }}>Código</th>
                        <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px' }}>Fecha Viaje</th>
                        <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px' }}>Ruta</th>
                        <th style={{ padding: '12px', textAlign: 'center', fontSize: '14px' }}>Asiento</th>
                        <th style={{ padding: '12px', textAlign: 'right', fontSize: '14px' }}>Precio</th>
                        <th style={{ padding: '12px', textAlign: 'center', fontSize: '14px' }}>Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {resultado.pasajes.map((pasaje, index) => (
                        <tr
                          key={pasaje.id}
                          style={{
                            borderBottom: '1px solid #e5e7eb',
                            background: index % 2 === 0 ? 'white' : '#f9fafb'
                          }}
                        >
                          <td style={{ padding: '12px', fontSize: '14px' }}>{pasaje.codigo_ticket}</td>
                          <td style={{ padding: '12px', fontSize: '14px' }}>{pasaje.fecha_viaje}</td>
                          <td style={{ padding: '12px', fontSize: '14px' }}>
                            {pasaje.origen} → {pasaje.destino}
                          </td>
                          <td style={{ padding: '12px', textAlign: 'center', fontSize: '14px', fontWeight: '600' }}>
                            {pasaje.numero_asiento}
                          </td>
                          <td style={{ padding: '12px', textAlign: 'right', fontSize: '14px', fontWeight: '600' }}>
                            S/ {pasaje.precio}
                          </td>
                          <td style={{ padding: '12px', textAlign: 'center' }}>
                            <span style={{
                              padding: '4px 12px',
                              borderRadius: '12px',
                              fontSize: '12px',
                              fontWeight: '600',
                              background: pasaje.estado === 'vendido' ? '#dcfce7' : pasaje.estado === 'anulado' ? '#fee2e2' : '#fef3c7',
                              color: pasaje.estado === 'vendido' ? '#166534' : pasaje.estado === 'anulado' ? '#991b1b' : '#92400e'
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
          </div>
        )}
      </div>
    </div>
  );
}