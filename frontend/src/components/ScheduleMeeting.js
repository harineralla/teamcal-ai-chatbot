import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CalendarComponent from './CalendarComponent';

const ScheduleMeetingComponent = ({ triggerNextStep }) => {
    const [title, setTitle] = useState('');
    const [date, setDate] = useState(new Date());
    const [time, setTime] = useState('');
    const [responseMessage, setResponseMessage] = useState();
    // const [triggerFunction, setTriggerFunction] = useState(triggerNextStep);

    useEffect(() => {
        if(responseMessage){
            triggerNextStep({
                value: responseMessage,
                trigger: 'meetingScheduled'
            });
        }
    },[responseMessage])
 
    const handleScheduleMeeting = async () => {
        try {
            const response = await axios({
                method: 'post',
                // url: 'http://localhost:8000/index.php',
                url: 'http://ec2-54-208-43-232.compute-1.amazonaws.com:8000/index.php',
                data: {
                    action: 'schedule_meeting',
                    title,
                    date: date.toDateString(),
                    time
                },
                headers:{
                    'Content-Type': 'application/json'
                },
            });

            const data = response.data;
            setResponseMessage(data.message);
  
        } catch (error) {
            setResponseMessage('Failed to schedule meeting');
        }
    };

    return (
        <div>
            <div>
                <label>Meeting Title:</label>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
            </div>
            <div>
                <label>Meeting Date:</label>
                <CalendarComponent setDate={setDate} />
            </div>
            <div>
                <label>Meeting Time:</label>
                <input type="time" value={time} onChange={(e) => setTime(e.target.value)} />
            </div>
            <button onClick={handleScheduleMeeting}>Schedule Meeting</button>
            {/* <>{responseMessage}</> */}
        </div>
    );
};

export default ScheduleMeetingComponent;