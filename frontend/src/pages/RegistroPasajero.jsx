import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { User, Mail, Phone, CreditCard, ArrowLeft } from 'lucide-react';

export default function RegistroPasajero() {
  const navigate = useNavigate();
  const location = useLocation();
  const { asiento, fecha_viaje, hora_salida, origen, destino, tipo_servicio, precio } = location.state || {};

  const [formData, setFormData] = useState({
    tipo_documento: 'DNI',
    numero_documento: '',
    nombres: '',
    apellidos: '',
    email: '',
    telefono: ''
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // 1. Registrar pasajero
      const pasajeroResponse = await fetch('http://localhost:8000/pasajeros/api/pasajeros/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      const pasajeroData = await pasajeroResponse.json();

      if (!pasajeroResponse.ok) {
        throw new Error(pasajeroData.error || 'Error al registrar pasajero');
      }

      // 2. Crear pasaje
      const pasajeData = {
        pasajero: pasajeroData.id,
        fecha_viaje: fecha_viaje,
        hora_salida: hora_salida,
        origen: origen,
        destino: destino,
        numero_asiento: asiento.numero,
        tipo_servicio: tipo_servicio,
        precio: precio,
        estado: 'vendido'
      };

      const pasajeResponse = await fetch('http://localhost:8000/pasajes/api/pasajes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(pasajeData)
      });

      const pasajeResult = await pasajeResponse.json();

      if (!pasajeResponse.ok) {
        throw new Error(pasajeResult.error || 'Error al crear pasaje');
      }

      // 3. Navegar a confirmación
      navigate('/confirmacion', {
        state: {
          pasajero: pasajeroData,
          pasaje: pasajeResult,
          asiento: asiento
        }
      });

    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (!asiento) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">No hay asiento seleccionado</h2>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Volver al inicio
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Datos del Pasajero</h1>
          <p className="text-gray-600 mt-2">Completa tus datos para confirmar la compra</p>
        </div>

        {/* Resumen del viaje */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-900 mb-2">Resumen de tu viaje</h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
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
              <p className="text-blue-700">💺 Asiento:</p>
              <p className="font-medium">#{asiento.numero}</p>
            </div>
            <div>
              <p className="text-blue-700">🎫 Servicio:</p>
              <p className="font-medium">{tipo_servicio}</p>
            </div>
            <div>
              <p className="text-blue-700">💰 Precio:</p>
              <p className="font-medium text-lg text-blue-900">S/ {precio}</p>
            </div>
          </div>
        </div>

        {/* Formulario */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
          <div className="space-y-4">
            {/* Tipo de documento */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <CreditCard className="w-4 h-4 inline mr-2" />
                Tipo de Documento
              </label>
              <select
                name="tipo_documento"
                value={formData.tipo_documento}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="DNI">DNI</option>
                <option value="Carnet de Extranjería">Carnet de Extranjería</option>
                <option value="Pasaporte">Pasaporte</option>
              </select>
            </div>

            {/* Número de documento */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Número de Documento
              </label>
              <input
                type="text"
                name="numero_documento"
                value={formData.numero_documento}
                onChange={handleChange}
                placeholder="Ej: 12345678"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                maxLength={formData.tipo_documento === 'DNI' ? 8 : 20}
              />
            </div>

            {/* Nombres */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <User className="w-4 h-4 inline mr-2" />
                Nombres
              </label>
              <input
                type="text"
                name="nombres"
                value={formData.nombres}
                onChange={handleChange}
                placeholder="Ej: Juan Carlos"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Apellidos */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Apellidos
              </label>
              <input
                type="text"
                name="apellidos"
                value={formData.apellidos}
                onChange={handleChange}
                placeholder="Ej: Pérez García"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Mail className="w-4 h-4 inline mr-2" />
                Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="ejemplo@correo.com"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Teléfono */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Phone className="w-4 h-4 inline mr-2" />
                Teléfono
              </label>
              <input
                type="tel"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                placeholder="987654321"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
                maxLength={9}
              />
            </div>
          </div>

          {/* Botones */}
          <div className="flex gap-4 mt-6">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Procesando...' : 'Confirmar Compra'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}