import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import api from '../services/api';

const Internships = () => {
  const [internships, setInternships] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    company: '',
    role: '',
    status: 'APPLIED'
  });

  const fetchInternships = async () => {
    try {
      const response = await api.get('/internships');
      setInternships(response.data);
    } catch (error) {
      toast.error('Failed to fetch internships');
    }
  };

  useEffect(() => {
    fetchInternships();
  }, []);

  const handleAddEntry = async (e) => {
    e.preventDefault();
    try {
      await api.post('/internships', formData);
      toast.success('Internship added successfully');
      setIsModalOpen(false);
      setFormData({ company: '', role: '', status: 'APPLIED' });
      fetchInternships();
    } catch (error) {
      toast.error('Failed to add internship');
    }
  };

  return (
    <div>
      <div className="mb-xl flex justify-between items-end">
        <div>
          <h2 className="font-h1 text-h1 font-bold text-on-surface tracking-tight">Internship Tracker</h2>
          <p className="font-body-base text-body-base text-on-surface-variant">Manage your career journey with systematic precision.</p>
        </div>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="bg-primary text-on-primary px-md py-sm rounded-xl font-label-caps text-label-caps flex items-center gap-sm hover:opacity-90 transition-opacity shadow-sm"
        >
          <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>add</span>
          Add Entry
        </button>
      </div>

      <div className="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden">
        {internships.length === 0 ? (
           <div className="p-xl text-center text-on-surface-variant">No applications tracked yet. Add your first one!</div>
        ) : (
          <table className="w-full text-left">
            <thead className="bg-surface-container-low border-b border-outline-variant font-label-caps text-label-caps text-on-surface-variant uppercase tracking-widest">
              <tr>
                <th className="px-lg py-md">Company</th>
                <th className="px-lg py-md">Role</th>
                <th className="px-lg py-md">Date Applied</th>
                <th className="px-lg py-md">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-outline-variant">
              {internships.map(internship => (
                <tr key={internship.id} className="hover:bg-surface-container-low transition-colors cursor-pointer">
                  <td className="px-lg py-md">
                    <div className="flex items-center gap-md">
                      <div className="w-8 h-8 rounded bg-primary-fixed text-primary font-bold flex items-center justify-center">
                        {internship.company.charAt(0)}
                      </div>
                      <span className="font-bold text-on-surface">{internship.company}</span>
                    </div>
                  </td>
                  <td className="px-lg py-md font-body-sm text-body-sm text-on-surface">{internship.role}</td>
                  <td className="px-lg py-md font-body-sm text-body-sm text-on-surface">{internship.date_applied || 'N/A'}</td>
                  <td className="px-lg py-md">
                    <span className="bg-surface-container-high border border-outline-variant font-label-caps text-label-caps px-xs py-1 rounded text-on-surface uppercase tracking-widest">
                      {internship.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-lg">
          <div className="bg-surface border border-outline-variant rounded-xl p-xl w-full max-w-md shadow-lg">
            <h3 className="font-h2 text-h2 font-bold text-on-surface mb-lg">Add Internship</h3>
            <form onSubmit={handleAddEntry} className="flex flex-col gap-md">
              <div>
                <label className="block font-label-caps text-label-caps text-on-surface-variant mb-xs">Company</label>
                <input 
                  type="text" 
                  required
                  className="w-full px-md py-sm bg-surface-container-lowest border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary outline-none" 
                  value={formData.company}
                  onChange={e => setFormData({...formData, company: e.target.value})}
                />
              </div>
              <div>
                <label className="block font-label-caps text-label-caps text-on-surface-variant mb-xs">Role</label>
                <input 
                  type="text" 
                  required
                  className="w-full px-md py-sm bg-surface-container-lowest border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary outline-none" 
                  value={formData.role}
                  onChange={e => setFormData({...formData, role: e.target.value})}
                />
              </div>
              <div>
                <label className="block font-label-caps text-label-caps text-on-surface-variant mb-xs">Status</label>
                <select 
                  className="w-full px-md py-sm bg-surface-container-lowest border border-outline-variant rounded-lg focus:ring-2 focus:ring-primary outline-none text-on-surface"
                  value={formData.status}
                  onChange={e => setFormData({...formData, status: e.target.value})}
                >
                  <option value="APPLIED">Applied</option>
                  <option value="INTERVIEWING">Interviewing</option>
                  <option value="OFFER">Offer</option>
                  <option value="REJECTED">Rejected</option>
                </select>
              </div>
              <div className="flex gap-md mt-sm">
                <button 
                  type="button" 
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-sm border border-outline-variant rounded-lg text-on-surface hover:bg-surface-container-low transition-colors font-body-sm"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="flex-1 py-sm bg-primary text-on-primary rounded-lg hover:opacity-90 transition-opacity font-body-sm font-bold"
                >
                  Save Entry
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Internships;
