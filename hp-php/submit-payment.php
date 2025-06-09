<?php
// submit-payment.php

function generateChecksum($data, $privateKey)
{
    ksort($data);
    $values = [];

    foreach ($data as $key => $value) {
        if (is_array($value) || is_object($value)) {
            $values[] = json_encode($value);
        } else {
            $values[] = $value;
        }
    }

    $concatenatedData = implode(',', $values);
    return hash_hmac('sha256', $concatenatedData, $privateKey);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = $_POST;
    $privateKey = 'add_your_private_key'; // replace with your real key

    // Optional: add redirect_url
    // $data['redirect_url'] = 'http://localhost/redirect.php';

    $checksum = generateChecksum($data, $privateKey);
    $data['checksum'] = $checksum;

    // Setup headers
    $headers = [
        "SecretKey: your_secret_key",
        "XApiKey: your_api_key",
        "Content-Type: application/x-www-form-urlencoded"
    ];

    // Send request to Herepay
    $ch = curl_init('https://uat.herepay.org/api/v1/herepay/initiate');
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        http_response_code(500);
        echo "Error initiating payment: " . curl_error($ch);
    } else {
        echo $response;
    }

    curl_close($ch);
}
