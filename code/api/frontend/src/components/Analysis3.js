import * as React from "react";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import { useState } from "react";
import { Button } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#d46969",
    },
  },
});

export default function Analysis3(request) {
  const [status, setStatus] = useState(0);
  const [res, setRes] = useState([]);
  const [res1, setRes1] = useState([]);
  const [year1, setYear1] = useState("");
  const [month1, setMonth1] = useState("");
  const [year2, setYear2] = useState("");
  const [month2, setMonth2] = useState("");

  function handleSubmit(e) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        year1: year1,
        month1: month1,
        year2: year2,
        month2: month2,
      }),
    };
    fetch("/api/ann3/", requestOptions).then((response) => response.json());
  }
  if (status == 0) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "select distinct substring(年月, 1, 4) from 分析三",
      }),
    };
    fetch("/api/query/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        let temp = [];
        for (let r in data) {
          temp.push(r);
          setRes(temp);
        }
      });
    const requestOptions1 = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "select distinct substring(年月, 6, 2) from 分析三",
      }),
    };
    fetch("/api/query/", requestOptions1)
      .then((response) => response.json())
      .then((data) => {
        let temp = [];
        for (let r in data) {
          temp.push(r);
          setRes1(temp);
          setStatus(1);
        }
      });
  }
  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="selection">
          <FormControl fullWidth>
            <Select
              labelId="year1"
              id="year1"
              size="small"
              sx={{ width: 100 }}
              displayEmpty
              defaultValue={""}
              inputProps={{ "aria-label": "Without label" }}
              onChange={(e) => {
                setYear1(e.target.value);
              }}
            >
              <MenuItem value={""}>年1</MenuItem>
              {res.map((item, index) => (
                <MenuItem value={item}>{item}</MenuItem>
              ))}
            </Select>
            <Select
              labelId="month1"
              id="month1"
              size="small"
              sx={{ width: 100 }}
              displayEmpty
              defaultValue={""}
              inputProps={{ "aria-label": "Without label" }}
              onChange={(e) => {
                setMonth1(e.target.value);
              }}
            >
              <MenuItem value={""}>月1</MenuItem>
              {res1.map((item, index) => (
                <MenuItem value={item}>{item}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <Select
              labelId="year2"
              id="year2"
              size="small"
              sx={{ width: 100, marginTop: 1 }}
              displayEmpty
              defaultValue={""}
              inputProps={{ "aria-label": "Without label" }}
              onChange={(e) => {
                setYear2(e.target.value);
              }}
            >
              <MenuItem value={""}>年2</MenuItem>
              {res.map((item, index) => (
                <MenuItem value={item}>{item}</MenuItem>
              ))}
            </Select>
            <Select
              labelId="month2"
              id="month2"
              size="small"
              sx={{ width: 100 }}
              displayEmpty
              defaultValue={""}
              inputProps={{ "aria-label": "Without label" }}
              onChange={(e) => {
                setMonth2(e.target.value);
              }}
            >
              <MenuItem value={""}>月2</MenuItem>
              {res1.map((item, index) => (
                <MenuItem value={item}>{item}</MenuItem>
              ))}
            </Select>
          </FormControl>
          {(year1 !== "" && year2 !== "") || (year1 === "" && year2 === "") ? (
            <FormControl fullWidth>
              <Button
                color="primary"
                variant="contained"
                sx={{ width: 100, borderRadius: 10, marginTop: 2 }}
                onClick={handleSubmit}
              >
                提交
              </Button>
            </FormControl>
          ) : (
            <FormControl fullWidth>
              <Button
                color="primary"
                variant="contained"
                disabled
                sx={{ width: 100, borderRadius: 10, marginTop: 2 }}
                onClick={handleSubmit}
              >
                提交
              </Button>
            </FormControl>
          )}
        </div>
        <div className="mainpanel">
          <iframe
            src="https://datav.dameng.com/dataview/publish/page.html?pageId=1670457086149926913&isTemplate=0"
            width="1110"
            height="560"
            frameBorder="0"
          ></iframe>
        </div>
      </ThemeProvider>
    </>
  );
}
