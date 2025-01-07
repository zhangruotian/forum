import { Outlet } from 'react-router-dom';

export function AuthLayout() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <Outlet />
    </div>
  );
} 