const express = require("express");
const db = require("../db");
const multer = require("multer");
const path = require("path");

const router = express.Router();

/* ================= MULTER CONFIG ================= */
const storage = multer.diskStorage({
    destination: "uploads/",
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage });

/* =====================================================
   =============== ADD CONTRIBUTION ====================
   ===================================================== */
router.post("/add", upload.single("image"), (req, res) => {
    const { user_id, type, category, description, location } = req.body;
    const image_path = req.file ? `/uploads/${req.file.filename}` : null;

    const sql = `
        INSERT INTO contributions
        (user_id, type, category, description, location, image_path, status, ngo_status)
        VALUES (?, ?, ?, ?, ?, ?, 'OPEN', 'PENDING')
    `;

    db.query(
        sql,
        [user_id, type, category, description, location, image_path],
        err => {
            if (err) return res.status(500).json(err);
            res.json({ message: "Contribution added successfully" });
        }
    );
});

/* =====================================================
   =============== USER CONTRIBUTIONS ==================
   ===================================================== */
router.get("/user/:userId", (req, res) => {
    db.query(
        "SELECT * FROM contributions WHERE user_id = ?",
        [req.params.userId],
        (err, results) => {
            if (err) return res.status(500).json(err);
            res.json(results);
        }
    );
});

/* =====================================================
   =============== NGO DASHBOARD (READ-ONLY) ===========
   ===================================================== */

/* ---------- ALL OPEN CONTRIBUTIONS (FIXED) ---------- */
router.get("/open", (req, res) => {
    const sql = `
        SELECT 
            c.*,
            u.email AS user_email,
            u.location AS user_location
        FROM contributions c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.status = 'OPEN'
        ORDER BY c.created_at DESC
    `;

    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results);
    });
});

/* ---------- DISTINCT CATEGORIES ---------- */
router.get("/categories", (req, res) => {
    const sql = `
        SELECT DISTINCT category
        FROM contributions
        WHERE status = 'OPEN'
          AND category IS NOT NULL
          AND TRIM(category) != ''
    `;

    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results.map(r => r.category));
    });
});

/* =====================================================
   =============== ALL LOCATIONS =======================
   ===================================================== */
router.get("/all-locations", (req, res) => {
    const sql = `
        SELECT DISTINCT TRIM(location) AS location
        FROM (
            SELECT location FROM users
            UNION
            SELECT location FROM contributions
        ) AS combined_locations
        WHERE location IS NOT NULL
          AND TRIM(location) != ''
          AND LOWER(TRIM(location)) != 'not specified'
        ORDER BY location ASC
    `;

    db.query(sql, (err, results) => {
        if (err) return res.status(500).json(err);
        res.json(results.map(r => r.location));
    });
});

/* =====================================================
   =============== USER CLOSE CONTRIBUTION =============
   ===================================================== */
router.put("/close/:id", (req, res) => {
    const contributionId = req.params.id;

    db.query(
        "UPDATE contributions SET status='CLOSED' WHERE contribution_id=?",
        [contributionId],
        (err, result) => {
            if (err) return res.status(500).json(err);
            if (result.affectedRows === 0)
                return res.status(404).json({ message: "Contribution not found" });

            res.json({ message: "Contribution closed successfully" });
        }
    );
});

module.exports = router;
