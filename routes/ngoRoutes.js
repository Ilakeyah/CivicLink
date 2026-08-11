const express = require("express");
const bcrypt = require("bcryptjs");
const db = require("../db");
const axios = require("axios");

const router = express.Router();

/* ================= NGO SIGNUP ================= */
router.post("/signup", async (req, res) => {
    const { ngo_name, email, password, location, specializations } = req.body;

    try {
        const hashedPassword = await bcrypt.hash(password, 10);

        const sql = `
            INSERT INTO ngos (ngo_name, email, password, location, specializations)
            VALUES (?, ?, ?, ?, ?)
        `;

        db.query(
            sql,
            [ngo_name, email, hashedPassword, location, specializations],
            (err) => {
                if (err) return res.status(500).json(err);
                res.json({ message: "NGO registered successfully" });
            }
        );
    } catch (err) {
        res.status(500).json({ message: "Signup failed" });
    }
});

/* ================= NGO LOGIN ================= */
router.post("/login", (req, res) => {
    const { email, password } = req.body;

    db.query(
        "SELECT * FROM ngos WHERE email = ?",
        [email],
        async (err, results) => {
            if (err) return res.status(500).json(err);
            if (results.length === 0)
                return res.status(401).json({ message: "NGO not found" });

            const valid = await bcrypt.compare(password, results[0].password);
            if (!valid)
                return res.status(401).json({ message: "Invalid password" });

            res.json({
                message: "Login successful",
                ngo: results[0]
            });
        }
    );
});

/* =====================================================
   =============== ML-BASED NGO RECOMMENDATION ==========
   ===================================================== */
router.post("/recommend", async (req, res) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/recommend",
            {
                category: req.body.category,
                description: req.body.description,
                location: req.body.location
            }
        );

        res.json(response.data);
    } catch (error) {
        console.error("ML Service Error:", error.message);
        res.status(500).json({ message: "ML service unavailable" });
    }
});

module.exports = router;
