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

export default function Minio() {
  const [endpoint, setEndpoint] = useState("localhost:9000");
  const [accesskey, setAccesskey] = useState("minioadmin");
  const [secretkey, setSecretkey] = useState("minioadmin");
  const [bucket, setBucket] = useState("test");
  const [path, setPath] = useState("csv");
  const [filetype, setFileType] = useState("csv");

  function handleConnect() {
    console.log(endpoint);
    console.log(accesskey);
    console.log(secretkey);
    console.log(bucket);
    console.log(path);
    console.log(filetype);
  }

  function handleSubmit() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint: endpoint,
        accesskey: accesskey,
        secretkey: secretkey,
        bucket: bucket,
        path: path,
        filetype: filetype,
      }),
    };
    console.log(requestOptions);
    fetch("/api/minio/", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data));
  }

  return (
    <>
      <div className="item">
        <Typography component="h4" variant="h4" textAlign="left">
          MinIO Input
        </Typography>
      </div>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="endpoint"
              label="Endpoint"
              variant="outlined"
              defaultValue={endpoint}
              onChange={(e) => setEndpoint(e.target.value)}
            />
            <FormHelperText>eg. localhost:9000</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="accesskey"
              label="Access Key"
              variant="outlined"
              defaultValue={accesskey}
              onChange={(e) => setAccesskey(e.target.value)}
            />
            <FormHelperText>eg. minioadmin</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="password"
              id="secretkey"
              label="Secret Key"
              variant="outlined"
              defaultValue={secretkey}
              onChange={(e) => setSecretkey(e.target.value)}
            />
            <FormHelperText>eg. minioadmin</FormHelperText>
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
              <FormControlLabel
                value="excel"
                control={<Radio />}
                label="excel"
              />
            </RadioGroup>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="bucket"
              label="Bucket"
              variant="outlined"
              defaultValue={bucket}
              onChange={(e) => setBucket(e.target.value)}
            />
            <FormHelperText>eg. test</FormHelperText>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <FormControl>
            <TextField
              sx={{ width: 300 }}
              type="text"
              id="path"
              label="Path"
              variant="outlined"
              defaultValue={path}
              onChange={(e) => setPath(e.target.value)}
            />
            <FormHelperText>eg. csv</FormHelperText>
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
