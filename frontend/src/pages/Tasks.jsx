import { useState, useEffect } from 'react';
import API from '../api/axios';
import TaskCard from '../components/TaskCard';

export default function Tasks() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState({ status: '', priority: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    API.get('/projects').then((res) => setProjects(res.data.projects));
  }, []);

  useEffect(() => {
    if (!selectedProject) {
      setTasks([]);
      return;
    }
    setLoading(true);
    const params = {};
    if (filter.status) params.status = filter.status;
    if (filter.priority) params.priority = filter.priority;
    API.get(`/tasks/project/${selectedProject}`, { params })
      .then((res) => setTasks(res.data.tasks))
      .finally(() => setLoading(false));
  }, [selectedProject, filter]);

  const handleStatusChange = async (taskId, newStatus) => {
    await API.put(`/tasks/${taskId}`, { status: newStatus });
    // Re-fetch
    const params = {};
    if (filter.status) params.status = filter.status;
    if (filter.priority) params.priority = filter.priority;
    const res = await API.get(`/tasks/project/${selectedProject}`, { params });
    setTasks(res.data.tasks);
  };

  const handleDelete = async (taskId) => {
    if (!window.confirm('Delete this task?')) return;
    await API.delete(`/tasks/${taskId}`);
    setTasks(tasks.filter((t) => t.id !== taskId));
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>All Tasks</h1>

      <div style={styles.filters}>
        <select
          value={selectedProject}
          onChange={(e) => setSelectedProject(e.target.value)}
          style={styles.select}
        >
          <option value="">Select a project</option>
          {projects.map((p) => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
        <select
          value={filter.status}
          onChange={(e) => setFilter({ ...filter, status: e.target.value })}
          style={styles.select}
        >
          <option value="">All Statuses</option>
          <option value="TODO">To Do</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="DONE">Done</option>
        </select>
        <select
          value={filter.priority}
          onChange={(e) => setFilter({ ...filter, priority: e.target.value })}
          style={styles.select}
        >
          <option value="">All Priorities</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
        </select>
      </div>

      {!selectedProject ? (
        <div style={styles.empty}>Select a project to view tasks</div>
      ) : loading ? (
        <div style={styles.empty}>Loading tasks...</div>
      ) : tasks.length === 0 ? (
        <div style={styles.empty}>No tasks found</div>
      ) : (
        <div>
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onStatusChange={handleStatusChange}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { padding: '2rem', maxWidth: '800px', margin: '0 auto' },
  title: { margin: '0 0 1.2rem', fontSize: '1.8rem', color: '#1a1a2e' },
  filters: {
    display: 'flex',
    gap: '0.8rem',
    marginBottom: '1.5rem',
    flexWrap: 'wrap',
  },
  select: {
    padding: '0.6rem 0.9rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '0.9rem',
    outline: 'none',
    background: '#fff',
    minWidth: '160px',
  },
  empty: {
    textAlign: 'center',
    padding: '3rem 0',
    color: '#aaa',
    fontSize: '1rem',
  },
};
