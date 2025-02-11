import express from "express";
import mysql from "mysql2/promise.js";

const pool = mysql.createPool({
  connectionLimit: 10,
  database: "book_db",
  host: process.env.MYSQL_HOST,
  user: "root",
  password: "admin",
});

const app = express();

app.get("/server2/books", async (req, res) => {
  const query = "SELECT * FROM Book";
  const [books] = await pool.query(query);
  res.setHeader("Content-type", "application/json");
  res.json(books);
});

app.get("/server2/books/:id", async (req, res) => {
  const bookID = req.params.id;
  const query = "SELECT * FROM Book WHERE bookID = ?";
  const [book] = await pool.query(query, [bookID]);
  res.setHeader("Content-type", "application/json");
  res.json(book);
});

app.listen("8080", () => {
  console.log("Node server started");
});

process.on("SIGTERM", async () => {
  console.log("Closing Node connection");
  await client.close();
  process.exit(1);
});

process.on("SIGINT", async () => {
  console.log("Closing Node connection");
  await client.close();
  process.exit(1);
});

export default app;
