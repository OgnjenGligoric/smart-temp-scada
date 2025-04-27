import { motion } from "framer-motion";
import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import { Thermometer,User, DoorOpen, Fan } from "lucide-react";
import TemperatureOverviewChart from "../components/charts/TemperatureOverviewChart";
import ModeSelector from "../components/controls/ModeSelector";
import ManualSettings from "../components/controls/ManualSettings";
import PIDControls from "../components/controls/PIDControls";
import AlarmHistory from "../components/controls/AlarmHistory";
import WebSocketListener from "../components/controls/WebSocketListener";
import { useState } from "react";
import { useRef } from "react";

import {sendModeChange} from "../../services/api";
import {Toaster, toast} from 'react-hot-toast';




const OverviewPage = () => {
	const RATE_LIMIT_MS = 1000; // 1 second

	const lastAlarmTimeRef = useRef(0);

	const [message, setMessage] = useState(null);
	const [alarms, setAlarms] = useState([]);

	const [status,setStatus] = useState({
		temperature: "25°C",
		presenceSwitch: "Active",
		windowSwitch: "Closed",
		fanSpeed: "2",
		mode: "manual",
		pidValue: "0",
	});

	const apiModeToMode = {
		manual: "manual",
		auto: "auto_3speed",
		pid: "auto_pid",
	  };
	  

	const handleMessageReceived = (data) => {
		
		console.log("Incoming data: ", data)
		// Parse the incoming data and update the state accordingly
		try {
			const parsedData = data
			setStatus((prevStatus) => ({
				...prevStatus,
				temperature: parsedData.temperature || prevStatus.temperature,
				presenceSwitch: parsedData.switch_someone_present === 'on' ? 'Active' : 'Inactive',
				windowSwitch: parsedData.switch_window === 'on' ? 'Active' : 'Inactive',
				fanSpeed: (parsedData.leds_on & parsedData.leds_on.toString()) || prevStatus.fanSpeed,
				mode: apiModeToMode[parsedData.mode] || prevStatus.mode,
				pidValue: parsedData.pid_value || prevStatus.pidValue,
			}));
		} catch (error) {
			console.error("Error parsing message:", error);
		}
	};

	const sendModeChangeToServer = (newMode) => {
		const modeMapping = {
			manual: 'manual',
			auto_3speed: 'auto',
			auto_pid: 'pid',
			// These two don't exist on backend:
			off: null,
			eco: null,
		  };
		
		const backendMode = modeMapping[newMode];
		
		if (!backendMode) {
			console.warn(`Mode "${newMode}" is not supported by backend, skipping API call.`);
			return;
		}
		  
		sendModeChange(backendMode)
		.then(() => {
			console.log("Mode change sent successfully:", newMode);
		})
	}

	return (

		<>
		<Toaster
			position='bottom-left'
			reverseOrder={false}
			/>

		<div className='flex-1 overflow-auto relative z-10'>
			<Header title='SCADA Dashboard' />

			<main className='max-w-7xl mx-auto py-6 px-4 lg:px-8'>
				{/* SALES STATS */}
				<motion.div
					className='grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 1 }}
				>
					<StatCard name='Temperature' icon={Thermometer} value={status.temperature} color='#6366F1' />
					<StatCard
						name='Presence switch'
						icon={User}
						value={status.presenceSwitch}
						color='#10B981'
					/>
					<StatCard
						name='Window switch'
						icon={DoorOpen}
						value={status.windowSwitch}
						color='#F59E0B'
					/>
					<StatCard name='Fan speed' icon={Fan} value={status.fanSpeed} color='#EF4444' />
				</motion.div>
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<ModeSelector 
					currentMode={status.mode}
					onModeChange={(newMode) => {
						// Handle when the user manually selects a mode
						setStatus((prev) => ({ ...prev, mode: newMode }));
				  
						// Optional: Send the new mode to the server if needed
						sendModeChangeToServer(newMode);
					  }}/>
					<ManualSettings />
				</div>
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<PIDControls calculatedPIDValue={status.pidValue} />
					<AlarmHistory alarmHistory={alarms} />
				</div>
				<TemperatureOverviewChart />

	
			</main>
			<WebSocketListener
				url="ws://localhost:5001"
				onMessage={(data) => {
					if (!data.alarmDescription){
						console.log("Received:", data);
						handleMessageReceived(data);
						setMessage(data);
					}
					// its an alarm, do something with it 
					else {
						const now = Date.now();
						if (now - lastAlarmTimeRef.current > RATE_LIMIT_MS) {
							console.log("Alarm received: ", data);
							setAlarms((prevAlarms) => [data, ...prevAlarms]);
							lastAlarmTimeRef.current = now;
							toast.error(`ALARM: ${data.alarmDescription}`);
						} else {
							console.log("Alarm dropped due to rate limit");
						}
					}

				}}
			/>
		</div>

		</>
	);
};
export default OverviewPage;
