import React, { useState } from 'react';
import './components.css';


const MeetingScheduled = (props) => {
    console.log("Inside the meeting scheduler", props.previousStep)
    return (
        <div>
            {props.previousStep && props.previousStep.value ? (
                <p>{props.previousStep.value}</p>
            ) : (
                <p>No meeting details available.</p>
            )}
        </div>
    );
};

export default MeetingScheduled;