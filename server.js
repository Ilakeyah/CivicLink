const express = require("express");
const cors = require("cors");

const userRoutes = require("./routes/userRoutes");
const ngoRoutes = require("./routes/ngoRoutes");
const contributionRoutes = require("./routes/contributionRoutes");


const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/users", userRoutes);
app.use("/api/ngos", ngoRoutes);
app.use("/api/contributions", contributionRoutes);
app.use("/uploads", express.static("uploads"));
app.use(express.static("public"));


app.listen(3000, () => {
    console.log("Server running on port 3000");
});
