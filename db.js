const mysql = require("mysql2");

const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "your_db_password",
    database: "civiclinkdb"
});

db.connect(err => {
    if (err) {
        console.error("Database connection failed:", err);
    } else {
        console.log("MySQL Connected");
    }
});

module.exports = db;
