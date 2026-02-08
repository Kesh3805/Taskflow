import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import API from '../api/axios';
import TaskCard from '../components/TaskCard';
import TaskDetailsModal from '../components/TaskDetailsModal';
import { useAuth } from '../context/AuthContext';
import { FiArrowLeft, FiPlus, FiTrash2, FiUserPlus, FiTag } from 'react-icons/fi';

export default function ProjectDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ status: '', priority: '' });

  // Task form
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [taskTitle, setTaskTitle] = useState('');
  const [taskDesc, setTaskDesc] = useState('');
  const [taskPriority, setTaskPriority] = useState('MEDIUM');
  const [taskDueDate, setTaskDueDate] = useState('');
  const [taskAssignee, setTaskAssignee] = useState('');

  // Add member
  const [allUsers, setAllUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [showMemberForm, setShowMemberForm] = useState(false);

  // Labels
  const [labels, setLabels] = useState([]);
  const [showLabelForm, setShowLabelForm] = useState(false);
  const [labelName, setLabelName] = useState('');
  const [labelColor, setLabelColor] = useState('#6b7280');

  // Task Details Modal
  const [selectedTask, setSelectedTask] = useState(null);
  const [showTaskModal, setShowTaskModal] = useState(false);

  const fetchProject = async () => {
    try {
      const res = await API.get(`/projects/${id}`);
      setProject(res.data.project);
    } catch (err) {
      console.error(err);
      navigate('/');
    }
  };

  const fetchAllUsers = async () => {
    try {
      const res = await API.get('/auth/users');
      setAllUsers(res.data.users || []);
    } catch (err) {
      console.error('Failed to fetch users', err);
    }
  };

  const fetchLabels = async () => {
    try {
      const res = await API.get(`/projects/${id}/labels`);
      setLabels(res.data);
    } catch (err) {
      console.error('Failed to fetch labels', err);
    }
  };

  const fetchTasks = async () => {
    try {
      const params = {};
      if (filter.status) params.status = filter.status;
      if (filter.priority) params.priority = filter.priority;
      const res = await API.get(`/tasks/project/${id}`, { params });
      setTasks(res.data.tasks);
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProject();
    fetchAllUsers();
    fetchLabels();
  }, [id]);

  useEffect(() => {
    if (project) fetchTasks();
  }, [project, filter]);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    try {
      await API.post('/tasks', {
        title: taskTitle,
        description: taskDesc,
        project_id: parseInt(id),
        priority: taskPriority,
        due_date: taskDueDate || null,
        assigned_to: taskAssignee ? parseInt(taskAssignee) : null,
      });
      setTaskTitle('');
      setTaskDesc('');
      setTaskPriority('MEDIUM');
      setTaskDueDate('');
      setTaskAssignee('');
      setShowTaskForm(false);
      fetchTasks();
    } catch (err) {
      console.error(err);
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await API.put(`/tasks/${taskId}`, { status: newStatus });
      fetchTasks();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Delete this task?')) return;
    try {
      await API.delete(`/tasks/${taskId}`);
      fetchTasks();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteProject = async () => {
    if (!window.confirm('Delete this project and all its tasks?')) return;
    try {
      await API.delete(`/projects/${id}`);
      navigate('/');
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddMember = async (e) => {
    e.preventDefault();
    if (!selectedUserId) {
      alert('Please select a user');
      return;
    }
    try {
      await API.post(`/projects/${id}/members`, { user_id: parseInt(selectedUserId) });
      setSelectedUserId('');
      setShowMemberForm(false);
      fetchProject();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to add member');
    }
  };

  const handleCreateLabel = async (e) => {
    e.preventDefault();
    try {
      await API.post(`/projects/${id}/labels`, { name: labelName, color: labelColor });
      setLabelName('');
      setLabelColor('#6b7280');
      setShowLabelForm(false);
      fetchLabels();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to create label');
    }
  };

  const handleDeleteLabel = async (labelId) => {
    if (!window.confirm('Delete this label?')) return;
    try {
      await API.delete(`/projects/labels/${labelId}`);
      fetchLabels();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete label');
    }
  };

  const handleTaskClick = (task) => {
    setSelectedTask(task);
    setShowTaskModal(true);
  };

  const handleTaskUpdate = (updatedTask) => {
    setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
    setSelectedTask(updatedTask);
    fetchTasks();
  };

  if (loading || !project) {
    return <div style={{ textAlign: 'center', padding: '4rem', color: '#888' }}>Loading...</div>;
  }

  const isOwner = project.owner_id === user?.id || user?.role === 'ADMIN';

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.topBar}>
        <button onClick={() => navigate('/')} style={styles.backBtn}>
          <FiArrowLeft size={18} /> Back
        </button>
        {isOwner && (
          <button onClick={handleDeleteProject} style={styles.deleteProjectBtn}>
            <FiTrash2 size={16} /> Delete Project
          </button>
        )}
      </div>

      <h1 style={styles.title}>{project.name}</h1>
      <p style={styles.desc}>{project.description || 'No description'}</p>

      {/* Role Indicator */}
      <div style={styles.roleIndicator}>
        {user?.role === 'ADMIN' ? (
          <>
            <span style={styles.roleBadgeAdmin}>ADMIN</span>
            <span style={styles.roleText}>Full access to all project features</span>
          </>
        ) : isOwner ? (
          <>
            <span style={styles.roleBadgeOwner}>OWNER</span>
            <span style={styles.roleText}>You own this project - manage members & labels</span>
          </>
        ) : (
          <>
            <span style={styles.roleBadgeMember}>MEMBER</span>
            <span style={styles.roleText}>Create & manage tasks, comment, use labels</span>
          </>
        )}
      </div>

      {/* Summary Cards */}
      <div style={styles.summaryRow}>
        {['TODO', 'IN_PROGRESS', 'DONE'].map((s) => (
          <div key={s} style={styles.summaryCard}>
            <span style={styles.summaryCount}>{summary[s] || 0}</span>
            <span style={styles.summaryLabel}>{s.replace('_', ' ')}</span>
          </div>
        ))}
        <div style={styles.summaryCard}>
          <span style={styles.summaryCount}>{summary.total || 0}</span>
          <span style={styles.summaryLabel}>TOTAL</span>
        </div>
      </div>

      {/* Members */}
      <div style={styles.section}>
        <div style={styles.sectionHeader}>
          <h3 style={{ margin: 0 }}>Members ({project.members?.length || 0})</h3>
          {isOwner && (
            <button onClick={() => setShowMemberForm(!showMemberForm)} style={styles.smallBtn}>
              <FiUserPlus size={14} /> Add
            </button>
          )}
        </div>
        {showMemberForm && (
          <form onSubmit={handleAddMember} style={styles.inlineForm}>
            <select
              value={selectedUserId}
              onChange={(e) => setSelectedUserId(e.target.value)}
              style={styles.select}
              required
            >
              <option value="">Select a user...</option>
              {allUsers
                .filter(u => !project.members?.some(m => m.id === u.id))
                .map((u) => (
                  <option key={u.id} value={u.id}>
                    {u.name} (ID: {u.id}) - {u.email}
                  </option>
                ))}
            </select>
            <button type="submit" style={styles.smallSubmitBtn}>Add</button>
          </form>
        )}
        <div style={styles.memberList}>
          {project.members?.map((m) => (
            <span key={m.id} style={styles.memberChip}>
              {m.name} {m.id === project.owner_id && '👑'}
            </span>
          ))}
        </div>
      </div>

      {/* Labels */}
      <div style={styles.section}>
        <div style={styles.sectionHeader}>
          <h3 style={{ margin: 0 }}>Labels ({labels.length})</h3>
          {isOwner && (
            <button onClick={() => setShowLabelForm(!showLabelForm)} style={styles.smallBtn}>
              <FiTag size={14} /> Add Label
            </button>
          )}
        </div>
        {showLabelForm && isOwner && (
          <form onSubmit={handleCreateLabel} style={styles.inlineForm}>
            <input
              type="text"
              placeholder="Label name"
              value={labelName}
              onChange={(e) => setLabelName(e.target.value)}
              style={styles.input}
              required
            />
            <input
              type="color"
              value={labelColor}
              onChange={(e) => setLabelColor(e.target.value)}
              style={styles.colorInput}
            />
            <button type="submit" style={styles.smallSubmitBtn}>Create</button>
          </form>
        )}
        <div style={styles.labelList}>
          {labels.map((label) => (
            <div 
              key={label.id} 
              style={{ 
                ...styles.labelChip, 
                backgroundColor: label.color + '20', 
                border: `1px solid ${label.color}`,
                color: label.color 
              }}
            >
              {label.name}
              {isOwner && (
                <button
                  onClick={() => handleDeleteLabel(label.id)}
                  style={styles.labelDeleteBtn}
                  title="Delete label"
                >
                  ×
                </button>
              )}
            </div>
          ))}
          {labels.length === 0 && <p style={{ color: '#999', fontSize: '0.9rem' }}>No labels yet{!isOwner && ' - only project owner can create labels'}</p>}
        </div>
      </div>

      {/* Filters & Tasks */}
      <div style={styles.section}>
        <div style={styles.sectionHeader}>
          <h3 style={{ margin: 0 }}>Tasks</h3>
          <button onClick={() => setShowTaskForm(!showTaskForm)} style={styles.addTaskBtn}>
            <FiPlus size={16} /> New Task
          </button>
        </div>

        {/* Filters */}
        <div style={styles.filterRow}>
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

        {/* New Task Form */}
        {showTaskForm && (
          <form onSubmit={handleCreateTask} style={styles.taskForm}>
            <input
              type="text"
              placeholder="Task title"
              value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              style={styles.input}
              required
            />
            <input
              type="text"
              placeholder="Description"
              value={taskDesc}
              onChange={(e) => setTaskDesc(e.target.value)}
              style={styles.input}
            />
            <div style={styles.formRow}>
              <select
                value={taskPriority}
                onChange={(e) => setTaskPriority(e.target.value)}
                style={styles.select}
              >
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
              </select>
              <input
                type="date"
                value={taskDueDate}
                onChange={(e) => setTaskDueDate(e.target.value)}
                style={styles.input}
              />
              <select
                value={taskAssignee}
                onChange={(e) => setTaskAssignee(e.target.value)}
                style={styles.select}
              >
                <option value="">Unassigned</option>
                {project.members?.map((m) => (
                  <option key={m.id} value={m.id}>{m.name}</option>
                ))}
              </select>
            </div>
            <button type="submit" style={styles.submitBtn}>Create Task</button>
          </form>
        )}

        {/* Task List */}
        {tasks.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem 0', color: '#aaa' }}>
            No tasks found. Create your first task!
          </div>
        ) : (
          <div style={styles.taskList}>
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onStatusChange={handleStatusChange}
                onDelete={handleDeleteTask}
                onClick={() => handleTaskClick(task)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Task Details Modal */}
      <TaskDetailsModal
        task={selectedTask}
        isOpen={showTaskModal}
        onClose={() => setShowTaskModal(false)}
        onUpdate={handleTaskUpdate}
        projectLabels={labels}
        projectMembers={project.members || []}
      />
    </div>
  );
}

const styles = {
  container: { padding: '2rem', maxWidth: '900px', margin: '0 auto' },
  topBar: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '1rem',
  },
  backBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.3rem',
    background: 'none',
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '0.5rem 1rem',
    cursor: 'pointer',
    color: '#555',
    fontSize: '0.9rem',
  },
  deleteProjectBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.3rem',
    background: '#fce4ec',
    color: '#c62828',
    border: 'none',
    borderRadius: '8px',
    padding: '0.5rem 1rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: '500',
  },
  title: { margin: '0 0 0.3rem', fontSize: '1.8rem', color: '#1a1a2e' },
  desc: { color: '#777', marginBottom: '1.5rem' },
  roleIndicator: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.8rem',
    padding: '0.8rem 1.2rem',
    background: '#f8f9fa',
    borderRadius: '10px',
    marginBottom: '1.5rem',
    border: '1px solid #e9ecef',
  },
  roleBadgeAdmin: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    padding: '0.3rem 0.9rem',
    borderRadius: '16px',
    fontSize: '0.7rem',
    fontWeight: '700',
    letterSpacing: '0.5px',
  },
  roleBadgeOwner: {
    background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    color: '#fff',
    padding: '0.3rem 0.9rem',
    borderRadius: '16px',
    fontSize: '0.7rem',
    fontWeight: '700',
    letterSpacing: '0.5px',
  },
  roleBadgeMember: {
    background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    color: '#fff',
    padding: '0.3rem 0.9rem',
    borderRadius: '16px',
    fontSize: '0.7rem',
    fontWeight: '700',
    letterSpacing: '0.5px',
  },
  roleText: {
    fontSize: '0.85rem',
    color: '#666',
  },
  summaryRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '1rem',
    marginBottom: '2rem',
  },
  summaryCard: {
    background: '#fff',
    borderRadius: '12px',
    padding: '1.2rem',
    textAlign: 'center',
    boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
  },
  summaryCount: {
    display: 'block',
    fontSize: '1.8rem',
    fontWeight: '700',
    color: '#667eea',
  },
  summaryLabel: { fontSize: '0.75rem', color: '#999', fontWeight: '600' },
  section: { marginBottom: '2rem' },
  sectionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1rem',
  },
  smallBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.3rem',
    background: '#f0f0f0',
    border: 'none',
    borderRadius: '6px',
    padding: '0.4rem 0.8rem',
    cursor: 'pointer',
    fontSize: '0.8rem',
  },
  inlineForm: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.8rem',
  },
  memberList: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap' },
  memberChip: {
    background: '#f0f0f0',
    padding: '0.3rem 0.8rem',
    borderRadius: '16px',
    fontSize: '0.82rem',
    color: '#555',
  },
  labelList: { display: 'flex', gap: '0.5rem', flexWrap: 'wrap' },
  labelChip: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.3rem 0.8rem',
    borderRadius: '16px',
    fontSize: '0.82rem',
    fontWeight: '500',
  },
  labelDeleteBtn: {
    background: 'none',
    border: 'none',
    color: 'inherit',
    cursor: 'pointer',
    fontSize: '1.2rem',
    lineHeight: 1,
    padding: '0',
    marginLeft: '0.25rem',
  },
  colorInput: {
    width: '60px',
    height: '38px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  addTaskBtn: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.3rem',
    padding: '0.5rem 1rem',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '0.85rem',
    fontWeight: '600',
    cursor: 'pointer',
  },
  filterRow: {
    display: 'flex',
    gap: '0.8rem',
    marginBottom: '1rem',
  },
  select: {
    padding: '0.5rem 0.8rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '0.85rem',
    outline: 'none',
    background: '#fff',
  },
  taskForm: {
    background: '#fff',
    padding: '1.2rem',
    borderRadius: '12px',
    marginBottom: '1rem',
    boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
  },
  input: {
    width: '100%',
    padding: '0.6rem 0.8rem',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '0.9rem',
    outline: 'none',
    marginBottom: '0.6rem',
    boxSizing: 'border-box',
  },
  formRow: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.6rem',
  },
  submitBtn: {
    padding: '0.6rem 1.2rem',
    background: '#667eea',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  smallSubmitBtn: {
    padding: '0.5rem 1rem',
    background: '#667eea',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontWeight: '600',
    cursor: 'pointer',
    fontSize: '0.85rem',
  },
  taskList: { marginTop: '0.5rem' },
};
