import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../services/api';

const Login = () => {
  const [email, setEmail] = useState('login@gmail.com');
  const [password, setPassword] = useState('123456');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // FastAPI expects form-data for OAuth2 login
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      localStorage.setItem('access_token', response.data.access_token);
      toast.success('Login successful!');
      navigate('/dashboard');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed. Check credentials.');
    }
  };

  return (
    <div className="bg-background min-h-screen flex items-center justify-center p-lg">
      <main className="w-full max-w-[440px] flex flex-col gap-lg">
        <header className="flex flex-col items-center text-center gap-xs">
          <div className="w-xl h-xl bg-primary-container rounded-xl flex items-center justify-center mb-sm">
            <span className="material-symbols-outlined text-on-primary-container" style={{ fontSize: '32px' }}>analytics</span>
          </div>
          <h1 className="font-h1 text-h1 text-on-surface tracking-tight">InternTrack Pro</h1>
          <p className="font-body-base text-body-base text-on-surface-variant">Manage your career trajectory with precision.</p>
        </header>

        <section className="bg-surface-container-lowest border border-outline-variant rounded-xl p-xl shadow-sm">
          <div className="flex flex-col gap-lg">
            <div className="grid grid-cols-2 gap-md">
              <button className="flex items-center justify-center gap-sm px-md py-sm border border-outline-variant rounded-lg font-body-sm text-body-sm text-on-surface hover:bg-surface-container-low transition-colors">
                Google
              </button>
              <button className="flex items-center justify-center gap-sm px-md py-sm border border-outline-variant rounded-lg font-body-sm text-body-sm text-on-surface hover:bg-surface-container-low transition-colors">
                GitHub
              </button>
            </div>

            <div className="relative flex items-center py-sm">
              <div className="flex-grow border-t border-outline-variant"></div>
              <span className="flex-shrink mx-md font-label-caps text-label-caps text-outline uppercase">Or continue with</span>
              <div className="flex-grow border-t border-outline-variant"></div>
            </div>

            <form className="flex flex-col gap-md" onSubmit={handleLogin}>
              <div className="flex flex-col gap-xs">
                <label className="font-label-caps text-label-caps text-on-surface-variant px-xs" htmlFor="email">Email Address</label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-md top-1/2 -translate-y-1/2 text-outline" style={{ fontSize: '20px' }}>mail</span>
                  <input 
                    className="w-full pl-3xl pr-md py-sm bg-surface border border-outline-variant rounded-lg font-body-base text-body-base focus:ring-2 focus:ring-primary-container focus:border-primary-container transition-all outline-none" 
                    id="email" 
                    placeholder="name@company.com" 
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="flex flex-col gap-xs">
                <div className="flex justify-between items-center px-xs">
                  <label className="font-label-caps text-label-caps text-on-surface-variant" htmlFor="password">Password</label>
                  <a className="font-label-caps text-label-caps text-primary hover:underline cursor-pointer">Forgot password?</a>
                </div>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-md top-1/2 -translate-y-1/2 text-outline" style={{ fontSize: '20px' }}>lock</span>
                  <input 
                    className="w-full pl-3xl pr-md py-sm bg-surface border border-outline-variant rounded-lg font-body-base text-body-base focus:ring-2 focus:ring-primary-container focus:border-primary-container transition-all outline-none" 
                    id="password" 
                    placeholder="••••••••" 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              <button className="w-full bg-primary-container text-on-primary-container font-h3 text-h3 py-md rounded-lg hover:opacity-90 active:scale-[0.98] transition-all flex items-center justify-center gap-sm mt-4" type="submit">
                Sign In
                <span className="material-symbols-outlined">arrow_forward</span>
              </button>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Login;
