const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// In-memory storage for resources
let resources = [
  { id: 1, name: 'JavaScript Tutorial', description: 'Learn modern JavaScript', url: 'https://javascript.info' },
  { id: 2, name: 'Node.js Documentation', description: 'Official Node.js docs', url: 'https://nodejs.org/docs' },
  { id: 3, name: 'Express Guide', description: 'Building web apps with Express', url: 'https://expressjs.com/guide' }
];

let nextId = 4;

// API Routes

// GET all resources
app.get('/api/resources', (req, res) => {
  res.json({ success: true, data: resources });
});

// POST new resource
app.post('/api/resources', (req, res) => {
  const { name, description, url } = req.body;

  // Validation
  if (!name || !description || !url) {
    return res.status(400).json({ 
      success: false, 
      message: 'Please provide name, description, and url' 
    });
  }

  // Basic URL validation
  try {
    new URL(url);
  } catch (error) {
    return res.status(400).json({ 
      success: false, 
      message: 'Please provide a valid URL' 
    });
  }

  const newResource = {
    id: nextId++,
    name: name.trim(),
    description: description.trim(),
    url: url.trim()
  };

  resources.push(newResource);
  
  res.status(201).json({ 
    success: true, 
    message: 'Resource added successfully',
    data: newResource 
  });
});

// Serve index.html for root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
