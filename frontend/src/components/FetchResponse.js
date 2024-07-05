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
            // url: 'http://localhost/teamcal-ai-chatbot/PHP/index.php',
            // url: 'http://localhost:8080/chatbot',
            // url: 'http://localhost:8000/index.php',
            url: 'ec2-54-208-43-232.compute-1.amazonaws.com//:8000/index.php',
            data: {
                message: userInput
            },
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            // withCredentials: true,
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
