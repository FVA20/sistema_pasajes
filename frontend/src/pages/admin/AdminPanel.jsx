import { useNavigate } from 'react-router-dom';
import { Users, FileText, DollarSign, Armchair, Search, ArrowLeft } from 'lucide-react';

export default function AdminPanel() {
  const navigate = useNavigate();

  const menuItems = [
    {
      title: 'Lista de Pasajeros',
      description: 'Ver todos los pasajeros registrados',
      icon: <Users className="w-12 h-12" />,
      path: '/admin/pasajeros',
      color: '#3b82f6'
    },
    {
      title: 'Buscar por DNI',
      description: 'Buscar información completa de un pasajero',
      icon: <Search className="w-12 h-12" />,
      path: '/admin/buscar-dni',
      color: '#8b5cf6'
    },
    {
      title: 'Lista de Pasajes',
      description: 'Ver todos los pasajes vendidos',
      icon: <FileText className="w-12 h-12" />,
      path: '/admin/pasajes',
      color: '#10b981'
    },
    {
      title: 'Visualizar Asientos',
      description: 'Ver qué pasajero compró cada asiento',
      icon: <Armchair className="w-12 h-12" />,
      path: '/admin/asientos',
      color: '#f59e0b'
    },
    {
      title: 'Reportes',
      description: 'Reportes diarios, mensuales y anuales',
      icon: <DollarSign className="w-12 h-12" />,
      path: '/admin/reportes',
      color: '#ef4444'
    }
  ];

  return (
    <div style={{ minHeight: '100vh', background: '#f3f4f6' }}>
      {/* Header */}
      <header style={{ background: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)', marginBottom: '32px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px' }}>
          <button
            onClick={() => navigate('/')}
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
            Volver al inicio
          </button>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1f2937' }}>
            🔐 Panel de Administración
          </h1>
          <p style={{ color: '#6b7280', marginTop: '8px' }}>
            Gestiona pasajeros, pasajes y reportes del sistema
          </p>
        </div>
      </header>

      {/* Menu Grid */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
          {menuItems.map((item, index) => (
            <div
              key={index}
              onClick={() => navigate(item.path)}
              style={{
                background: 'white',
                borderRadius: '12px',
                padding: '32px',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                cursor: 'pointer',
                transition: 'all 0.3s',
                border: '2px solid transparent'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 8px 12px rgba(0,0,0,0.15)';
                e.currentTarget.style.borderColor = item.color;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
                e.currentTarget.style.borderColor = 'transparent';
              }}
            >
              <div style={{ color: item.color, marginBottom: '16px' }}>
                {item.icon}
              </div>
              <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '8px', color: '#1f2937' }}>
                {item.title}
              </h3>
              <p style={{ color: '#6b7280', fontSize: '14px' }}>
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}