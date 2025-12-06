import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    origen: 'Lima',
    destino: 'Ferreñafe',
    fecha_viaje: '',
    hora_salida: '22:00',
    tipo_servicio: 'normal',
    precio: '80'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    let nuevoPrecio = formData.precio;
    if (name === 'tipo_servicio') {
      if (value === 'normal') nuevoPrecio = '80';
      else if (value === 'vip') nuevoPrecio = '120';
      else if (value === 'premium') nuevoPrecio = '150';
    }
    
    setFormData(prev => ({
      ...prev,
      [name]: value,
      ...(name === 'tipo_servicio' && { precio: nuevoPrecio })
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.fecha_viaje) {
      alert('Por favor selecciona una fecha de viaje');
      return;
    }

    navigate('/asientos', {
      state: formData,
      replace: true
    });
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #2563eb, #1e40af)' }}>
      {/* Header */}
      <header style={{ background: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937' }}>
            🚌 VÍA PACÍFICO
          </h1>
          <button
            onClick={() => navigate('/admin')}
            style={{
              background: '#dc2626',
              color: 'white',
              padding: '12px 24px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '16px'
            }}
          >
            🔐 Panel Admin
          </button>
        </div>
      </header>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '80px 16px' }}>
        <div style={{ textAlign: 'center', color: 'white', marginBottom: '48px' }}>
          <h2 style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '16px' }}>
            Tu viaje comienza aquí
          </h2>
          <p style={{ fontSize: '20px', opacity: 0.9 }}>
            Lima - Ferreñafe | Viajes seguros y confortables
          </p>
        </div>

        <div style={{ 
          maxWidth: '900px', 
          margin: '0 auto', 
          background: 'white', 
          borderRadius: '16px', 
          boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
          padding: '32px'
        }}>
          <h3 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '24px' }}>
            Busca tu pasaje
          </h3>
          
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px', marginBottom: '24px' }}>
              
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  📍 Origen
                </label>
                <select
                  name="origen"
                  value={formData.origen}
                  onChange={handleChange}
                  style={{ width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '8px', fontSize: '16px' }}
                  required
                >
                  <option value="Lima">Lima</option>
                  <option value="Chiclayo">Chiclayo</option>
                  <option value="Ferreñafe">Ferreñafe</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  📍 Destino
                </label>
                <select
                  name="destino"
                  value={formData.destino}
                  onChange={handleChange}
                  style={{ width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '8px', fontSize: '16px' }}
                  required
                >
                  <option value="Lima">Lima</option>
                  <option value="Chiclayo">Chiclayo</option>
                  <option value="Ferreñafe">Ferreñafe</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  📅 Fecha de viaje
                </label>
                <input
                  type="date"
                  name="fecha_viaje"
                  value={formData.fecha_viaje}
                  onChange={handleChange}
                  min={new Date().toISOString().split('T')[0]}
                  style={{ width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '8px', fontSize: '16px' }}
                  required
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                  🕐 Horario
                </label>
                <select
                  name="hora_salida"
                  value={formData.hora_salida}
                  onChange={handleChange}
                  style={{ width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '8px', fontSize: '16px' }}
                  required
                >
                  <option value="08:00">08:00 AM</option>
                  <option value="14:00">02:00 PM</option>
                  <option value="22:00">10:00 PM</option>
                </select>
              </div>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '500', marginBottom: '8px' }}>
                🚌 Tipo de Servicio
              </label>
              <select
                name="tipo_servicio"
                value={formData.tipo_servicio}
                onChange={handleChange}
                style={{ width: '100%', padding: '12px', border: '1px solid #d1d5db', borderRadius: '8px', fontSize: '16px' }}
                required
              >
                <option value="normal">Normal - S/ 80</option>
                <option value="vip">VIP - S/ 120</option>
                <option value="premium">Premium - S/ 150</option>
              </select>
            </div>

            <button
              type="submit"
              style={{ 
                width: '100%', 
                background: '#2563eb', 
                color: 'white', 
                padding: '16px', 
                borderRadius: '8px',
                fontSize: '18px',
                fontWeight: '600',
                border: 'none',
                cursor: 'pointer'
              }}
            >
              Buscar Pasajes
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}