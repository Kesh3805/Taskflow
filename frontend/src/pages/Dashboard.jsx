import { useState, useEffect } from 'react';
import API from '../api/axios';
import ProjectCard from '../components/ProjectCard';
import { FiPlus, FiX } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchProjects = async () => {
    try {
      const res = await API.get('/projects');
      setProjects(res.data.projects);
    } catch (err) {
      console.error('Failed to fetch projects', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await API.post('/projects', { name, description });
      setName('');
      setDescription('');
      setShowForm(false);
      fetchProjects();
    } catch (err) {
      console.error('Failed to create project', err);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading projects...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Projects</h1>
          <p style={styles.subtitle}>{projects.length} project(s)</p>
        </div>
        {user?.role === 'ADMIN' && (
          <button onClick={() => setShowForm(!showForm)} style={styles.addBtn}>
            {showForm ? <FiX size={18} /> : <FiPlus size={18} />}
            {showForm ? 'Cancel' : 'New Project'}
          </button>
        )}
      </div>

      {/* Role Info Banner */}
      {user?.role === 'ADMIN' ? (
        <div style={styles.infoBanner}>
          <span style={styles.adminBadge}>ADMIN</span>
          <p style={styles.infoText}>
            As an admin, you can create projects, manage all resources, and have full access across the platform.
          </p>
        </div>
      ) : (
        <div style={styles.infoBannerMember}>
          <span style={styles.memberBadge}>MEMBER</span>
          <p style={styles.infoText}>
            You can create tasks, comment, and collaborate on projects you're a member of. Only admins can create new projects.
          </p>
        </div>
      )}

      {showForm && (
        <form onSubmit={handleCreate} style={styles.form}>
          <input
            type="text"
            placeholder="Project name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={styles.input}
            required
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.submitBtn}>Create Project</button>
        </form>
      )}

      {projects.length === 0 ? (
        <div style={styles.empty}>
          <p style={{ fontSize: '3rem', margin: 0 }}>📁</p>
          <p style={{ color: '#888' }}>No projects yet. Create your first project!</p>
        </div>
      ) : (
        <div style={styles.grid}>
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '2rem', maxWidth: '1200px', margin: '0 auto' },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
  },
  title: { margin: 0, fontSize: '1.8rem', color: '#1a1a2e' },
  subtitle: { margin: '0.3rem 0 0', color: '#888', fontSize: '0.9rem' },
  addBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
    padding: '0.6rem 1.2rem',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.9rem',
    fontWeight: '600',
    cursor: 'pointer',
  },
  form: {
    background: '#fff',
    padding: '1.5rem',
    borderRadius: '12px',
    marginBottom: '1.5rem',
    boxShadow: '0 2px 10px rgba(0,0,0,0.06)',
    display: 'flex',
    gap: '1rem',
    flexWrap: 'wrap',
  },
  input: {
    flex: '1 1 200px',
    padding: '0.7rem 0.9rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '0.95rem',
    outline: 'none',
  },
  submitBtn: {
    padding: '0.7rem 1.5rem',
    background: '#667eea',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '1.2rem',
  },
  empty: { textAlign: 'center', padding: '4rem 0' },
  loading: { textAlign: 'center', padding: '4rem 0', color: '#888' },
  infoBanner: {
    background: 'linear-gradient(135deg, #667eea15 0%, #764ba215 100%)',
    border: '1px solid #667eea40',
    borderRadius: '12px',
    padding: '1rem 1.5rem',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  infoBannerMember: {
    background: 'linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%)',
    border: '1px solid #f093fb40',
    borderRadius: '12px',
    padding: '1rem 1.5rem',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  adminBadge: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    padding: '0.4rem 1rem',
    borderRadius: '20px',
    fontSize: '0.75rem',
    fontWeight: '700',
    letterSpacing: '0.5px',
  },
  memberBadge: {
    background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    color: '#fff',
    padding: '0.4rem 1rem',
    borderRadius: '20px',
    fontSize: '0.75rem',
    fontWeight: '700',
    letterSpacing: '0.5px',
  },
  infoText: {
    margin: 0,
    fontSize: '0.9rem',
    color: '#555',
    lineHeight: '1.5',
  },
};
