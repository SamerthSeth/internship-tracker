import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Internships from './pages/Internships';

const ProtectedRoute = () => {
  const token = localStorage.getItem('access_token');
  if (!token) return <Navigate to="/" replace />;
  return <Outlet />;
};

const Layout = () => {
  return (
    <div className="flex bg-background min-h-screen text-on-surface">
      <Sidebar />
      <div className="flex-1 ml-[240px] flex flex-col">
        <Navbar />
        <main className="flex-1 p-3xl overflow-y-auto w-full max-w-[1440px] mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <>
      <Toaster position="top-right" toastOptions={{
        style: {
          background: '#272a32',
          color: '#e0e2ed',
          border: '1px solid #414754',
        }
      }}/>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          
          <Route element={<ProtectedRoute />}>
            <Route element={<Layout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/internships" element={<Internships />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
