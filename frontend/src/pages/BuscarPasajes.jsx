import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, Calendar, Clock, Bus } from 'lucide-react';

export default function BuscarPasajes() {
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
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validar que todos los campos estén llenos
    if (!formData.fecha_viaje) {
      alert('Por favor selecciona una fecha de viaje');
      return;
    }

    // Navegar a selección de asientos con los datos
    navigate('/asientos', {
      state: formData
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-gray-600 hover:text-gray-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Volver al inicio
          </button>
          <div className="flex items-center gap-3 mb-2">
            <Bus className="w-10 h-10 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-800">VÍA PACÍFICO</h1>
          </div>
          <p className="text-gray-600">Busca y reserva tu pasaje</p>
        </div>

        {/* Formulario de búsqueda */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Buscar Pasajes</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Origen */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="w-4 h-4 inline mr-2" />
                Origen
              </label>
              <select
                name="origen"
                value={formData.origen}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="Lima">Lima</option>
                <option value="Chiclayo">Chiclayo</option>
                <option value="Ferreñafe">Ferreñafe</option>
              </select>
            </div>

            {/* Destino */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <MapPin className="w-4 h-4 inline mr-2" />
                Destino
              </label>
              <select
                name="destino"
                value={formData.destino}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="Lima">Lima</option>
                <option value="Chiclayo">Chiclayo</option>
                <option value="Ferreñafe">Ferreñafe</option>
              </select>
            </div>

            {/* Fecha de viaje */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="w-4 h-4 inline mr-2" />
                Fecha de Viaje
              </label>
              <input
                type="date"
                name="fecha_viaje"
                value={formData.fecha_viaje}
                onChange={handleChange}
                min={new Date().toISOString().split('T')[0]}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            {/* Hora de salida */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Clock className="w-4 h-4 inline mr-2" />
                Hora de Salida
              </label>
              <select
                name="hora_salida"
                value={formData.hora_salida}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="08:00">08:00 AM</option>
                <option value="14:00">02:00 PM</option>
                <option value="22:00">10:00 PM</option>
              </select>
            </div>

            {/* Tipo de servicio */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Bus className="w-4 h-4 inline mr-2" />
                Tipo de Servicio
              </label>
              <select
                name="tipo_servicio"
                value={formData.tipo_servicio}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="normal">Normal - S/ 80</option>
                <option value="vip">VIP - S/ 120</option>
                <option value="premium">Premium - S/ 150</option>
              </select>
            </div>

            {/* Precio (oculto pero necesario) */}
            <input type="hidden" name="precio" value={formData.precio} />

            {/* Resumen */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
              <h3 className="font-semibold text-blue-900 mb-2">Resumen del viaje</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-blue-700">Ruta:</p>
                  <p className="font-medium">{formData.origen} → {formData.destino}</p>
                </div>
                <div>
                  <p className="text-blue-700">Fecha:</p>
                  <p className="font-medium">{formData.fecha_viaje || 'Selecciona una fecha'}</p>
                </div>
                <div>
                  <p className="text-blue-700">Hora:</p>
                  <p className="font-medium">{formData.hora_salida}</p>
                </div>
                <div>
                  <p className="text-blue-700">Precio:</p>
                  <p className="font-medium text-lg text-blue-900">S/ {formData.precio}</p>
                </div>
              </div>
            </div>

            {/* Botón de búsqueda */}
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Buscar Pasajes Disponibles
            </button>
          </form>
        </div>

        {/* Información adicional */}
        <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="font-semibold text-yellow-800 mb-2">ℹ️ Información importante:</h4>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• Los precios incluyen IGV</li>
            <li>• Puedes cancelar hasta 24 horas antes del viaje</li>
            <li>• Llega 15 minutos antes de la hora de salida</li>
            <li>• Presenta tu DNI al momento de abordar</li>
          </ul>
        </div>
      </div>
    </div>
  );
}