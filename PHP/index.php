<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Credentials: true");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);

    if (isset($data['action']) && $data['action'] === 'schedule_meeting') {
        $meetingTitle = $data['title'];
        $meetingDate = $data['date'];
        $meetingTime = $data['time'];

        $url = 'http://localhost:5000/schedule_meeting';
        $ch = curl_init($url);
        $payload = json_encode(['title' => $meetingTitle, 'date' => $meetingDate, 'time' => $meetingTime]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpcode >= 200 && $httpcode < 300) {
            echo $response;
        } else {
            echo json_encode(['error' => 'Failed to schedule meeting through Flask.']);
        }
    } else {
        $userMessage = $data['message'];
        // echo $userMessage;
        $url = 'http://flask-app:5000/get_response';
        $ch = curl_init($url);
        $payload = json_encode(['message' => $userMessage]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpcode >= 200 && $httpcode < 300) {
            echo $response;
        } else {
            echo json_encode(['error' => 'Failed to get response from Flask.']);
        }
    }
}
