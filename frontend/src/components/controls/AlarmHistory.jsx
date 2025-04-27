
import React from 'react';
import { motion } from 'framer-motion';

const AlarmHistory = ({ alarmHistory }) => {
  return (
    <motion.div
      className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-red-700 mb-6 overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
    >
      <h2 className="text-xl font-semibold text-gray-100 mb-6">Alarms</h2>

      <div className="max-h-64 overflow-y-auto pr-2" style={{ scrollbarGutter: 'stable' }}>
        {alarmHistory.length > 0 ? (
          alarmHistory.map(alarm => (
            <div
              key={alarm.id}
              className="flex justify-between items-center border-b border-gray-700 py-3 last:border-b-0"
            >
              <div className="flex items-center mr-4">
                <span className="text-lg text-gray-400">{alarm.timestamp}</span>
              </div>

              <div className="flex-shrink-0 text-right">
                <span className="text-lg font-medium text-red-500">
                  {alarm.alarmDescription}
                </span>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-400 py-4">No alarms recorded yet.</div>
        )}
      </div>
    </motion.div>
  );
};

export default AlarmHistory;