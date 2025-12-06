import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle, Download, Home } from 'lucide-react';

export default function Confirmacion() {
  const location = useLocation();
  const navigate = useNavigate();
  const { pasajero, pasaje, asiento } = location.state || {};

  if (!pasajero || !pasaje) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">No hay datos de confirmación</h2>
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

  const descargarTicket = async () => {
    try {
      const response = await fetch(`http://localhost:8000/pasajes/${pasaje.id}/ticket/`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ticket_${pasaje.codigo_pasaje}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      alert('Error al descargar el ticket');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        {/* Mensaje de éxito */}
        <div className="text-center mb-8">
          <CheckCircle className="w-20 h-20 text-green-500 mx-auto mb-4" />
          <h1 className="text-4xl font-bold text-gray-800 mb-2">¡Compra Exitosa!</h1>
          <p className="text-gray-600">Tu pasaje ha sido registrado correctamente</p>
        </div>

        {/* Tarjeta de ticket */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-6">
          {/* Header del ticket */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6">
            <h2 className="text-2xl font-bold mb-2">VÍA PACÍFICO</h2>
            <p className="text-blue-100">Código: {pasaje.codigo_pasaje}</p>
          </div>

          {/* Contenido del ticket */}
          <div className="p-6 space-y-4">
            {/* Información del pasajero */}
            <div className="border-b pb-4">
              <h3 className="font-semibold text-gray-700 mb-3">👤 Pasajero</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-500">Nombres:</p>
                  <p className="font-medium">{pasajero.nombres} {pasajero.apellidos}</p>
                </div>
                <div>
                  <p className="text-gray-500">Documento:</p>
                  <p className="font-medium">{pasajero.tipo_documento}: {pasajero.numero_documento}</p>
                </div>
                <div>
                  <p className="text-gray-500">Email:</p>
                  <p className="font-medium">{pasajero.email}</p>
                </div>
                <div>
                  <p className="text-gray-500">Teléfono:</p>
                  <p className="font-medium">{pasajero.telefono}</p>
                </div>
              </div>
            </div>

            {/* Información del viaje */}
            <div className="border-b pb-4">
              <h3 className="font-semibold text-gray-700 mb-3">🚌 Detalles del Viaje</h3>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p className="text-gray-500">Ruta:</p>
                  <p className="font-medium">{pasaje.origen} → {pasaje.destino}</p>
                </div>
                <div>
                  <p className="text-gray-500">Fecha:</p>
                  <p className="font-medium">{pasaje.fecha_viaje}</p>
                </div>
                <div>
                  <p className="text-gray-500">Hora de Salida:</p>
                  <p className="font-medium">{pasaje.hora_salida}</p>
                </div>
                <div>
                  <p className="text-gray-500">Asiento:</p>
                  <p className="font-medium text-lg">#{pasaje.numero_asiento}</p>
                </div>
                <div>
                  <p className="text-gray-500">Servicio:</p>
                  <p className="font-medium">{pasaje.tipo_servicio}</p>
                </div>
                <div>
                  <p className="text-gray-500">Estado:</p>
                  <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                    {pasaje.estado}
                  </span>
                </div>
              </div>
            </div>

            {/* Precio total */}
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="flex justify-between items-center">
                <span className="text-gray-700 font-medium">Total Pagado:</span>
                <span className="text-3xl font-bold text-blue-600">S/ {pasaje.precio}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="flex gap-4">
          <button
            onClick={descargarTicket}
            className="flex-1 flex items-center justify-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="w-5 h-5" />
            Descargar Ticket PDF
          </button>
          <button
            onClick={() => navigate('/')}
            className="flex-1 flex items-center justify-center gap-2 bg-gray-600 text-white px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <Home className="w-5 h-5" />
            Volver al Inicio
          </button>
        </div>

        {/* Información adicional */}
        <div className="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h4 className="font-semibold text-yellow-800 mb-2">📋 Información Importante:</h4>
          <ul className="text-sm text-yellow-700 space-y-1">
            <li>• Presenta tu DNI y este ticket al momento de abordar</li>
            <li>• Llega 15 minutos antes de la hora de salida</li>
            <li>• El ticket ha sido enviado a tu correo electrónico</li>
            <li>• Puedes cancelar con 24 horas de anticipación</li>
          </ul>
        </div>
      </div>
    </div>
  );
}