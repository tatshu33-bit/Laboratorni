# Laboratorni - Resource Manager

A simple web application for managing learning resources with a clean and modern interface.

## Features

- 📋 **Display Resources**: View all available resources in an organized list
- ➕ **Add Resources**: Submit new resources through an intuitive form
- ✅ **Validation**: Input validation for all form fields including URL validation
- 💬 **Feedback Messages**: Success and error messages for user actions
- 🎨 **Modern Design**: Clean, responsive UI with gradient backgrounds and smooth animations

## Technology Stack

- **Backend**: Node.js with Express
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **Data Storage**: In-memory storage (for demonstration purposes)

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tatshu33-bit/Laboratorni.git
cd Laboratorni
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

Start the server:
```bash
npm start
```

The application will be available at: http://localhost:3000

## Usage

1. **View Resources**: The page automatically loads and displays all available resources
2. **Add New Resource**:
   - Fill in the resource name
   - Add a description
   - Provide a valid URL
   - Click "Add Resource" button
3. **Success/Error Messages**: Messages appear at the top of the page confirming actions or showing errors

## API Endpoints

### GET /api/resources
Retrieves all resources.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Resource Name",
      "description": "Resource Description",
      "url": "https://example.com"
    }
  ]
}
```

### POST /api/resources
Adds a new resource.

**Request Body:**
```json
{
  "name": "Resource Name",
  "description": "Resource Description",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Resource added successfully",
  "data": {
    "id": 4,
    "name": "Resource Name",
    "description": "Resource Description",
    "url": "https://example.com"
  }
}
```

## Project Structure

```
Laboratorni/
├── server.js           # Express server and API endpoints
├── package.json        # Project dependencies
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── public/            # Frontend files
    ├── index.html     # Main HTML page
    ├── styles.css     # Styles and layout
    └── app.js         # JavaScript for API interaction
```

## License

MIT