const mysql = require("mysql2");

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "escola",
  database: "ProvaBim"
});

db.connect();

module.exports = db;
