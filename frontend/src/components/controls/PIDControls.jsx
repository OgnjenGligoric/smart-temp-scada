// src/components/controls/PIDControls.jsx
// This version is for STYLING PREVIEW ONLY.
// It includes the input fields and button structure but uses dummy local state.
// It DOES NOT accept or use the 'status' prop for rendering or data.
// It DOES NOT send commands or interact with any backend logic.

import React, { useState, useEffect } from 'react'; // Import useState and useEffect (even if useEffect is commented out)
import { motion } from 'framer-motion';

import {sendPIDSettings} from "../../../services/api" // Import the API function to send PID settings (commented out for styling preview)


// Define default PID values and temp range for initial dummy state
const DEFAULT_KP = '1.0';
const DEFAULT_KI = '0.1';
const DEFAULT_KD = '0.01';
const DEFAULT_TARGET_TEMP = '22.0';
const MIN_TEMP_INPUT = 15;
const MAX_TEMP_INPUT = 30;


const PIDControls = ({ status, onSetPIDParams, onSetTargetTemp, calculatedPIDValue }) => { // Props are listed but NOT used for rendering/logic in this version

    // --- Dummy Local State for Input Values (for styling preview) ---
    // These state variables hold the values shown in the input fields.
    const [kpInput, setKpInput] = useState(DEFAULT_KP);
    const [kiInput, setKiInput] = useState(DEFAULT_KI);
    const [kdInput, setKdInput] = useState(DEFAULT_KD);
    const [targetTempInput, setTargetTempInput] = useState(DEFAULT_TARGET_TEMP);
   
    const handleSetValues = () => {
        console.log("Set Values clicked");
        console.log("Kp:", kpInput, "Ki:", kiInput, "Kd:", kdInput, "Target Temp:", targetTempInput);
        
        // Call the API function to send the PID settings (commented out for styling preview)
        sendPIDSettings(kpInput, kiInput, kdInput, targetTempInput)
        
    };


    return (
        // Main container with your dark/glassmorphic style and animation
        <motion.div
            className='bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-6'
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }} // Animation on entry
        >
            {/* Heading */}
            <h2 className='text-xl font-semibold text-gray-100 mb-6'>Automatic (PID) Control Settings </h2>

            {/* === START: PID Parameters Input Section === */}
            <div className="flex flex-col mb-8"> {/* Flex container for the entire section */}
                <h3 className="text-lg font-medium text-gray-300 mb-4">PID Parameters (Kp, Ki, Kd)</h3> {/* Section heading */}

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4"> {/* Grid for side-by-side inputs */}
                    {/* Kp Input */}
                    <div>
                        <label htmlFor="kp-input" className="block text-sm font-medium text-gray-400 mb-1">Kp</label> {/* Label for accessibility */}
                        <input
                            type="number" // Use number type for numerical input
                            id="kp-input" // Match label's htmlFor
                            value={kpInput} // Controlled by local state
                            onChange={(e) => setKpInput(e.target.value)} // Update local state on change
                            className="w-full px-3 py-2 rounded-md bg-gray-700 bg-opacity-50 border border-gray-600 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500" // Styling
                            step="0.1" // Allow decimal steps (adjust as needed)
                            min="0"   
                            max="50" 
                        />
                    </div>

                    {/* Ki Input */}
                    <div>
                         <label htmlFor="ki-input" className="block text-sm font-medium text-gray-400 mb-1">Ki</label>
                        <input
                            type="number"
                            id="ki-input"
                            value={kiInput}
                            onChange={(e) => setKiInput(e.target.value)}
                             className="w-full px-3 py-2 rounded-md bg-gray-700 bg-opacity-50 border border-gray-600 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                             step="0.01" 
                             min="0"   
                             max="10" 
                        />
                    </div>

                    {/* Kd Input */}
                    <div>
                         <label htmlFor="kd-input" className="block text-sm font-medium text-gray-400 mb-1">Kd</label>
                        <input
                            type="number"
                            id="kd-input"
                            value={kdInput}
                            onChange={(e) => setKdInput(e.target.value)} // <-- Corrected typo: setKdInput
                             className="w-full px-3 py-2 rounded-md bg-gray-700 bg-opacity-50 border border-gray-600 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                             step="0.001" 
                             min="0"   
                             max="10" 
                        />
                    </div>
                </div>
            </div>
            {/* === END: PID Parameters Input Section === */}


            {/* === START: Target Temperature Input Section === */}
             <div className="flex flex-col mb-8"> {/* Flex container for section */}
                <h3 className="text-lg font-medium text-gray-300 mb-4">Target Temperature (°C)</h3> {/* Section heading */}
                <div className="max-w-xs"> {/* Limit width for a single input */}
                    <label htmlFor="target-temp-input" className="block text-sm font-medium text-gray-400 mb-1">Temperature (°C)</label> {/* Label */}
                     <input
                        type="number"
                        id="target-temp-input" // Match label's htmlFor
                        value={targetTempInput} // Controlled by local state
                        onChange={(e) => setTargetTempInput(e.target.value)} // Update local state
                        className="w-full px-3 py-2 rounded-md bg-gray-700 bg-opacity-50 border border-gray-600 text-gray-100 focus:outline-none focus:ring-blue-500 focus:border-blue-500" // Styling
                        step="0.1" // Allow decimal steps
                        min="15" // Use your defined min/max temp for context
                        max="30"
                    />
                </div>
            </div>
            {/* === END: Target Temperature Input Section === */}


            {/* === START: Set Values Button === */}
            <div className="flex justify-center"> {/* Center the button */}
                <button
                    onClick={handleSetValues} // Connect button click to handler
                    className="px-6 py-2 rounded-md text-lg font-semibold bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-150" // Styling
                >
                    Set PID & Target Values
                </button>
            </div>
            {/* === END: Set Values Button === */}


            {/* Display Calculated PID Output (Read-only) */}
             <div className="mt-8 text-center"> {/* Add margin-top for spacing */}
                <h3 className="text-lg font-medium text-gray-300 mb-2">Calculated PID Output:</h3> {/* Heading */}
                 <p className="text-gray-100 text-3xl font-bold">
                 {calculatedPIDValue !== undefined ? Number(calculatedPIDValue).toFixed(2) : '---'}%                 </p>
             </div>

        </motion.div>
    );
};

export default PIDControls;