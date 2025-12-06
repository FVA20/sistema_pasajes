import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { ArrowLeft, Users } from 'lucide-react';

export default function SeleccionAsientos() {
  const navigate = useNavigate();
  const location = useLocation();
  const { fecha_viaje, hora_salida, origen, destino, tipo_servicio, precio } = location.state || {};

  const [asientos, setAsientos] = useState({ piso1: [], piso2: [], total_asientos: 0, total_disponibles: 0, total_ocupados: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Validar datos
    if (!fecha_viaje || !hora_salida || !origen || !destino) {
      alert('Faltan datos del viaje');
      navigate('/');
      return;
    }

    cargarAsientos();
  }, [fecha_viaje, hora_salida, origen, destino]); // Dependencias específicas

  const cargarAsientos = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/pasajes/api/asientos/?fecha_viaje=${fecha_viaje}&hora_salida=${hora_salida}&origen=${origen}&destino=${destino}`
      );
      const data = await response.json();

      if (data.success) {
        setAsientos(data);
      } else {
        generarAsientosLocales();
      }
    } catch (error) {
      console.error('Error al cargar asientos:', error);
      generarAsientosLocales();
    } finally {
      setLoading(false);
    }
  };

  const generarAsientosLocales = () => {
    // Piso 1: del 1 al 10
    const piso1 = Array.from({ length: 10 }, (_, i) => ({
      id: i + 1,
      numero: i + 1,
      ocupado: false
    }));

    // Piso 2: del 11 al 30 (20 asientos)
    const piso2 = Array.from({ length: 20 }, (_, i) => ({
      id: i + 11,
      numero: i + 11,
      ocupado: Math.random() > 0.8
    }));

    setAsientos({
      success: true,
      piso1,
      piso2,
      total_asientos: 30,
      total_disponibles: piso1.filter(a => !a.ocupado).length + piso2.filter(a => !a.ocupado).length,
      total_ocupados: piso1.filter(a => a.ocupado).length + piso2.filter(a => a.ocupado).length
    });
  };

  // Función que navega DIRECTAMENTE al hacer clic
  const seleccionarAsiento = (asiento) => {
    if (!asiento || asiento.ocupado) return;
    
    // Ir directo al registro
    navigate('/registro', {
      state: {
        asiento: asiento,
        fecha_viaje: fecha_viaje,
        hora_salida: hora_salida,
        origen: origen,
        destino: destino,
        tipo_servicio: tipo_servicio,
        precio: precio
      }
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando asientos disponibles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Selecciona tu Asiento</h1>
          <p className="text-gray-600 mt-2">Haz clic en un asiento disponible para continuar</p>
        </div>

        {/* Información del viaje */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-900 mb-2">Resumen del viaje</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div>
              <p className="text-blue-700">📍 Ruta:</p>
              <p className="font-medium">{origen} → {destino}</p>
            </div>
            <div>
              <p className="text-blue-700">📅 Fecha:</p>
              <p className="font-medium">{fecha_viaje}</p>
            </div>
            <div>
              <p className="text-blue-700">🕐 Hora:</p>
              <p className="font-medium">{hora_salida}</p>
            </div>
            <div>
              <p className="text-blue-700">💰 Precio:</p>
              <p className="font-medium text-lg">S/ {precio}</p>
            </div>
          </div>
        </div>

        {/* Estadísticas */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Asientos</p>
                <p className="text-2xl font-bold text-gray-800">{asientos.total_asientos}</p>
              </div>
              <Users className="w-10 h-10 text-blue-500" />
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Disponibles</p>
                <p className="text-2xl font-bold text-green-600">{asientos.total_disponibles}</p>
              </div>
              <div className="w-10 h-10 bg-green-500 rounded-full"></div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Ocupados</p>
                <p className="text-2xl font-bold text-red-600">{asientos.total_ocupados}</p>
              </div>
              <div className="w-10 h-10 bg-red-500 rounded-full"></div>
            </div>
          </div>
        </div>

        {/* Leyenda */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <h3 className="font-semibold text-gray-700 mb-3">Leyenda:</h3>
          <div className="flex flex-wrap gap-6">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-green-500 rounded-lg"></div>
              <span className="text-sm text-gray-700">Disponible - Haz clic para seleccionar</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-red-500 rounded-lg"></div>
              <span className="text-sm text-gray-700">Ocupado</span>
            </div>
          </div>
        </div>

        {/* Mapa de asientos POR PISOS */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          {/* PISO 1 - Grid 4x3 (del 1 al 10) */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">Piso 1</h3>
            <div className="grid grid-cols-4 gap-3 max-w-md mx-auto">
              {asientos.piso1.map((asiento) => (
                <button
                  key={asiento.id}
                  onClick={() => seleccionarAsiento(asiento)}
                  disabled={asiento.ocupado}
                  className={`h-16 rounded-lg font-bold text-white transition-all ${
                    asiento.ocupado
                      ? 'bg-red-500 cursor-not-allowed opacity-50'
                      : 'bg-green-500 hover:bg-green-600 hover:scale-105 active:scale-95'
                  }`}
                >
                  {asiento.numero}
                </button>
              ))}
            </div>
          </div>

          {/* PISO 2 - Grid 4x5 (del 11 al 30) */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold text-gray-800 mb-4 text-center">Piso 2</h3>
            <div className="grid grid-cols-4 gap-3">
              {asientos.piso2.map((asiento) => (
                <button
                  key={asiento.id}
                  onClick={() => seleccionarAsiento(asiento)}
                  disabled={asiento.ocupado}
                  className={`h-16 rounded-lg font-bold text-white transition-all ${
                    asiento.ocupado
                      ? 'bg-red-500 cursor-not-allowed opacity-50'
                      : 'bg-green-500 hover:bg-green-600 hover:scale-105 active:scale-95'
                  }`}
                >
                  {asiento.numero}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}