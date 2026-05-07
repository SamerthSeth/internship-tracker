import React from 'react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
  { path: '/internships', label: 'Internship Tracker', icon: 'assignment' }
];

const Sidebar = () => {
  return (
    <aside className="fixed left-0 top-0 h-full w-[240px] bg-surface border-r border-outline-variant flex flex-col gap-sm p-md z-50">
      <div className="mb-xl px-md mt-lg">
        <h1 className="font-h2 text-h2 font-black text-primary">InternTrack Pro</h1>
        <p className="font-label-caps text-label-caps text-on-surface-variant opacity-70 uppercase tracking-widest mt-1">
          Management Suite
        </p>
      </div>
      <nav className="flex flex-col gap-xs flex-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `px-md py-sm flex items-center gap-md rounded-xl transition-all duration-150 ${
                isActive
                  ? 'bg-surface-container-high text-primary font-bold'
                  : 'text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface'
              }`
            }
          >
            <span className="material-symbols-outlined">{item.icon}</span>
            <span className="font-label-caps text-label-caps tracking-wide">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
