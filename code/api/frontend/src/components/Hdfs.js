import * as React from "react";
import { useState } from "react";

import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import Button from "@mui/material/Button";
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#d46969",
    },
  },
});

export default function Hdfs() {
  const [host, setHost] = useState("localhost");
  const [port, setPort] = useState("9000");
  const [directory, setDirectory] = useState("");
  const [filetype, setFileType] = useState("csv");

  function handleConnect() {
    console.log(host);
    console.log(port);
    console.log(directory);
    console.log(filetype);
  }

  function handleSubmit() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        host: host,
        port: port,
        directory: directory,
        filetype: filetype,
      }),
    };
    console.log(requestOptions);
    fetch("/api/hdfs/", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data));
  }

  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="item">
          <div className="subtitle">HDFS Input</div>
        </div>

        <FormControl>
          <div className="formitem">
            <TextField
              sx={{ width: 300, marginRight: 2 }}
              type="text"
              id="host"
              label="Host"
              variant="outlined"
              defaultValue={host}
              onChange={(e) => setHost(e.target.value)}
            />
            <TextField
              sx={{ width: 100 }}
              type="text"
              id="port"
              label="Port"
              variant="outlined"
              defaultValue={port}
              onChange={(e) => setPort(e.target.value)}
            />
          </div>
        </FormControl>
        <div className="formitem">
          <FormControl>
            <FormLabel id="filetype">File Type</FormLabel>
            <RadioGroup
              row
              aria-labelledby="filetype"
              name="filetype"
              defaultValue={filetype}
              onChange={(e) => setFileType(e.target.value)}
            >
              <FormControlLabel value="csv" control={<Radio />} label="csv" />
              <FormControlLabel value="txt" control={<Radio />} label="txt" />
            </RadioGroup>
          </FormControl>
        </div>
        <div className="formitem">
          <FormControl>
            <TextField
              sx={{ width: 416 }}
              type="text"
              id="directory"
              label="Directory"
              variant="outlined"
              defaultValue={directory}
              onChange={(e) => setDirectory(e.target.value)}
            />
            <FormHelperText>eg. path/to/files</FormHelperText>
          </FormControl>
        </div>
        <div className="formitem">
          <Button
            color="primary"
            variant="contained"
            sx={{ width: 180, marginRight: 7 }}
            onClick={handleConnect}
          >
            Test Connection
          </Button>

          <Button
            color="primary"
            variant="contained"
            sx={{ width: 180 }}
            onClick={handleSubmit}
          >
            Submit
          </Button>
        </div>
      </ThemeProvider>
    </>
  );
}
