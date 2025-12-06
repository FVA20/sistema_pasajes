import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Search, Edit2, Trash2, Save, X } from 'lucide-react';

export default function ListaPasajeros() {
  const navigate = useNavigate();
  const [pasajeros, setPasajeros] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [loading, setLoading] = useState(true);
  const [editando, setEditando] = useState(null);
  const [formEdit, setFormEdit] = useState({});

  useEffect(() => {
    cargarPasajeros();
  }, []);

  const cargarPasajeros = async () => {
    try {
      const response = await fetch(`http://localhost:8000/pasajes/api/admin/pasajeros/`);
      const data = await response.json();
      
      if (data.success) {
        setPasajeros(data.pasajeros);
      }
    } catch (error) {
      console.error('Error al cargar pasajeros:', error);
      alert('Error al cargar la lista de pasajeros');
    } finally {
      setLoading(false);
    }
  };

  const buscarPasajeros = async () => {
    if (!busqueda.trim()) {
      cargarPasajeros();
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/pasajes/api/admin/pasajeros/?busqueda=${busqueda}`);
      const data = await response.json();
      
      if (data.success) {
        setPasajeros(data.pasajeros);
      }
    } catch (error) {
      console.error('Error al buscar:', error);
    }
  };

  const iniciarEdicion = (pasajero) => {
    setEditando(pasajero.id);
    setFormEdit({
      nombres: pasajero.nombres,
      apellidos: pasajero.apellidos,
      correo: pasajero.correo,
      telefono: pasajero.telefono
    });
  };

  const cancelarEdicion = () => {
    setEditando(null);
    setFormEdit({});
  };

  const guardarEdicion = async (pasajeroId) => {
    try {
      const response = await fetch('http://localhost:8000/pasajes/api/admin/editar-pasajero/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pasajero_id: pasajeroId,
          ...formEdit
        })
      });

      const data = await response.json();

      if (data.success) {
        alert(data.mensaje);
        setEditando(null);
        setFormEdit({});
        cargarPasajeros();
      } else {
        alert(data.error || 'Error al actualizar');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al guardar los cambios');
    }
  };

  const eliminarPasajero = async (pasajeroId, nombre) => {
    if (!confirm(`¿Estás seguro de eliminar al pasajero ${nombre}?`)) {
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/pasajes/api/admin/eliminar-pasajero/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pasajero_id: pasajeroId })
      });

      const data = await response.json();

      if (data.success) {
        alert(data.mensaje);
        cargarPasajeros();
      } else {
        alert(data.error || 'Error al eliminar');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al eliminar el pasajero');
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
            👥 Lista de Pasajeros
          </h1>
        </div>
      </header>

      <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 16px' }}>
        {/* Buscador */}
        <div style={{ background: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
          <div style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              placeholder="Buscar por DNI, nombres o apellidos..."
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && buscarPasajeros()}
              style={{
                flex: 1,
                padding: '12px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '16px'
              }}
            />
            <button
              onClick={buscarPasajeros}
              style={{
                background: '#3b82f6',
                color: 'white',
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Search className="w-5 h-5" />
              Buscar
            </button>
          </div>
        </div>

        {/* Tabla de pasajeros */}
        <div style={{ background: 'white', borderRadius: '12px', overflow: 'hidden' }}>
          {loading ? (
            <div style={{ padding: '48px', textAlign: 'center' }}>
              <p>Cargando pasajeros...</p>
            </div>
          ) : pasajeros.length === 0 ? (
            <div style={{ padding: '48px', textAlign: 'center' }}>
              <p style={{ color: '#6b7280' }}>No se encontraron pasajeros</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ background: '#f9fafb', borderBottom: '2px solid #e5e7eb' }}>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>DNI</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Nombres</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Apellidos</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Correo</th>
                    <th style={{ padding: '16px', textAlign: 'left', fontWeight: '600' }}>Teléfono</th>
                    <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Viajes</th>
                    <th style={{ padding: '16px', textAlign: 'center', fontWeight: '600' }}>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {pasajeros.map((pasajero, index) => (
                    <tr
                      key={pasajero.id}
                      style={{
                        borderBottom: '1px solid #e5e7eb',
                        background: index % 2 === 0 ? 'white' : '#f9fafb'
                      }}
                    >
                      <td style={{ padding: '16px' }}>{pasajero.dni}</td>
                      <td style={{ padding: '16px' }}>
                        {editando === pasajero.id ? (
                          <input
                            type="text"
                            value={formEdit.nombres}
                            onChange={(e) => setFormEdit({...formEdit, nombres: e.target.value})}
                            style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
                          />
                        ) : pasajero.nombres}
                      </td>
                      <td style={{ padding: '16px' }}>
                        {editando === pasajero.id ? (
                          <input
                            type="text"
                            value={formEdit.apellidos}
                            onChange={(e) => setFormEdit({...formEdit, apellidos: e.target.value})}
                            style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
                          />
                        ) : pasajero.apellidos}
                      </td>
                      <td style={{ padding: '16px' }}>
                        {editando === pasajero.id ? (
                          <input
                            type="email"
                            value={formEdit.correo}
                            onChange={(e) => setFormEdit({...formEdit, correo: e.target.value})}
                            style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
                          />
                        ) : pasajero.correo}
                      </td>
                      <td style={{ padding: '16px' }}>
                        {editando === pasajero.id ? (
                          <input
                            type="text"
                            value={formEdit.telefono}
                            onChange={(e) => setFormEdit({...formEdit, telefono: e.target.value})}
                            style={{ width: '100%', padding: '8px', border: '1px solid #d1d5db', borderRadius: '4px' }}
                          />
                        ) : pasajero.telefono}
                      </td>
                      <td style={{ padding: '16px', textAlign: 'center' }}>
                        <span style={{
                          background: '#dbeafe',
                          color: '#1e40af',
                          padding: '4px 12px',
                          borderRadius: '12px',
                          fontSize: '14px',
                          fontWeight: '600'
                        }}>
                          {pasajero.total_viajes}
                        </span>
                      </td>
                      <td style={{ padding: '16px' }}>
                        {editando === pasajero.id ? (
                          <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                            <button
                              onClick={() => guardarEdicion(pasajero.id)}
                              style={{
                                background: '#10b981',
                                color: 'white',
                                padding: '8px 12px',
                                borderRadius: '6px',
                                border: 'none',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                              }}
                            >
                              <Save className="w-4 h-4" />
                              Guardar
                            </button>
                            <button
                              onClick={cancelarEdicion}
                              style={{
                                background: '#6b7280',
                                color: 'white',
                                padding: '8px 12px',
                                borderRadius: '6px',
                                border: 'none',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                              }}
                            >
                              <X className="w-4 h-4" />
                              Cancelar
                            </button>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
                            <button
                              onClick={() => iniciarEdicion(pasajero)}
                              style={{
                                background: '#3b82f6',
                                color: 'white',
                                padding: '8px 12px',
                                borderRadius: '6px',
                                border: 'none',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                              }}
                            >
                              <Edit2 className="w-4 h-4" />
                              Editar
                            </button>
                            <button
                              onClick={() => eliminarPasajero(pasajero.id, `${pasajero.nombres} ${pasajero.apellidos}`)}
                              style={{
                                background: '#ef4444',
                                color: 'white',
                                padding: '8px 12px',
                                borderRadius: '6px',
                                border: 'none',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '4px'
                              }}
                            >
                              <Trash2 className="w-4 h-4" />
                              Eliminar
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div style={{ marginTop: '16px', textAlign: 'center', color: '#6b7280' }}>
          Total: {pasajeros.length} pasajeros
        </div>
      </div>
    </div>
  );
}