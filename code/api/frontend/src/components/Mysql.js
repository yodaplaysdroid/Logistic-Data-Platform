import React, { useState } from "react";
import ReactDOM from "react-dom";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#d46969",
    },
  },
});

export default function Mysql(props) {
  const [username, setUsername] = useState("root");
  const [password, setPassword] = useState("Owkl.9130");
  const [host, setHost] = useState("localhost");
  const [database, setDatabase] = useState("test");
  const [connection, setConnection] = useState(0);
  const [res, setRes] = useState(<></>);

  function handleConnect() {
    setRes(
      <>
        {res}
        <br />
        Connecting...
      </>
    );
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        password: password,
        host: host,
        database: database,
        test: 1,
      }),
    };
    console.log(requestOptions);
    fetch("/api/mysql/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setRes(
          <>
            {res}
            <br />
            {data.message}
          </>
        );
        data.status === 0 ? setConnection(1) : setConnection(0);
      });
  }

  function handleSubmit() {
    setRes(
      <>
        {res}
        <br />
        Submitting...
      </>
    );
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        password: password,
        host: host,
        database: database,
        test: 0,
      }),
    };
    console.log(requestOptions);
    fetch("/api/mysql/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setRes(
          <>
            {res}
            <br />
            {data.message}
          </>
        );
      });
  }

  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="inputform">
          <div className="item">
            <div className="subtitle">MySql Input</div>
          </div>

          <FormControl>
            <div className="formitem">
              <TextField
                sx={{ width: 200, marginRight: 2 }}
                type="text"
                id="username"
                label="Username"
                variant="outlined"
                defaultValue={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                sx={{ width: 200 }}
                type="password"
                id="password"
                label="Password"
                variant="outlined"
                defaultValue={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </FormControl>

          <FormControl>
            <div className="formitem">
              <TextField
                sx={{ width: 416 }}
                type="text"
                id="host"
                label="Host"
                variant="outlined"
                defaultValue={host}
                onChange={(e) => setHost(e.target.value)}
              />
              <FormHelperText>eg. localhost</FormHelperText>
            </div>
          </FormControl>

          <FormControl>
            <div className="formitem">
              <TextField
                sx={{ width: 416 }}
                type="text"
                id="database"
                label="Database"
                variant="outlined"
                defaultValue={database}
                onChange={(e) => setDatabase(e.target.value)}
              />
              <FormHelperText>eg. myDatabase</FormHelperText>
            </div>
          </FormControl>

          <div className="formitem">
            <Button
              color="primary"
              variant="contained"
              sx={{ width: 180, marginRight: 7 }}
              onClick={handleConnect}
            >
              Test Connection
            </Button>
            {connection === 1 ? (
              <Button
                color="primary"
                variant="contained"
                sx={{ width: 180 }}
                onClick={handleSubmit}
              >
                Submit
              </Button>
            ) : (
              <Button
                color="primary"
                variant="contained"
                disabled
                sx={{ width: 180 }}
                onClick={handleSubmit}
              >
                Submit
              </Button>
            )}
          </div>
        </div>
        <div className="consolepanel">
          <div className="console">{res}</div>
        </div>
      </ThemeProvider>
    </>
  );
}
