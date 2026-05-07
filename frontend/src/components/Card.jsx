import React from 'react';

const Card = ({ title, value, icon, colorClass }) => {
  return (
    <div className="bg-surface-container-lowest border border-outline-variant p-md rounded-xl">
      <div className="flex justify-between items-start mb-sm">
        <div className={`${colorClass} p-sm rounded-lg`}>
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
            {icon}
          </span>
        </div>
      </div>
      <p className="text-on-surface-variant font-label-caps text-label-caps uppercase">{title}</p>
      <p className="font-h1 text-h1 font-bold text-on-surface">{value}</p>
    </div>
  );
};

export default Card;
