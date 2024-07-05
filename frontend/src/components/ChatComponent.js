import React, { useState } from 'react';
import ChatBot from 'react-simple-chatbot';
import FetchResponse from './FetchResponse';
import ScheduleMeetingComponent from './ScheduleMeeting';
import CalendarComponent from './CalendarComponent';
import MeetingScheduled from './MeetingScheduled';
import './components.css';

// const MeetingScheduled = (props) => {
//     console.log("Inside the meeting scheduler", props)
//     return (
//         <div>
//             <p>{props.previousStep.value}</p>
//         </div>
//     );
// };

const ChatComponent = () => {
    const steps = [
        {
            id: '1',
            message: 'Hi! What can I help you with today?',
            trigger: 'options'
        },
        {
            id: 'options',
            options: [
                { value: 'schedule_meeting', label: 'Schedule meetings', trigger: 'scheduleMeeting' },
                { value: 'check_calendar', label: 'Check calendar', trigger: 'checkCalendar' },
                { value: 'other', label: 'Other', trigger: 'userInput' }
            ]
        },
        {
            id: 'scheduleMeeting',
            message: 'You selected to schedule a meeting. Please provide the details.',
            trigger: 'scheduleMeetingDetails'
        },
        {
            id: 'scheduleMeetingDetails',
            component: <ScheduleMeetingComponent />,
            asMessage: true,
            waitAction: true,
            trigger: 'meetingScheduled'
        },
        {
            id: 'meetingScheduled',
            component: <MeetingScheduled />,
            asMessage: true,
            // waitAction: true,
            trigger: 'userInput'
        },
        {
            id: 'checkCalendar',
            component: <CalendarComponent />,
            asMessage: true,
            trigger: 'userInput'
        },
        {
            id: 'userInput',
            user: true,
            trigger: 'fetchResponse'
        },
        {
            id: 'fetchResponse',
            component: <FetchResponse />,
            asMessage: true,
            waitAction: true,
            trigger: 'options'
        }
    ];

    const customStyle = {
        botBubbleColor: "#fff",
        botFontColor: "#000",
        userBubbleColor: "#f0f0f0",
        userFontColor: "#4a4a4a",
        width: "800px",
        height: "600px"
    };

    return (
        <div style={{ width: '800px', height: '600px' }}>
            <ChatBot steps={steps} floating={true} style={customStyle} />
        </div>
    );
};

export default ChatComponent;
