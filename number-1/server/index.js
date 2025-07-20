const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const path = require("path");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

// In-memory storage for form data
const formDataStorage = [];

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan("combined"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// API Routes
// POST endpoint to submit form data
app.post("/api/submit-data", (req, res) => {
  try {
    const { name, email, message, phone } = req.body;

    // Basic validation
    if (!name || !email || !message) {
      return res.status(400).json({
        error: "Missing required fields",
        message: "Name, email, and message are required",
        required: ["name", "email", "message"],
        received: Object.keys(req.body),
      });
    }

    // Email validation (basic)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        error: "Invalid email format",
        message: "Please provide a valid email address",
      });
    }

    // Create new form entry
    const newEntry = {
      id: Date.now().toString(),
      name: name.trim(),
      email: email.trim(),
      message: message.trim(),
      phone: phone ? phone.trim() : null,
      timestamp: new Date().toISOString(),
    };

    // Store the data
    formDataStorage.push(newEntry);

    // Return success response
    res.status(201).json({
      success: true,
      message: "Form data submitted successfully",
      data: newEntry,
      totalEntries: formDataStorage.length,
    });
  } catch (error) {
    console.error("Error submitting form data:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Failed to submit form data",
    });
  }
});

// GET endpoint to retrieve all stored data
app.get("/api/get-data", (req, res) => {
  try {
    res.status(200).json({
      success: true,
      message: "Data retrieved successfully",
      data: formDataStorage,
      totalEntries: formDataStorage.length,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("Error retrieving data:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Failed to retrieve data",
    });
  }
});

// GET endpoint to retrieve a specific entry by ID
app.get("/api/get-data/:id", (req, res) => {
  try {
    const { id } = req.params;
    const entry = formDataStorage.find((item) => item.id === id);

    if (!entry) {
      return res.status(404).json({
        error: "Entry not found",
        message: `No entry found with ID: ${id}`,
      });
    }

    res.status(200).json({
      success: true,
      message: "Entry retrieved successfully",
      data: entry,
    });
  } catch (error) {
    console.error("Error retrieving entry:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Failed to retrieve entry",
    });
  }
});

// PATCH endpoint to update a specific entry
app.patch("/api/update-data/:id", (req, res) => {
  try {
    const { id } = req.params;
    const { name, email, message, phone } = req.body;

    // Basic validation
    if (!name || !email || !message) {
      return res.status(400).json({
        error: "Missing required fields",
        message: "Name, email, and message are required",
        required: ["name", "email", "message"],
        received: Object.keys(req.body),
      });
    }

    // Email validation (basic)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({
        error: "Invalid email format",
        message: "Please provide a valid email address",
      });
    }

    const entryIndex = formDataStorage.findIndex((item) => item.id === id);

    if (entryIndex === -1) {
      return res.status(404).json({
        error: "Entry not found",
        message: `No entry found with ID: ${id}`,
      });
    }

    // Update the entry
    const updatedEntry = {
      ...formDataStorage[entryIndex],
      name: name.trim(),
      email: email.trim(),
      message: message.trim(),
      phone: phone ? phone.trim() : null,
      updatedAt: new Date().toISOString(),
    };

    formDataStorage[entryIndex] = updatedEntry;

    res.status(200).json({
      success: true,
      message: "Entry updated successfully",
      data: updatedEntry,
      totalEntries: formDataStorage.length,
    });
  } catch (error) {
    console.error("Error updating entry:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Failed to update entry",
    });
  }
});

// DELETE endpoint to remove a specific entry
app.delete("/api/delete-data/:id", (req, res) => {
  try {
    const { id } = req.params;
    const entryIndex = formDataStorage.findIndex((item) => item.id === id);

    if (entryIndex === -1) {
      return res.status(404).json({
        error: "Entry not found",
        message: `No entry found with ID: ${id}`,
      });
    }

    const deletedEntry = formDataStorage.splice(entryIndex, 1)[0];

    res.status(200).json({
      success: true,
      message: "Entry deleted successfully",
      deletedData: deletedEntry,
      totalEntries: formDataStorage.length,
    });
  } catch (error) {
    console.error("Error deleting entry:", error);
    res.status(500).json({
      error: "Internal server error",
      message: "Failed to delete entry",
    });
  }
});

// Serve static files from the Vue.js build (only in production)
if (process.env.NODE_ENV === "production") {
  app.use(express.static(path.join(__dirname, "../client/dist")));

  // Catch all handler: send back Vue's index.html file for any non-API routes
  app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "../client/dist/index.html"));
  });
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: "Something went wrong!",
    message: err.message,
  });
});

app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
  console.log(`API available at http://localhost:${PORT}/api`);
  console.log(`Form data endpoints:`);
  console.log(`POST /api/submit-data - Submit form data`);
  console.log(`GET  /api/get-data - Get all stored data`);
  console.log(`GET  /api/get-data/:id - Get specific entry`);
  console.log(`PATCH /api/update-data/:id - Update specific entry`);
  console.log(`DELETE /api/delete-data/:id - Delete specific entry`);
});
