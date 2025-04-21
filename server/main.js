const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");

const app = express();
const PORT = 3000;

// MongoDB connection string
const mongoURL = "mongodb+srv://Sathvika:Shiny123$@cluster0.b6ii3qy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"; // Replace with your MongoDB URL

// Connect to MongoDB
mongoose
  .connect(mongoURL, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Failed to connect to MongoDB", err));

// Define a schema for storing login data
const loginSchema = new mongoose.Schema({
  username: String,
  password: String,
});

// Create a model for the login data
const Login = mongoose.model("Login", loginSchema);

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// API endpoint to handle login
app.post("/api/login", async (req, res) => {
  const { username, password } = req.body;

  // Log the username and password to the terminal
  console.log(`Username: ${username}`);
  console.log(`Password: ${password}`);

  // Store the login data in the database
  const loginData = new Login({ username, password });
  try {
    await loginData.save();
    console.log("Login data saved to database");
  } catch (err) {
    console.error("Error saving login data to database", err);
    return res.status(500).json({ message: "Internal server error" });
  }

  // Send a response back to the client
  if (username === "admin" && password === "admin") {
    res.status(200).json({ message: "Login successful!" });
  } else {
    res.status(401).json({ message: "Invalid username or password." });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
