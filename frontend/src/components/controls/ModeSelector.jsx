import React from 'react';
import { motion } from 'framer-motion';
// Optional: Import icons if you plan to add them
// import { Power, Leaf, Hand, Settings, Sigma } from 'lucide-react';

// Define the modes and their display properties
const thermostatModes = [
  // { value: 'off', name: 'Off' },
  // { value: 'eco', name: 'Eco Mode' },
  { value: 'manual', name: 'Manual Mode' },
  { value: 'auto_3speed', name: 'Automatic (3-Speed)' },
  { value: 'auto_pid', name: 'Automatic (PID)' },
];

// Optional: Map icons to mode values
// const modeIcons = {
//   'off': Power,
//   'eco': Leaf,
//   'manual': Hand,
//   'auto_3speed': Settings,
//   'auto_pid': Sigma,
// };

const ModeSelector = ({ currentMode, onModeChange }) => {


  return (
    <motion.div
      className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-6' // Outer container style
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
    >
      {/* Heading */}
      <h3 className="mb-5 text-lg font-medium text-gray-100">Select Operating Mode</h3>

      {/* Grid layout: 2 columns on medium screens and above */}
      <ul className="grid grid-cols-1 md:grid-cols-2 gap-4"> {/* gap-4 for spacing between items */}
        {thermostatModes.map((mode, index) => (
          <li
            key={mode.value}
            // --- Styling for the 5th item to center it ---
            // On medium screens and above, the 5th item (index 4) should span 2 columns and be centered.
            className={`
              ${index === 4 ? 'md:col-span-2 md:justify-self-center' : ''}
              w-full // Ensure list item takes full width of its grid cell
            `}
          >
            {/* Hidden radio input */}
            <input
              type="radio"
              id={`thermostat-mode-${mode.value}`} // Unique ID
              name="thermostat-mode"              // Same name for the group
              value={mode.value}                  // Mode identifier (sent to onModeChange)
              className="hidden peer"             // Hide default, enable peer styling
              checked={currentMode === mode.value} // Controlled by parent's state
              onChange={() => {
                onModeChange(mode.value);
                console.log("Mode changed! ",mode.value)}} // Call parent handler on change
              // Add required={true} if needed for a form
            />
            {/* The styled label - This is the clickable "button" */}
            <label
              htmlFor={`thermostat-mode-${mode.value}`}
              className={`
                inline-flex items-center justify-center w-full py-8 px-6 rounded-xl cursor-pointer h-full // Increased vertical padding (py-8), kept px-6
                bg-gray-800 bg-opacity-50 backdrop-blur-md border border-gray-700 // Base background and border
                text-gray-400 hover:text-gray-200 hover:bg-gray-700 hover:bg-opacity-70 // Hover states
                transition-all duration-200 ease-in-out // Animation for transitions
                // --- Corrected Checked State Styling (Blue Border/Text, Keep Glass Background) ---
                peer-checked:border-blue-600 // **Blue border when checked**
                peer-checked:text-blue-500   // **Blue text when checked**
                // peer-checked:bg-gray-800 peer-checked:bg-opacity-50 backdrop-blur-md // Explicitly keep base background if needed, but usually not necessary if you don't override it
                peer-checked:shadow-lg // Add shadow when checked
                peer-checked:scale-105 // Slightly scale up animation when checked
              `} // Combined Tailwind classes
            >
              <div className="flex flex-col items-center justify-center text-center">
                {/* Optional: Render icon */}
                {/* {modeIcons[mode.value] && (
                  <motion.div
                    initial={false}
                    animate={{ scale: currentMode === mode.value ? 1.2 : 1 }}
                    transition={{ duration: 0.2 }}
                  >
                     <modeIcons[mode.value] size={32} className="mb-3" /> // Icon size & margin (text color inherited)
                </motion.div>
                )} */}
                {/* Main mode name - Increased text size */}
                <div className="w-full text-xl font-semibold">{mode.name}</div> {/* Increased text size */}
                {/* Optional: Add a small description */}
                {/* <div className="w-full text-sm text-gray-300 mt-1">
                     {mode.value === 'off' && 'System is off'}
                     {mode.value === 'eco' && 'Energy saving setting'}
                     {mode.value === 'manual' && 'Direct fan control'}
                     {mode.value === 'auto_3speed' && 'Auto control (3 speeds)'}
                     {mode.value === 'auto_pid' && 'Auto control (continuous)'}
                   </div> */}
              </div>
            </label>
          </li>
        ))}
      </ul>
    </motion.div>
  );
};

export default ModeSelector;