import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Loading } from 'react-simple-chatbot';

const FetchResponse = ({ steps, triggerNextStep }) => {
    // debugger
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(true);


    async function handleUserInput(userInput) {
        const response = await axios({
            method: 'post',
            url: 'http://localhost/teamcal-ai-chatbot/PHP/index.php',
            data: {
                message: userInput
            },
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            console.log(response.data);
            // return response.data.response;
            setResponse(response.data.response);
            setLoading(false);
            triggerNextStep({ trigger: 'userInput' });
        }).catch(error => {
            console.error('Error:', error);
        });
    }


    useEffect(() => {
        const userInput = steps.userInput.value;
        handleUserInput(userInput).then(res => {
            // debugger
        });
    }, []);

    return loading ? <Loading /> : <span>{response}</span>;
};



export default FetchResponse;
