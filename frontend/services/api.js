const API_URL = 'http://localhost:5000';

export const sendModeChange = async (newMode) => {
    try {
      const response = await fetch(`${API_URL}/mode`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mode: newMode }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        console.error('Failed to change mode:', errorData.error || response.statusText);
        return;
      }
  
      const responseData = await response.json();
      console.log('Mode changed successfully:', responseData.mode);
    } catch (error) {
      console.error('Error sending mode change:', error);
    }
  };

  export const sendFanSpeedChange = async (fanSpeed) => {
    try {
      const response = await fetch(`${API_URL}/manual_speed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ speed: fanSpeed }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Failed to change fan speed:', errorData.error || response.statusText);
        return;
      }

      const responseData = await response.json();
      console.log('Fan speed changed successfully:', responseData.fan_speed);
    } catch (error) {
      console.error('Error sending fan speed change:', error);
    }
  };

  export const sendPIDSettings = async (kp, ki, kd, targetTemp) => {
    try {
        const kpValue = parseFloat(kp);
        const kiValue = parseFloat(ki);
        const kdValue = parseFloat(kd);
        const targetTempValue = parseFloat(targetTemp);

        const requestBody = { 
            kp: kpValue,
            ki: kiValue,
            kd: kdValue,
            target_temp: targetTempValue,
        };

        const response = await fetch(`${API_URL}/pid_params`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            let errorText = `HTTP ${response.status} ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorText = errorData.error || errorText;
            } catch (jsonError) {
                console.warn('No JSON body in error response');
            }
            console.error('Failed to change PID settings:', errorText);
            return;
        }

        const responseData = await response.json();
        console.log('PID settings changed successfully:', responseData);

    } catch (error) {
        console.error('Error sending PID settings:', error);
    }
}


export const getRecentTemperatures = async () => {
    try {
      const response = await fetch(`${API_URL}/influx/temperature`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        let errorText = `HTTP ${response.status} ${response.statusText}`;
        try {
          const errorData = await response.json();
          errorText = errorData.error || errorText;
        } catch (jsonError) {
          console.warn('No JSON body in error response');
        }
        console.error('Failed to fetch temperatures:', errorText);
        return;
      }
  
      const temperatures = await response.json();
      console.log('Recent temperatures fetched successfully:', temperatures);
      return temperatures;
  
    } catch (error) {
      console.error('Error fetching recent temperatures:', error);
    }
  };
  