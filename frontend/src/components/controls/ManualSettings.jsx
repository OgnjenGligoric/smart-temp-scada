// src/components/controls/ManualSettings.jsx
// This version focuses on styling the CircularSlider and displaying a value in its center.
// It uses local dummy state for basic interaction during styling.
// It DOES NOT accept or use the 'status' prop.
// It DOES NOT send commands or interact with any backend logic.

import React, { useState } from 'react'; // Import useState
import { motion } from 'framer-motion';
import CircularSlider from '@fseehawer/react-circular-slider';

import {sendFanSpeedChange} from "../../../services/api" // Import the API function to send fan speed changes

// Recharts imports are not needed in this component - remove them
// import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
// Remove dummy data arrays if they are not used in THIS component
// const salesByCategory = [ ... ];
// const COLORS = [ ... ];

// Define the available manual fan speeds and temperature range
const manualFanSpeeds = [0, 1, 2, 3];
const MIN_TEMP = 15; // Using the previous range
const MAX_TEMP = 35; // Using the previous range

// Set an initial dummy value
const INITIAL_DUMMY_TEMP = 15;

const ManualSettings = () => {
    // --- Dummy Local State for Styling Purposes Only ---
    // This state holds the value shown in the center and updates with the slider
    const [targetTemp, setTargetTemp] = useState(INITIAL_DUMMY_TEMP);
    // Dummy state for fan speed button highlight (optional for this specific request, but good to keep for styling)
    const [currentFanSpeed, setCurrentFanSpeed] = useState(0);

    // Dummy handler for the slider's onChange event
    const handleTempChange = (newValue) => {
        // The new library provides the continuous value. Round it to an integer for temp display.
        const roundedValue = Math.round(newValue);
        setTargetTemp(roundedValue); // Update the state to display the new value
        // console.log("Dummy Temp Slider Value:", roundedValue); // Optional logging
    };

     // Dummy handler for fan speed buttons (optional for this request, but good for styling buttons)
    const handleSpeedClick = (speed) => {
        
        sendFanSpeedChange(speed); // Send the fan speed change to the server
        console.log("Fan Speed Button Clicked:", speed); // Optional logging
        setCurrentFanSpeed(speed);
        
    };
    // --- End Dummy State ---


	return (
		<motion.div
			className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-6' // Added mb-6 for spacing
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ delay: 0.3 }}
		>
			<h2 className='text-xl font-semibold text-gray-100 mb-6'>Manual Control Settings</h2> {/* Adjusted spacing */}

			{/* Temperature Slider Section */}
			<div className="flex flex-col items-center mb-8">
        {/* Heading for the slider */}
				<h3 className="text-lg font-medium text-gray-300 mb-4">Set Target Temperature (°C)</h3>

        {/* Container for the slider AND the centered value. Make it relative */}
        {/* Use flex and justify-center/items-center to help center the slider itself */}
				<div className="relative flex items-center justify-center" style={{ width: "220px", height: "220px" }}>
            {/* Circular Slider */}
            <CircularSlider
              width={220} // Must match the width/height of the container div
              min={MIN_TEMP} // Use MIN_TEMP constant
              max={MAX_TEMP} // Use MAX_TEMP constant
              initialValue={INITIAL_DUMMY_TEMP} // Use INITIAL_DUMMY_TEMP constant
              // Use the dummy state handler for interactions
              onChange={handleTempChange}

              // --- Styling Props (adapted for this library) ---
              trackColor="#4B5563" // Background track color (Dark Grey)
              trackSize={12}      // Background track thickness
              progressColorFrom="#3B82F6" // Progress gradient start (Blue 600)
              progressColorTo="#60A5FA"   // Progress gradient end (Blue 400)
              progressSize={12}   // Progress arc thickness
              knobColor="#3B82F6" // Knob color (Blue 600)
              knobSize={36}       // Knob size
              progressLineCap="round" // Rounded ends

              // --- Behavior Props ---
              // onChange prop is already set to handleTempChange above

              // --- Label/Value Display Props ---
              // Keep hidden because we are using our custom display div
              hideLabelValue={true}
           />

           {/* --- Custom Display for Temperature Value --- */}
           {/* This div is absolutely positioned within the relative parent */}
           {/* Use Tailwind classes to center it (flex, justify-center, items-center) */}
           {/* Use Tailwind classes for text styling */}
           <div className="absolute inset-0 flex items-center justify-center pointer-events-none"> {/* pointer-events-none allows clicking the slider underneath */}
             <div className="text-gray-100 text-4xl font-bold">
               {/* Display the dummy state value */}
               {targetTemp}°C {/* Add the Celsius symbol */}
             </div>
           </div>
           {/* --- End Custom Display --- */}

			</div>
		</div>

         {/* Fan Speed Buttons Section (Copied from previous version, still uses dummy state) */}
        <div className="flex flex-col items-center">
            <h3 className="text-lg font-medium text-gray-300 mb-4">Set Manual Fan Speed</h3>
            <div className="flex space-x-4">
                {manualFanSpeeds.map((speed) => (
                    <button
                        key={speed}
                        onClick={() => handleSpeedClick(speed)}
                        className={`
                            px-6 py-2 rounded-md text-lg font-semibold
                            transition-colors duration-150 ease-in-out
                            ${
                                currentFanSpeed === speed
                                    ? 'bg-blue-600 text-white shadow-md'
                                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600 hover:text-gray-100'
                            }
                        `}
                    >
                        {speed === 0 ? 'Off' : `Speed ${speed}`}
                    </button>
                ))}
            </div>
        </div>
         {/* End Fan Speed Buttons Section */}


		</motion.div>
	);
};

export default ManualSettings;