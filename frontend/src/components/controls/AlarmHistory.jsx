// src/components/data/AlarmHistory.jsx (Example path)

import React from 'react';
import { motion } from 'framer-motion';
// Optional: Import icons for alarm types if desired
// import { AlertTriangle, ThermometerSnowflake, ThermometerSun, Zap } from 'lucide-react';

// --- Dummy Alarm Data for Styling Preview Only ---
// In the final version, this data will be fetched from your backend log
const dummyAlarms = [
  {
    id: 1,
    timestamp: '2025-04-26 10:30:15',
    type: 'Temperature Exceeded Upper Limit',
    // Optional: severity: 'high' // Could use for color coding
  },
  {
    id: 2,
    timestamp: '2025-04-26 11:05:40',
    type: 'Window Open while Fan Active',
    // Optional: severity: 'medium'
  },
  {
    id: 3,
    timestamp: '2025-04-26 09:10:01',
    type: 'Temperature Below Lower Limit',
    // Optional: severity: 'high'
  },
  {
    id: 4,
    timestamp: '2025-04-25 23:55:00',
    type: 'Window Open while Fan Active',
    // Optional: severity: 'medium'
  },
   {
    id: 5,
    timestamp: '2025-04-25 22:18:30',
    type: 'Temperature Exceeded Upper Limit',
    // Optional: severity: 'high'
  },
];
// --- End Dummy Alarm Data ---


const AlarmHistory = () => {

  // In this styling-only version, we render unconditionally.
  // In the functional version, you might pass 'alarms' data as a prop instead of using local dummy data.

  return (
    // Main container with your dark/glassmorphic style and animation
    <motion.div
      className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-6 overflow-hidden' // Added overflow-hidden for rounded corners with potential scroll
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }} // Animation on entry
    >
      {/* Heading */}
      <h2 className='text-xl font-semibold text-gray-100 mb-6'>Alarm History</h2>

      {/* Alarm List Container */}
      {/* Optional: Add max-h and overflow-y-auto to make the list scrollable if it gets long */}
      <div className="max-h-64 overflow-y-auto pr-2" style={{ scrollbarGutter: 'stable' }}> {/* pr-2 adds space for scrollbar */}

        {dummyAlarms.length > 0 ? (
          // Map over dummy data to create list items
          dummyAlarms.map(alarm => (
            <div
              key={alarm.id} // Unique key is important when mapping lists
              className="flex justify-between items-center border-b border-gray-700 py-3 last:border-b-0" // Flex layout, bottom border, padding, remove border on last item
            >
              {/* Left side: Timestamp and optional Icon */}
              <div className="flex items-center mr-4"> {/* Added right margin */}
                {/* Optional: Render icon based on alarm type/severity */}
                {/* <AlertTriangle size={20} className="text-red-500 mr-2" /> */}
                <span className="text-sm text-gray-400">{alarm.timestamp}</span> {/* Timestamp styling */}
              </div>

              {/* Right side: Alarm Type */}
              <div className="flex-shrink-0 text-right"> {/* Prevent text wrapping, right align */}
                 {/* Style alarm type - maybe red for critical, orange for warning? */}
                 <span className="text-sm font-medium text-red-500"> {/* Example: Use red for alarm text */}
                   {alarm.type}
                 </span>
              </div>
            </div>
          ))
        ) : (
          // Display a message if there are no alarms (or dummy data is empty)
          <div className="text-center text-gray-400 py-4">
            No alarms recorded yet.
          </div>
        )}

      </div>
      {/* End Alarm List Container */}

    </motion.div>
  );
};

export default AlarmHistory;