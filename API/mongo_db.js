require("dotenv").config(); //get credentials
const mongoose = require("mongoose");

const uri = process.env.MONGO_URI;

mongoose.connect(uri, {dbName: 'app_users'});

const mongo_db = mongoose.connection;

mongo_db.on("error", (err) => {
  console.log(err);
});

mongo_db.once("connected", () => {
  console.log("connected");
});

const userSchema = new mongoose.Schema({
  _id: mongoose.ObjectId,
  username: String,
  firstname: String,
  lastname: String,
  dob: Date,
  teams: [Object],
  gender: String,
  location: String,
  age: Number,
});

const userModel = mongoose.model("user", userSchema);

module.exports = { mongo_db, userModel };
