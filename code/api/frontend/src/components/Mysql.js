import React, { useState } from "react";
import ReactDOM from "react-dom";

import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import { Link } from "react-router-dom";

export default function Mysql(props) {
  const [username, setUsername] = useState("root");
  const [password, setPassword] = useState("Owkl.9130");
  const [host, setHost] = useState("localhost");
  const [database, setDatabase] = useState("test");

  function handleConnect() {
    console.log(username);
    console.log(password);
    console.log(host);
    console.log(database);
  }

  function handleSubmit() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        password: password,
        host: host,
        database: database,
      }),
    };
    console.log(requestOptions);
    fetch("/api/mysql/", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data));
  }

  return (
    <>
      <div className="item">
        <Typography component="h4" variant="h4" textAlign="left">
          MySql Input
        </Typography>
      </div>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="username"
              label="Username"
              variant="outlined"
              defaultValue={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <FormHelperText>eg. root</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="password"
              id="password"
              label="Password"
              variant="outlined"
              defaultValue={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <FormHelperText>eg. admin</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="host"
              label="Host"
              variant="outlined"
              defaultValue={host}
              onChange={(e) => setHost(e.target.value)}
            />
            <FormHelperText>eg. localhost</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="database"
              label="Database"
              variant="outlined"
              defaultValue={database}
              onChange={(e) => setDatabase(e.target.value)}
            />
            <FormHelperText>eg. test</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <Button color="primary" variant="contained" onClick={handleConnect}>
            Test Connection
          </Button>
        </Grid>

        <Grid item xs={12}>
          <Button color="primary" variant="contained" onClick={handleSubmit}>
            Submit
          </Button>
        </Grid>

        <Grid item xs={12}>
          <Button color="secondary" variant="contained" to="/" component={Link}>
            Back
          </Button>
        </Grid>
      </Grid>
    </>
  );
}
