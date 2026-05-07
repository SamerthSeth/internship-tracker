import { useEffect, useState } from 'react';
import api from '../services/api';
import Card from '../components/Card';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_certificates: 0,
    active_internships: 0,
    expired_certificates: 0,
    upcoming_deadlines: 0
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/dashboard/stats');
        setStats(response.data);
      } catch {
        toast.error('Failed to fetch dashboard stats');
      }
    };
    fetchStats();
  }, []);

  return (
    <div>
      <div className="mb-xl flex justify-between items-end">
        <div>
          <h2 className="font-h1 text-h1 font-bold text-on-surface tracking-tight">Performance Dashboard</h2>
          <p className="font-body-base text-body-base text-on-surface-variant">Review your progress and manage ongoing internship applications.</p>
        </div>
      </div>

      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-lg mb-xl">
        <Card 
          title="Total Certificates" 
          value={stats.total_certificates} 
          icon="workspace_premium" 
          colorClass="bg-primary-fixed text-primary" 
        />
        <Card 
          title="Active Internships" 
          value={stats.active_internships} 
          icon="business_center" 
          colorClass="bg-secondary-fixed text-secondary" 
        />
        <Card 
          title="Upcoming Deadlines" 
          value={stats.upcoming_deadlines} 
          icon="event_busy" 
          colorClass="bg-error-container text-error" 
        />
        <Card 
          title="Expired Certificates" 
          value={stats.expired_certificates} 
          icon="warning" 
          colorClass="bg-tertiary-fixed text-tertiary" 
        />
      </section>
    </div>
  );
};

export default Dashboard;
