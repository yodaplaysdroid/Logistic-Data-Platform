import * as React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";

import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

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
      <div className="item">
        <Typography component="h4" variant="h4" textAlign="left">
          HDFS Input
        </Typography>
      </div>

      <Grid container spacing={2}>
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
              id="port"
              label="Port"
              variant="outlined"
              defaultValue={port}
              onChange={(e) => setPort(e.target.value)}
            />
            <FormHelperText>eg. 9000</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
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
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="directory"
              label="Directory"
              variant="outlined"
              defaultValue={directory}
              onChange={(e) => setDirectory(e.target.value)}
            />
            <FormHelperText>eg. path/to/files</FormHelperText>
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
