const express = require("express");
const app = express();
const bcrypt = require("bcrypt");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const { mongo, userModel } = require("./mongo_db");
const mongoose = require("mongoose");
const pool = require("./sql_db");

const PORT = process.env.PORT || 5500;

// middleware
app.use(cors());
app.use(express.json()); // => req.body
app.use(express.static("public"));

// Repeated functions

async function querySql(statement, values) {
  const query = await pool.query(statement, values);
  // console.log(query);
  const results = query.rows;
  return results;
}

async function handleParams(branch, params) {
  const statement = "SELECT * FROM " + branch + " WHERE tier=$1 ORDER BY rank ASC LIMIT 25;";
  const results = await querySql(statement, params);
  const output = {
    data: results
  };
  return output;
}

/* ROUTES */

// get the top 25 of the tier.
app.get("/apiv1/current/:tier", async (req, res) => {
  try {
    const { tier } = req.params;
    const output = await handleParams("current", [tier]);
    // console.log(output);
    return res.json(output);
  } catch (error) {
    console.log(error.message);
  }
});

app.get("/apiv1/previous/:tier", async (req, res) => {
  try {
    const { tier } = req.params;
    const output = await handleParams("previous", [tier]);
    res.json(output);
  } catch (error) {
    console.log(error.message);
  }
});

app.get("/apiv1/older/:tier", async (req, res) => {
  try {
    const { tier } = req.params;
    const output = await handleParams("tma", [tier]);
    res.json(output);
  } catch (error) {
    console.log(error.message);
  }
});

// User database interactions

app.post("/apiv1/login", async (req, res) => {
  //Get the login creds from the request
  const { username, password } = req.body;
  console.log(req.body)
  try {
    //Query the database, similar to above, just searching a different table
    const loginQuery =
      "SELECT id, role, mongo_id, username, password FROM users WHERE username = $1";
    const queryRes = await pool.query(loginQuery, [username]);
    const userData = queryRes.rows[0];
    //if it doesn't return a userData, send 404 (Not Found)
    if (!userData) {
      res.json({message: "Please provide username and password."});
    }
    const storedPass = userData.password;
    const validPassword = await bcrypt.compare(password, storedPass);
    // if passwords don't match, send 403 (Unauthorised)
    if (!validPassword) {
      res.json({message: "Invalid login credentials."});
    }
    // get user profile data, this won't be used in this project, but the
    // idea is that the user profile stores user data, such as name, dob etc (all optional except for username)

    // Keeping the profile information separate from the login information is done because
    // SQL is really well designed for logging in, and I'm much more familiar with querying SQL
    // but because user profile data can be wildly varying and the teams key is an array of objects
    // it made sense to use MongoDB for this. While SQL DOES support JSON columns, there can issues
    // using unicode escapes and so on, and as well I believe has slightly more overhead than with NoSQL
    // and also I just wanted to experience working with two databases in a single application.

    //In future use, userProfile will be used to populate a profile page, and save teams, if desired.
    const userProfile = await userModel.findById(userData.mongo_id).exec();
    console.log(userProfile)
    const {_id, __v, ...profile} = userProfile.toObject()
    // console.log(userProfile.toObject())
    //sign token (This isn't used in this application as we aren't using cookies,
    // but in a real-world scenario, or possibly in the future, it might be useful)
    const token = jwt.sign(
      {
        username: userData.username,
        role: userData.role,
        mongo_id: userData.mongo_id,
      },
      "secretkey"
    );
    res.status(200).send({
      username: username,
      role: userData.role,
      mongo_id: userData.mongo_id,
      profileInfo: profile,
      token,
    });
  } catch (error) {
    console.log(error);
  }
});

app.post("/apiv1/register", async (req, res) => {
  const { username, password, email } = req.body;
  try {
    const hashedPass = await bcrypt.hash(password, 10);
    const validCheckQuery = "SELECT 1 FROM users WHERE USERNAME = $1";
    const validCheckRes = await pool.query(validCheckQuery, [username]);
    const validCheck = validCheckRes.rows[0];
    if (validCheck) {
      res.json({
        message: "Username already in use, please choose another username.",
      });
    } else {
      // make mongo DB entry first, to get MongoID
      const newUserId = new mongoose.Types.ObjectId();
      const newUser = new userModel({
        _id: newUserId,
        username: username,
        email: email,
      });
      await newUser.save();
      const strippedID = newUserId.toString(); //without this, mongo_id is wrapped in quotes in the database
      const newPgUserQuery =
        "INSERT INTO users (username, password, mongo_id) VALUES ($1, $2, $3)";
      await pool.query(newPgUserQuery, [
        username,
        hashedPass,
        strippedID,
      ]).then(
        res.status(201).send({ message: `Successfuly registered ${username}` })
      );
    }
  } catch (err) {
    console.log(err);
  }
});

app.post('/apiv1/saveteam', async (req, res) => {
  const {id, username, team} = req.body;
  const user = await userModel.findById(id).exec();
  if (user.teams){
    user.teams.push(team);
  } else {
    user.teams = [team];
  };
  await user.save().then(
    res.status(200).send({message: `Successfully updated ${username}'s teams.`})
  );
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}.`);
});
