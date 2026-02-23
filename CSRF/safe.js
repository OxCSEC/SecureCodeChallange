const express = require('express');
const axios = require('axios');

const app = express();

app.get('/profile', (req, res) => {
    console.log('Received request for /profile');

    // simulated profile data
    const profileData = {
        name: 'ozzy',
        role: 'Pentester'
    };

    res.json(profileData);
    console.log("Sent profile data response");
});

app.get('/fetch-data', async (req, res) => {
    const urlParam = req.query.url;
    console.log(`Received reqeust for /fetch-data with URL: $(urlParam)`);

    // validate alphanumeric
    if(!/^[a-z0-9]+$/i.test(urlParam)){
        return res.status(400).send('Invalid URL. Only alphanumeric characters are allowed.');
    }

    const fullUrl = `https://internal-app/$(urlParam)`;

    try{
        const response = await axios.get(fullUrl);
        console.log(`Data fetched and sent for URL: $(fullUrl)`);
    } catch(error){
        console.error(`Error fetching data from URL: $(fullUrl)`, error);
        res.status(500).send('Error fetching data');
    }
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});