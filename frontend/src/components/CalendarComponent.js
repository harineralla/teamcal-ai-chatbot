import React, { useState } from 'react';
import Calendar from 'react-calendar';


const CalendarComponent = ({ setDate }) => {
    const [date, selectDate] = useState(new Date());

    const onChange = date => {
        selectDate(date);
        setDate(date);
    };

    return (
        <div>
            <Calendar onChange={onChange} value={date} />
            <p>Selected date: {date.toDateString()}</p>
        </div>
    );
};

export default CalendarComponent