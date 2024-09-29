const express = require('express');
const path = require('path');
const axios = require('axios');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' }); // Specify the destination for uploaded files

// Endpoint for handling file uploads
app.post('/upload', upload.fields([{ name: 'video' }, { name: 'presentation' }]), (req, res) => {
    // Handle file processing here
    console.log(req.files); // Log uploaded files for debugging

    // Redirect to result page after processing (this can be modified as needed)
    res.redirect('/result.html'); // You may want to add logic to send results instead
});

// Example API endpoint to fetch data from Python backend
app.get('/api/data', async (req, res) => {
    try {
        const response = await axios.get('http://your-python-backend-url/api/data');
        res.json(response.data);
    } catch (error) {
        res.status(500).send('Error fetching data');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
