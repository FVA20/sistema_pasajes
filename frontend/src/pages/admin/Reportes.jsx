import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, TrendingUp, Calendar, DollarSign } from 'lucide-react';

export default function Reportes() {
  const navigate = useNavigate();
  const [tipoReporte, setTipoReporte] = useState('diario');
  const [fecha, setFecha] = useState('');
  const [mes, setMes] = useState('');
  const [anio, setAnio] = useState('');
  const [reporte, setReporte] = useState(null);
  const [loading, setLoading] = useState(false);

  const generarReporte = async () => {
    setLoading(true);

    try {
      let url = '';

      if (tipoReporte === 'diario') {
        if (!fecha) {
          alert('Por favor selecciona una fecha');
          setLoading(false);
          return;
        }
        url = `http://localhost:8000/pasajes/api/admin/reporte-diario/?fecha=${fecha}`;
      } else if (tipoReporte === 'mensual') {
        if (!mes) {
          alert('Por favor selecciona un mes');
          setLoading(false);
          return;
        }
        url = `http://localhost:8000/pasajes/api/admin/reporte-mensual/?mes=${mes}`;
      } else if (tipoReporte === 'anual') {
        if (!anio) {
          alert('Por favor ingresa un año');
          setLoading(false);
          return;
        }
        url = `http://localhost:8000/pasajes/api/admin/reporte-anual/?anio=${anio}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      if (data.success) {
        setReporte(data);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al generar el reporte');
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
            📊 Reportes de Ventas
          </h1>
        </div>
      </header>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
        {/* Selector de tipo de reporte */}
        <div style={{ background: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
              Tipo de Reporte
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
              {['diario', 'mensual', 'anual'].map((tipo) => (
                <button
                  key={tipo}
                  onClick={() => {
                    setTipoReporte(tipo);
                    setReporte(null);
                  }}
                  style={{
                    padding: '12px',
                    border: tipoReporte === tipo ? '2px solid #ef4444' : '2px solid #e5e7eb',
                    background: tipoReporte === tipo ? '#fef2f2' : 'white',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontWeight: '600',
                    fontSize: '16px',
                    color: tipoReporte === tipo ? '#ef4444' : '#6b7280'
                  }}
                >
                  {tipo.charAt(0).toUpperCase() + tipo.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Filtros según tipo */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
            {tipoReporte === 'diario' && (
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
            )}

            {tipoReporte === 'mensual' && (
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  📅 Mes
                </label>
                <input
                  type="month"
                  value={mes}
                  onChange={(e) => setMes(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '8px',
                    fontSize: '16px'
                  }}
                />
              </div>
            )}

            {tipoReporte === 'anual' && (
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  📅 Año
                </label>
                <input
                  type="number"
                  value={anio}
                  onChange={(e) => setAnio(e.target.value)}
                  placeholder="2025"
                  min="2020"
                  max="2030"
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '1px solid #d1d5db',
                    borderRadius: '8px',
                    fontSize: '16px'
                  }}
                />
              </div>
            )}

            <div style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button
                onClick={generarReporte}
                disabled={loading}
                style={{
                  width: '100%',
                  background: '#ef4444',
                  color: 'white',
                  padding: '12px',
                  borderRadius: '8px',
                  border: 'none',
                  cursor: loading ? 'not-allowed' : 'pointer',
                  fontSize: '16px',
                  fontWeight: '600'
                }}
              >
                {loading ? 'Generando...' : 'Generar Reporte'}
              </button>
            </div>
          </div>
        </div>

        {/* Resultados */}
        {reporte && (
          <div>
            {/* Resumen */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px', marginBottom: '24px' }}>
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                  <TrendingUp className="w-8 h-8" style={{ color: '#ef4444' }} />
                  <h3 style={{ fontSize: '16px', color: '#6b7280' }}>Total Vendidos</h3>
                </div>
                <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#1f2937' }}>
                  {reporte.resumen.total_vendidos}
                </p>
              </div>

              <div style={{ background: 'white', padding: '24px', borderRadius: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                  <DollarSign className="w-8 h-8" style={{ color: '#10b981' }} />
                  <h3 style={{ fontSize: '16px', color: '#6b7280' }}>Total Recaudado</h3>
                </div>
                <p style={{ fontSize: '36px', fontWeight: 'bold', color: '#1f2937' }}>
                  S/ {reporte.resumen.total_recaudado}
                </p>
              </div>
            </div>

            {/* Detalle por ruta (diario) */}
            {tipoReporte === 'diario' && reporte.por_ruta && reporte.por_ruta.length > 0 && (
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
                  Ventas por Ruta
                </h3>
                <div style={{ display: 'grid', gap: '12px' }}>
                  {reporte.por_ruta.map((ruta, index) => (
                    <div
                      key={index}
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: '16px',
                        background: '#f9fafb',
                        borderRadius: '8px'
                      }}
                    >
                      <div>
                        <p style={{ fontWeight: '600', fontSize: '16px' }}>{ruta.ruta}</p>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>{ruta.cantidad} pasajes</p>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <p style={{ fontWeight: 'bold', fontSize: '18px', color: '#10b981' }}>
                          S/ {ruta.total}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Detalle por día (mensual) */}
            {tipoReporte === 'mensual' && reporte.por_dia && reporte.por_dia.length > 0 && (
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px' }}>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
                  Ventas por Día
                </h3>
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Fecha</th>
                        <th style={{ padding: '12px', textAlign: 'center' }}>Cantidad</th>
                        <th style={{ padding: '12px', textAlign: 'right' }}>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reporte.por_dia.map((dia, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid #e5e7eb' }}>
                          <td style={{ padding: '12px' }}>{dia.fecha}</td>
                          <td style={{ padding: '12px', textAlign: 'center' }}>{dia.cantidad}</td>
                          <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>
                            S/ {dia.total}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Detalle por mes (anual) */}
            {tipoReporte === 'anual' && reporte.por_mes && reporte.por_mes.length > 0 && (
              <div style={{ background: 'white', padding: '24px', borderRadius: '12px' }}>
                <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>
                  Ventas por Mes
                </h3>
                <div style={{ overflowX: 'auto' }}>
                  <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                      <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                        <th style={{ padding: '12px', textAlign: 'left' }}>Mes</th>
                        <th style={{ padding: '12px', textAlign: 'center' }}>Cantidad</th>
                        <th style={{ padding: '12px', textAlign: 'right' }}>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reporte.por_mes.map((mes, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid #e5e7eb' }}>
                          <td style={{ padding: '12px' }}>{mes.mes}</td>
                          <td style={{ padding: '12px', textAlign: 'center' }}>{mes.cantidad}</td>
                          <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600' }}>
                            S/ {mes.total}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}