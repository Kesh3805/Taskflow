import { useState, useEffect } from 'react';
import { FiX, FiCalendar, FiUser, FiMessageCircle, FiActivity } from 'react-icons/fi';
import PropTypes from 'prop-types';
import API from '../api/axios';
import LabelBadge from './LabelBadge';

const TaskDetailsModal = ({ task, isOpen, onClose, onUpdate, projectLabels, projectMembers }) => {
  const [comments, setComments] = useState([]);
  const [activityLog, setActivityLog] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('comments');
  const [editMode, setEditMode] = useState(false);
  const [editData, setEditData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    status: task?.status || 'TODO',
    priority: task?.priority || 'MEDIUM',
    assigned_to: task?.assigned_to || '',
    due_date: task?.due_date || '',
  });

  useEffect(() => {
    if (isOpen && task) {
      fetchComments();
      fetchActivity();
      setEditData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        assigned_to: task.assigned_to || '',
        due_date: task.due_date || '',
      });
    }
  }, [isOpen, task]);

  const fetchComments = async () => {
    try {
      const response = await API.get(`/tasks/${task.id}/comments`);
      setComments(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const fetchActivity = async () => {
    try {
      const response = await API.get(`/tasks/${task.id}/activity`);
      setActivityLog(response.data);
    } catch (error) {
      console.error('Error fetching activity:', error);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setLoading(true);
    try {
      await API.post(`/tasks/${task.id}/comments`, { content: newComment });
      setNewComment('');
      fetchComments();
      fetchActivity();
    } catch (error) {
      alert('Failed to add comment: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await API.put(`/tasks/${task.id}`, editData);
      onUpdate(response.data.task);
      setEditMode(false);
      fetchActivity();
    } catch (error) {
      alert('Failed to update task: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAddLabel = async (labelId) => {
    try {
      const response = await API.post(`/tasks/${task.id}/labels/${labelId}`);
      onUpdate(response.data);
    } catch (error) {
      alert('Failed to add label: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleRemoveLabel = async (labelId) => {
    try {
      const response = await API.delete(`/tasks/${task.id}/labels/${labelId}`);
      onUpdate(response.data);
    } catch (error) {
      alert('Failed to remove label: ' + (error.response?.data?.error || error.message));
    }
  };

  if (!isOpen || !task) return null;

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div style={styles.header}>
          <h2 style={styles.title}>Task Details</h2>
          <button onClick={onClose} style={styles.closeBtn}>
            <FiX size={24} />
          </button>
        </div>

        <div style={styles.content}>
          {/* Task Info Section */}
          {editMode ? (
            <form onSubmit={handleUpdateTask} style={styles.editForm}>
              <input
                type="text"
                value={editData.title}
                onChange={(e) => setEditData({ ...editData, title: e.target.value })}
                style={styles.input}
                placeholder="Task Title"
                required
              />
              <textarea
                value={editData.description}
                onChange={(e) => setEditData({ ...editData, description: e.target.value })}
                style={styles.textarea}
                placeholder="Description"
                rows={3}
              />
              <div style={styles.formRow}>
                <select
                  value={editData.status}
                  onChange={(e) => setEditData({ ...editData, status: e.target.value })}
                  style={styles.select}
                >
                  <option value="TODO">To Do</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="DONE">Done</option>
                </select>
                <select
                  value={editData.priority}
                  onChange={(e) => setEditData({ ...editData, priority: e.target.value })}
                  style={styles.select}
                >
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                </select>
              </div>
              <div style={styles.formRow}>
                <select
                  value={editData.assigned_to}
                  onChange={(e) => setEditData({ ...editData, assigned_to: e.target.value })}
                  style={styles.select}
                >
                  <option value="">Unassigned</option>
                  {projectMembers.map((member) => (
                    <option key={member.id} value={member.id}>
                      {member.name}
                    </option>
                  ))}
                </select>
                <input
                  type="date"
                  value={editData.due_date}
                  onChange={(e) => setEditData({ ...editData, due_date: e.target.value })}
                  style={styles.input}
                />
              </div>
              <div style={styles.formActions}>
                <button type="submit" style={styles.saveBtn} disabled={loading}>
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
                <button type="button" onClick={() => setEditMode(false)} style={styles.cancelBtn}>
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div style={styles.taskInfo}>
              <h3 style={styles.taskTitle}>{task.title}</h3>
              {task.description && <p style={styles.taskDesc}>{task.description}</p>}
              
              <div style={styles.metadata}>
                <div style={styles.metaItem}>
                  <strong>Status:</strong> {task.status.replace('_', ' ')}
                </div>
                <div style={styles.metaItem}>
                  <strong>Priority:</strong> {task.priority}
                </div>
                {task.assignee && (
                  <div style={styles.metaItem}>
                    <FiUser size={14} />
                    <strong>Assigned to:</strong> {task.assignee.name}
                  </div>
                )}
                {task.due_date && (
                  <div style={styles.metaItem}>
                    <FiCalendar size={14} />
                    <strong>Due:</strong> {task.due_date}
                  </div>
                )}
              </div>

              {/* Labels */}
              <div style={styles.labelsSection}>
                <strong>Labels:</strong>
                <div style={styles.labelsGrid}>
                  {task.labels?.map((label) => (
                    <LabelBadge
                      key={label.id}
                      label={label}
                      removable
                      onRemove={handleRemoveLabel}
                    />
                  ))}
                  <select
                    onChange={(e) => {
                      if (e.target.value) {
                        handleAddLabel(Number(e.target.value));
                        e.target.value = '';
                      }
                    }}
                    style={styles.labelSelect}
                  >
                    <option value="">+ Add Label</option>
                    {projectLabels
                      .filter((label) => !task.labels?.some((tl) => tl.id === label.id))
                      .map((label) => (
                        <option key={label.id} value={label.id}>
                          {label.name}
                        </option>
                      ))}
                  </select>
                </div>
              </div>

              <button onClick={() => setEditMode(true)} style={styles.editBtn}>
                Edit Task
              </button>
            </div>
          )}

          {/* Tabs */}
          <div style={styles.tabs}>
            <button
              style={activeTab === 'comments' ? { ...styles.tab, ...styles.activeTab } : styles.tab}
              onClick={() => setActiveTab('comments')}
            >
              <FiMessageCircle size={16} /> Comments ({comments.length})
            </button>
            <button
              style={activeTab === 'activity' ? { ...styles.tab, ...styles.activeTab } : styles.tab}
              onClick={() => setActiveTab('activity')}
            >
              <FiActivity size={16} /> Activity ({activityLog.length})
            </button>
          </div>

          {/* Tab Content */}
          <div style={styles.tabContent}>
            {activeTab === 'comments' ? (
              <>
                <form onSubmit={handleAddComment} style={styles.commentForm}>
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Add a comment..."
                    style={styles.commentInput}
                    rows={3}
                  />
                  <button type="submit" style={styles.commentBtn} disabled={loading || !newComment.trim()}>
                    {loading ? 'Posting...' : 'Post Comment'}
                  </button>
                </form>
                <div style={styles.commentsList}>
                  {comments.length === 0 ? (
                    <p style={styles.emptyState}>No comments yet</p>
                  ) : (
                    comments.map((comment) => (
                      <div key={comment.id} style={styles.comment}>
                        <div style={styles.commentHeader}>
                          <strong>{comment.author?.name}</strong>
                          <span style={styles.commentDate}>
                            {new Date(comment.created_at).toLocaleString()}
                          </span>
                        </div>
                        <p style={styles.commentContent}>{comment.content}</p>
                      </div>
                    ))
                  )}
                </div>
              </>
            ) : (
              <div style={styles.activityList}>
                {activityLog.length === 0 ? (
                  <p style={styles.emptyState}>No activity yet</p>
                ) : (
                  activityLog.map((activity) => (
                    <div key={activity.id} style={styles.activityItem}>
                      <div style={styles.activityHeader}>
                        <strong>{activity.user?.name}</strong>
                        <span style={styles.activityAction}>{activity.action}</span>
                        {activity.field_changed && (
                          <span style={styles.activityField}>{activity.field_changed}</span>
                        )}
                      </div>
                      {activity.old_value && activity.new_value && (
                        <div style={styles.activityChange}>
                          <span style={styles.oldValue}>{activity.old_value}</span>
                          <span> → </span>
                          <span style={styles.newValue}>{activity.new_value}</span>
                        </div>
                      )}
                      <span style={styles.activityDate}>
                        {new Date(activity.created_at).toLocaleString()}
                      </span>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

TaskDetailsModal.propTypes = {
  task: PropTypes.object,
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  projectLabels: PropTypes.array.isRequired,
  projectMembers: PropTypes.array.isRequired,
};

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modal: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    width: '90%',
    maxWidth: '800px',
    maxHeight: '90vh',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1.5rem',
    borderBottom: '1px solid #e2e8f0',
  },
  title: {
    margin: 0,
    fontSize: '1.5rem',
    fontWeight: '600',
    color: '#1a202c',
  },
  closeBtn: {
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '0.5rem',
    display: 'flex',
    alignItems: 'center',
    color: '#718096',
  },
  content: {
    padding: '1.5rem',
    overflowY: 'auto',
    flex: 1,
  },
  taskInfo: {
    marginBottom: '1.5rem',
  },
  taskTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '0.5rem',
    color: '#2d3748',
  },
  taskDesc: {
    color: '#718096',
    marginBottom: '1rem',
    lineHeight: 1.6,
  },
  metadata: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '0.75rem',
    marginBottom: '1rem',
  },
  metaItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    fontSize: '0.9rem',
    color: '#4a5568',
  },
  labelsSection: {
    marginBottom: '1rem',
  },
  labelsGrid: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '0.5rem',
    marginTop: '0.5rem',
  },
  labelSelect: {
    padding: '0.25rem 0.5rem',
    fontSize: '0.75rem',
    border: '1px dashed #cbd5e0',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  editBtn: {
    backgroundColor: '#4299e1',
    color: '#fff',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
  },
  editForm: {
    marginBottom: '1.5rem',
  },
  input: {
    width: '100%',
    padding: '0.75rem',
    marginBottom: '0.75rem',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    fontSize: '0.95rem',
  },
  textarea: {
    width: '100%',
    padding: '0.75rem',
    marginBottom: '0.75rem',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    fontSize: '0.95rem',
    fontFamily: 'inherit',
    resize: 'vertical',
  },
  select: {
    flex: 1,
    padding: '0.75rem',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    fontSize: '0.95rem',
  },
  formRow: {
    display: 'flex',
    gap: '0.75rem',
    marginBottom: '0.75rem',
  },
  formActions: {
    display: 'flex',
    gap: '0.75rem',
  },
  saveBtn: {
    backgroundColor: '#48bb78',
    color: '#fff',
    border: 'none',
    padding: '0.75rem 1.5rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
  },
  cancelBtn: {
    backgroundColor: '#e2e8f0',
    color: '#4a5568',
    border: 'none',
    padding: '0.75rem 1.5rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    fontWeight: '500',
  },
  tabs: {
    display: 'flex',
    gap: '0.5rem',
    borderBottom: '1px solid #e2e8f0',
    marginBottom: '1rem',
  },
  tab: {
    background: 'none',
    border: 'none',
    padding: '0.75rem 1rem',
    cursor: 'pointer',
    fontSize: '0.9rem',
    color: '#718096',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    borderBottom: '2px solid transparent',
  },
  activeTab: {
    color: '#4299e1',
    borderBottomColor: '#4299e1',
  },
  tabContent: {
    minHeight: '200px',
  },
  commentForm: {
    marginBottom: '1.5rem',
  },
  commentInput: {
    width: '100%',
    padding: '0.75rem',
    border: '1px solid #e2e8f0',
    borderRadius: '6px',
    fontSize: '0.9rem',
    fontFamily: 'inherit',
    marginBottom: '0.5rem',
    resize: 'vertical',
  },
  commentBtn: {
    backgroundColor: '#4299e1',
    color: '#fff',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '0.9rem',
  },
  commentsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  comment: {
    padding: '1rem',
    backgroundColor: '#f7fafc',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
  },
  commentHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '0.5rem',
  },
  commentDate: {
    fontSize: '0.75rem',
    color: '#a0aec0',
  },
  commentContent: {
    margin: 0,
    color: '#4a5568',
    lineHeight: 1.5,
  },
  activityList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
  },
  activityItem: {
    padding: '0.75rem',
    backgroundColor: '#f7fafc',
    borderRadius: '6px',
    fontSize: '0.85rem',
  },
  activityHeader: {
    display: 'flex',
    gap: '0.5rem',
    marginBottom: '0.25rem',
    flexWrap: 'wrap',
  },
  activityAction: {
    color: '#4a5568',
    fontStyle: 'italic',
  },
  activityField: {
    color: '#718096',
    backgroundColor: '#e2e8f0',
    padding: '0.125rem 0.5rem',
    borderRadius: '4px',
  },
  activityChange: {
    marginTop: '0.25rem',
    marginBottom: '0.25rem',
  },
  oldValue: {
    color: '#e53e3e',
    textDecoration: 'line-through',
  },
  newValue: {
    color: '#48bb78',
    fontWeight: '500',
  },
  activityDate: {
    fontSize: '0.7rem',
    color: '#a0aec0',
    display: 'block',
    marginTop: '0.25rem',
  },
  emptyState: {
    textAlign: 'center',
    color: '#a0aec0',
    padding: '2rem',
  },
};

export default TaskDetailsModal;
