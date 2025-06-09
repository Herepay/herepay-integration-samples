const express = require('express');
const path = require('path');
const axios = require('axios');
const crypto = require('crypto');
const app = express();
const PORT = 3000;

// Serve static files from "public" directory
app.use(express.static(path.join(__dirname, 'public')));

function generateChecksum(data, privateKey) {
  const sortedKeys = Object.keys(data).sort();
  const sortedData = {};

  sortedKeys.forEach(key => {
    const value = data[key];
    sortedData[key] = Array.isArray(value) || typeof value === 'object'
      ? JSON.stringify(value)
      : value;
  });

  const concatenatedData = Object.values(sortedData).join(',');
  console.log('Concatenated data:', concatenatedData);
  return crypto.createHmac('sha256', privateKey).update(concatenatedData).digest('hex');
}

app.post('/submit-payment', express.urlencoded({ extended: true }), (req, res) => {
  console.log('Form data:', req.body);
  const data = req.body;
  // append redirect URL to the data
  // data.redirect_url = 'http://localhost:3000/redirect'; // Change to your actual redirect URL
  const privateKey = 'add_your_private_key'; // Replace with your actual private key
  const checksum = generateChecksum(data, privateKey);

  const headers = {
    'SecretKey': 'your_secret_key',
    'XApiKey': 'your_api_key',
  };

  let formData = req.body;
  formData.checksum = checksum;

  const axios = require('axios');
  axios.post('https://uat.herepay.org/api/v1/herepay/initiate', formData, { headers })
    .then(response => {
      res.send(response.data);
    })
    .catch(error => {
      res.status(500).send('Error initiating payment');
    });

});
app.use(express.urlencoded({ extended: true }));
app.post('/redirect', (req, res) => {
  console.log('Redirected to /redirect with form data:', req.body);
  let payload = req.body;
  if (payload.status_code === '00') {
    res.send('Payment successful!');
  } else {
    res.send('Payment failed: ' + payload.message);
  }
});
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
