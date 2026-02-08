import { useState } from 'react';
import PropTypes from 'prop-types';

const LabelBadge = ({ label, onRemove, removable = false }) => {
  return (
    <span
      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
      style={{ backgroundColor: label.color + '20', color: label.color, border: `1px solid ${label.color}` }}
    >
      {label.name}
      {removable && (
        <button
          onClick={() => onRemove(label.id)}
          className="ml-1 hover:text-red-600 focus:outline-none"
        >
          ×
        </button>
      )}
    </span>
  );
};

LabelBadge.propTypes = {
  label: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    color: PropTypes.string.isRequired,
  }).isRequired,
  onRemove: PropTypes.func,
  removable: PropTypes.bool,
};

export default LabelBadge;
