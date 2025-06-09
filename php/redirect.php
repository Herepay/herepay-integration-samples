<?php
// redirect.php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $payload = $_POST;

    if (isset($payload['status_code']) && $payload['status_code'] === '00') {
        echo 'Payment successful!';
    } else {
        $message = isset($payload['message']) ? $payload['message'] : 'Unknown error';
        echo 'Payment failed: ' . htmlspecialchars($message);
    }
} else {
    echo 'Invalid access.';
}
