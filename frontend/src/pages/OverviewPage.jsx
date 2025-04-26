import { motion } from "framer-motion";

import Header from "../components/common/Header";
import StatCard from "../components/common/StatCard";
import { Thermometer,User, DoorOpen, Fan } from "lucide-react";
import TemperatureOverviewChart from "../components/charts/TemperatureOverviewChart";
import ModeSelector from "../components/controls/ModeSelector";
import ManualSettings from "../components/controls/ManualSettings";
import PIDControls from "../components/controls/PIDControls";
import AlarmHistory from "../components/controls/AlarmHistory";

const salesStats = {
	totalRevenue: "25°C",
	presenceSwitch: "Active",
	windowSwitch: "Closed",
	salesGrowth: "2",
};

const OverviewPage = () => {
	return (
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
					<StatCard name='Temperature' icon={Thermometer} value={salesStats.totalRevenue} color='#6366F1' />
					<StatCard
						name='Presence switch'
						icon={User}
						value={salesStats.presenceSwitch}
						color='#10B981'
					/>
					<StatCard
						name='Window switch'
						icon={DoorOpen}
						value={salesStats.windowSwitch}
						color='#F59E0B'
					/>
					<StatCard name='Fan speed' icon={Fan} value={salesStats.salesGrowth} color='#EF4444' />
				</motion.div>
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<ModeSelector />
					<ManualSettings />
				</div>
				<div className='grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'>
					<PIDControls />
					<AlarmHistory />
				</div>
				<TemperatureOverviewChart />

	
			</main>
		</div>
	);
};
export default OverviewPage;
