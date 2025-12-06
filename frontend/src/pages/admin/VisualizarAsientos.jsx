import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, Armchair } from 'lucide-react';

export default function VisualizarAsientos() {
  const navigate = useNavigate();
  const [fecha, setFecha] = useState('');
  const [hora, setHora] = useState('22:00');
  const [asientos, setAsientos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [info, setInfo] = useState(null);

  const buscarAsientos = async () => {
    if (!fecha) {
      alert('Por favor selecciona una fecha');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/pasajes/api/admin/visualizar-asientos/?fecha=${fecha}&hora=${hora}`
      );
      const data = await response.json();

      if (data.success) {
        setAsientos(data.asientos_ocupados);
        setInfo({
          fecha: data.fecha,
          hora: data.hora,
          ruta: data.ruta,
          total: data.total_ocupados
        });
      } else {
        alert(data.error || 'Error al cargar los asientos');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al cargar los asientos');
    } finally {
      setLoading(false);
    }
  };

  const formatearHora = (hora24) => {
    const [horas, minutos] = hora24.split(':');
    const h = parseInt(horas);
    const periodo = h >= 12 ? 'PM' : 'AM';
    const h12 = h % 12 || 12;
    return `${h12}:${minutos} ${periodo}`;
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
            💺 Visualizar Asientos Ocupados
          </h1>
        </div>
      </header>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
        {/* Filtros */}
        <div style={{ background: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                📅 Fecha
              </label>
              <input
                type="date"
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                🕐 Hora
              </label>
              <select
                value={hora}
                onChange={(e) => setHora(e.target.value)}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '16px'
                }}
              >
                <option value="08:00">08:00 AM</option>
                <option value="14:00">02:00 PM</option>
                <option value="22:00">10:00 PM</option>
              </select>
            </div>

            <div style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button
                onClick={buscarAsientos}
                disabled={loading}
                style={{
                  width: '100%',
                  background: '#f59e0b',
                  color: 'white',
                  padding: '12px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '8px',
                  fontSize: '16px',
                  fontWeight: '600',
                  opacity: loading ? 0.6 : 1
                }}
              >
                <Search className="w-5 h-5" />
                {loading ? 'Buscando...' : 'Buscar'}
              </button>
            </div>
          </div>
        </div>

        {/* Información del viaje */}
        {info && (
          <div style={{
            background: 'white',
            padding: '16px 24px',
            borderRadius: '12px',
            marginBottom: '24px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <p style={{ fontSize: '18px', fontWeight: 'bold' }}>
                {info.ruta} - {formatearHora(info.hora)}
              </p>
              <p style={{ color: '#6b7280' }}>Fecha: {info.fecha}</p>
            </div>
            <div style={{
              background: '#fef3c7',
              color: '#92400e',
              padding: '8px 16px',
              borderRadius: '8px',
              fontWeight: '600'
            }}>
              {info.total} asientos ocupados
            </div>
          </div>
        )}

        {/* Lista de asientos */}
        {asientos.length > 0 && (
          <div style={{ background: 'white', borderRadius: '12px', overflow: 'hidden' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                  <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Asiento</th>
                  <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Pasajero</th>
                  <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>DNI</th>
                  <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Teléfono</th>
                  <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Código Ticket</th>
                  <th style={{ padding: '16px', textAlign: 'right', fontWeight: '600' }}>Precio</th>
                  <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Estado</th>
                </tr>
              </thead>
              <tbody>
                {asientos.map((item, index) => (
                  <tr
                    key={index}
                    style={{
                      borderBottom: '1px solid #e5e7eb',
                      background: index % 2 === 0 ? 'white' : '#f9fafb'
                    }}
                  >
                    <td style={{ padding: '16px', textAlign: 'center' }}>
                      <div style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '48px',
                        height: '48px',
                        background: '#f59e0b',
                        color: 'white',
                        borderRadius: '8px',
                        fontWeight: 'bold',
                        fontSize: '18px'
                      }}>
                        {item.numero_asiento}
                      </div>
                    </td>
                    <td style={{ padding: '16px' }}>
                      {item.pasajero.nombres} {item.pasajero.apellidos}
                    </td>
                    <td style={{ padding: '16px' }}>{item.pasajero.dni}</td>
                    <td style={{ padding: '16px' }}>{item.pasajero.telefono}</td>
                    <td style={{ padding: '16px' }}>{item.codigo_ticket}</td>
                    <td style={{ padding: '16px', textAlign: 'right', fontWeight: '600' }}>
                      S/ {item.precio}
                    </td>
                    <td style={{ padding: '16px', textAlign: 'center' }}>
                      <span style={{
                        padding: '6px 12px',
                        borderRadius: '12px',
                        fontSize: '13px',
                        fontWeight: '600',
                        background: item.estado === 'vendido' ? '#dcfce7' : '#fef3c7',
                        color: item.estado === 'vendido' ? '#166534' : '#92400e'
                      }}>
                        {item.estado}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {asientos.length === 0 && info && (
          <div style={{
            background: 'white',
            padding: '48px',
            borderRadius: '12px',
            textAlign: 'center'
          }}>
            <Armchair className="w-16 h-16" style={{ margin: '0 auto', color: '#d1d5db' }} />
            <p style={{ color: '#6b7280', marginTop: '16px', fontSize: '18px' }}>
              No hay asientos ocupados para este viaje
            </p>
          </div>
        )}

        {!info && !loading && (
          <div style={{
            background: 'white',
            padding: '48px',
            borderRadius: '12px',
            textAlign: 'center'
          }}>
            <Search className="w-16 h-16" style={{ margin: '0 auto', color: '#d1d5db' }} />
            <p style={{ color: '#6b7280', marginTop: '16px', fontSize: '18px' }}>
              Selecciona una fecha y hora para buscar los asientos ocupados
            </p>
          </div>
        )}
      </div>
    </div>
  );
}