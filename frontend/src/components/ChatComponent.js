import React from 'react';
import ChatBot from 'react-simple-chatbot';
import FetchResponse from './FetchResponse';

const ChatComponent = () => {
    const steps = [
        {
            id: '1',
            message: 'Hi! What can I help you with today?',
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
            trigger: 'userInput'
        }
    ];

    return (
        <ChatBot steps={steps} floating={true} />
    );
};

export default ChatComponent;
