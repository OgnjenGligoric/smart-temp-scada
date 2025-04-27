import { motion } from "framer-motion";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { useState, useEffect } from "react";
import { getRecentTemperatures } from "../../../services/api";






const TemperatureOverviewChart = () => {
	const [selectedTimeRange, setSelectedTimeRange] = useState("This Month");

	const [monthlyTemperaturesData,setMonthlyTemperaturesData] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
		  const rawData = await getRecentTemperatures();
		  const formattedData = rawData.map(item => ({
			timestamp: new Date(item.time).getTime(), // Convert to timestamp
			temperature: item.value,
		  }));
		  setMonthlyTemperaturesData(formattedData);
		};
	
		fetchData();
	  }, []);

	console.log(monthlyTemperaturesData)

	return (
		<motion.div
		  className="bg-gray-800 bg-opacity-50 backdrop-blur-md shadow-lg rounded-xl p-6 border border-gray-700 mb-8"
		  initial={{ opacity: 0, y: 20 }}
		  animate={{ opacity: 1, y: 0 }}
		  transition={{ delay: 0.2 }}
		>
		  <div className="flex items-center justify-between mb-6">
			<h2 className="text-xl font-semibold text-gray-100">Temperature Overview</h2>
	
			<select
			  className="bg-gray-700 text-white rounded-md px-3 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
			  value={selectedTimeRange}
			  onChange={(e) => setSelectedTimeRange(e.target.value)}
			>
			  <option>This Week</option>
			  <option>This Month</option>
			  <option>This Quarter</option>
			  <option>This Year</option>
			</select>
		  </div>
	
		  <div className="w-full h-80">
			<ResponsiveContainer>
			  <AreaChart data={monthlyTemperaturesData}>
				<CartesianGrid strokeDasharray="3 3" stroke="#374151" />
				<XAxis
				  dataKey="timestamp"
				  scale="time"
				  type="number"
				  domain={['dataMin', 'dataMax']}
				  tickFormatter={(unixTime) => new Date(unixTime).toLocaleTimeString()}
				  stroke="#9CA3AF"
				/>
				<YAxis stroke="#9CA3AF" domain={[15, 'auto']} />
				<Tooltip
				  labelFormatter={(timestamp) => new Date(timestamp).toLocaleString()}
				  contentStyle={{ backgroundColor: "rgba(31, 41, 55, 0.8)", borderColor: "#4B5563" }}
				  itemStyle={{ color: "#E5E7EB" }}
				/>
				<Area
				  type="monotone"
				  dataKey="temperature"
				  stroke="#8B5CF6"
				  fill="#8B5CF6"
				  fillOpacity={0.3}
				/>
			  </AreaChart>
			</ResponsiveContainer>
		  </div>
		</motion.div>
	  );
};
export default TemperatureOverviewChart;
