import { FiCalendar, FiUser, FiTrash2, FiMessageCircle } from 'react-icons/fi';
import LabelBadge from './LabelBadge';

const statusColors = {
  TODO: { bg: '#fff3e0', text: '#e65100', label: 'To Do' },
  IN_PROGRESS: { bg: '#e3f2fd', text: '#1565c0', label: 'In Progress' },
  DONE: { bg: '#e8f5e9', text: '#2e7d32', label: 'Done' },
};

const priorityColors = {
  LOW: { bg: '#f0f0f0', text: '#666' },
  MEDIUM: { bg: '#fff8e1', text: '#f9a825' },
  HIGH: { bg: '#fce4ec', text: '#c62828' },
};

export default function TaskCard({ task, onStatusChange, onDelete, onClick }) {
  const status = statusColors[task.status] || statusColors.TODO;
  const priority = priorityColors[task.priority] || priorityColors.MEDIUM;

  const nextStatus = {
    TODO: 'IN_PROGRESS',
    IN_PROGRESS: 'DONE',
    DONE: 'TODO',
  };

  return (
    <div style={styles.card} onClick={onClick}>
      <div style={styles.topRow}>
        <span
          style={{ ...styles.statusBadge, background: status.bg, color: status.text }}
          onClick={(e) => {
            e.stopPropagation();
            onStatusChange(task.id, nextStatus[task.status]);
          }}
          title="Click to change status"
        >
          {status.label}
        </span>
        <span style={{ ...styles.priorityBadge, background: priority.bg, color: priority.text }}>
          {task.priority}
        </span>
      </div>

      <h4 style={styles.title}>{task.title}</h4>
      {task.description && <p style={styles.desc}>{task.description}</p>}
      
      {task.labels && task.labels.length > 0 && (
        <div style={styles.labelsRow}>
          {task.labels.map((label) => (
            <LabelBadge key={label.id} label={label} />
          ))}
        </div>
      )}

      <div style={styles.footer}>
        <div style={styles.meta}>
          {task.assignee && (
            <span style={styles.metaItem}>
              <FiUser size={13} /> {task.assignee.name}
            </span>
          )}
          {task.due_date && (
            <span style={styles.metaItem}>
              <FiCalendar size={13} /> {task.due_date}
            </span>
          )}
          {task.comment_count > 0 && (
            <span style={styles.metaItem}>
              <FiMessageCircle size={13} /> {task.comment_count}
            </span>
          )}
        </div>
        <button 
          onClick={(e) => {
            e.stopPropagation();
            onDelete(task.id);
          }} 
          style={styles.deleteBtn} 
          title="Delete task"
        >
          <FiTrash2 size={14} />
        </button>
      </div>
    </div>
  );
}

const styles = {
  card: {
    background: '#fff',
    borderRadius: '10px',
    padding: '1rem 1.2rem',
    boxShadow: '0 1px 6px rgba(0,0,0,0.06)',
    border: '1px solid #f0f0f0',
    marginBottom: '0.8rem',
    cursor: 'pointer',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  topRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '0.6rem',
  },
  statusBadge: {
    padding: '3px 10px',
    borderRadius: '12px',
    fontSize: '0.72rem',
    fontWeight: '600',
    cursor: 'pointer',
    userSelect: 'none',
  },
  priorityBadge: {
    padding: '3px 10px',
    borderRadius: '12px',
    fontSize: '0.72rem',
    fontWeight: '600',
  },
  title: {
    margin: '0 0 0.3rem 0',
    fontSize: '0.95rem',
    fontWeight: '600',
    color: '#1a1a2e',
  },
  desc: {
    margin: '0 0 0.6rem 0',
    fontSize: '0.82rem',
    color: '#777',
    lineHeight: 1.4,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
  },
  labelsRow: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.4rem',
    marginBottom: '0.6rem',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  meta: {
    display: 'flex',
    gap: '0.8rem',
  },
  metaItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem',
    fontSize: '0.78rem',
    color: '#999',
  },
  deleteBtn: {
    background: 'none',
    border: 'none',
    color: '#ccc',
    cursor: 'pointer',
    padding: '4px',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
  },
};
