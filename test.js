// Import the http and fs modules
const http = require("http");
const fs = require("fs");

// Create a server object
const server = http.createServer((req, res) => {
  // Read the file from the given path
  fs.readFile("/tmp/tmp1cm37eq8/converted.html", (err, data) => {
    // Handle errors
    if (err) {
      res.statusCode = 404;
      res.end("File not found");
    } else {
      // Send the file as HTML
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/html");
      res.end(data);
    }
  });
});

// Start the server on port 3000
server.listen(3000, () => {
  console.log("Server running at http://localhost:3000/");
});
