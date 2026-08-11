const express = require("express");
const bcrypt = require("bcryptjs");
const db = require("../db");

const router = express.Router();

/* USER SIGNUP */
router.post("/signup", async (req, res) => {
    const { name, email, password, location } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);

    const sql = "INSERT INTO users (name, email, password, location) VALUES (?, ?, ?, ?)";
    db.query(sql, [name, email, hashedPassword, location], (err) => {
        if (err) return res.status(500).json(err);
        res.json({ message: "User registered successfully" });
    });
});

/* USER LOGIN */
router.post("/login", (req, res) => {
    const { email, password } = req.body;

    db.query("SELECT * FROM users WHERE email = ?", [email], async (err, results) => {
        if (results.length === 0) return res.status(401).json({ message: "User not found" });

        const valid = await bcrypt.compare(password, results[0].password);
        if (!valid) return res.status(401).json({ message: "Invalid password" });

        res.json({ message: "Login successful", user: results[0] });
    });
});

module.exports = router;
