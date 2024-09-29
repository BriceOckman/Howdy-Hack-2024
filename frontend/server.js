const express = require('express');
const path = require('path');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Set up multer for file uploads
const upload = multer({ dest: 'uploads/' });

// Endpoint for handling file uploads
app.post('/upload', upload.fields([{ name: 'video' }, { name: 'presentation' }]), (req, res) => {
    console.log(req.files); // Log uploaded files for debugging

    // Redirect to result page after processing
    res.redirect('/result.html'); // Ensure this path is correct
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
