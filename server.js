const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the current directory
app.use(express.static(__dirname));

// Route for the root URL
app.get('/', (req, res) => {
    console.log('Serving index.html...');
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Frontend app running at http://localhost:${port}`);
});
