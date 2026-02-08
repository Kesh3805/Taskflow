import { useNavigate } from 'react-router-dom';
import { FiFolder, FiUsers, FiCheckSquare } from 'react-icons/fi';

export default function ProjectCard({ project }) {
  const navigate = useNavigate();

  return (
    <div
      style={styles.card}
      onClick={() => navigate(`/projects/${project.id}`)}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = '0 8px 25px rgba(0,0,0,0.12)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0 2px 10px rgba(0,0,0,0.06)';
      }}
    >
      <div style={styles.header}>
        <FiFolder size={20} color="#667eea" />
        <h3 style={styles.title}>{project.name}</h3>
      </div>
      <p style={styles.description}>
        {project.description || 'No description'}
      </p>
      <div style={styles.footer}>
        <span style={styles.stat}>
          <FiCheckSquare size={14} /> {project.task_count} tasks
        </span>
        <span style={styles.stat}>
          <FiUsers size={14} /> {project.members?.length || 0} members
        </span>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: '#fff',
    borderRadius: '12px',
    padding: '1.5rem',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    boxShadow: '0 2px 10px rgba(0,0,0,0.06)',
    border: '1px solid #f0f0f0',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    marginBottom: '0.6rem',
  },
  title: {
    margin: 0,
    fontSize: '1.1rem',
    fontWeight: '600',
    color: '#1a1a2e',
  },
  description: {
    color: '#666',
    fontSize: '0.9rem',
    margin: '0 0 1rem 0',
    lineHeight: 1.4,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  footer: {
    display: 'flex',
    gap: '1rem',
    borderTop: '1px solid #f5f5f5',
    paddingTop: '0.8rem',
  },
  stat: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.3rem',
    fontSize: '0.8rem',
    color: '#888',
  },
};
