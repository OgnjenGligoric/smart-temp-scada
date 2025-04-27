import { useEffect } from "react";
import { io } from "socket.io-client"; // Import socket.io-client

const WebSocketListener = ({ url, onMessage }) => {
  useEffect(() => {
    // Connect to the Socket.IO server
    const socket = io(url, {
      transports: ['websocket'], // Ensuring it uses WebSocket for transport (for performance and reliability)
      cors: {
        origin: "http://localhost:5001", // Allow connections from any origin (you may restrict this in production)
        methods: ["GET", "POST"]
      }
    });
    // Listen for messages from the server
    socket.on('message', (data) => {
      onMessage(data); // Handle the incoming message
    });

    // Optionally, listen for a custom event
    socket.on('my response', (data) => {
      console.log('Received custom event data:', data);
    });

    return () => {
    };
  }, [url, onMessage]);

  return null;
};

export default WebSocketListener;
