import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/');
  };

  return (
    <header className="bg-surface border-b border-outline-variant sticky top-0 z-40">
      <div className="flex justify-between items-center w-full px-lg h-[64px] max-w-[1440px] mx-auto">
        <div className="flex items-center flex-1">
          <div className="relative w-full max-w-md group">
            <span className="material-symbols-outlined absolute left-sm top-1/2 -translate-y-1/2 text-on-surface-variant group-focus-within:text-primary">
              search
            </span>
            <input
              type="text"
              placeholder="Search internships or documents..."
              className="bg-surface-container-low border-none rounded-xl pl-xl pr-md py-xs w-full font-body-sm text-body-sm focus:ring-2 focus:ring-primary transition-all text-on-surface outline-none"
            />
          </div>
        </div>
        <div className="flex items-center gap-md">
          <button className="p-sm text-on-surface-variant hover:text-primary transition-colors relative">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-2 right-2 w-2 h-2 bg-error rounded-full"></span>
          </button>
          <div className="flex items-center gap-sm pl-md border-l border-outline-variant">
            <div className="w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center font-bold text-sm">
              U
            </div>
            <span className="font-body-base text-body-base font-bold text-on-surface ml-2 mr-2">User</span>
            <button onClick={handleLogout} className="text-on-surface-variant hover:text-error transition-colors p-1" title="Logout">
              <span className="material-symbols-outlined">logout</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
