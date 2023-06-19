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

export default function Analysis5(request) {
  const [col, setCol] = useState("");
  const [val, setVal] = useState("");
  const [res, setRes] = useState([]);
  function handleColChange(e) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: `select distinct ${e.target.value} from 分析五`,
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
    setCol(e.target.value);
  }
  function handleSubmit(e) {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        col: col,
        val: val,
      }),
    };
    fetch("/api/ann5/", requestOptions).then((response) => response.json());
  }
  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="selection1">
          <FormControl>
            <Select
              labelId="col"
              id="col"
              size="small"
              sx={{ width: 100 }}
              displayEmpty
              defaultValue={""}
              inputProps={{ "aria-label": "Without label" }}
              onChange={handleColChange}
            >
              <MenuItem value={""}>筛选</MenuItem>
              <MenuItem value={"堆存港口"}>堆存港口</MenuItem>
              <MenuItem value={"货物名称"}>货物名称</MenuItem>
            </Select>
          </FormControl>
          <FormControl>
            {col === "" ? (
              <Select
                labelId="val"
                id="val"
                size="small"
                sx={{ width: 100 }}
                displayEmpty
                disabled
                defaultValue={""}
                inputProps={{ "aria-label": "Without label" }}
              >
                <MenuItem value={""}>选择</MenuItem>
              </Select>
            ) : (
              <Select
                labelId="val"
                id="val"
                size="small"
                sx={{ width: 100 }}
                displayEmpty
                defaultValue={""}
                inputProps={{ "aria-label": "Without label" }}
                onChange={(e) => {
                  setVal(e.target.value);
                }}
              >
                <MenuItem value={""}>筛选</MenuItem>
                {res.map((item, index) => (
                  <MenuItem value={item}>{item}</MenuItem>
                ))}
              </Select>
            )}
          </FormControl>
          {val !== "" ? (
            <FormControl>
              <Button
                color="primary"
                variant="contained"
                sx={{ width: 100, borderRadius: 10 }}
                onClick={handleSubmit}
              >
                提交
              </Button>
            </FormControl>
          ) : (
            <FormControl>
              <Button
                color="primary"
                variant="contained"
                disabled
                sx={{ width: 100, borderRadius: 10 }}
              >
                提交
              </Button>
            </FormControl>
          )}
        </div>
        <div className="mainpanel">
          <iframe
            src="https://datav.dameng.com/dataview/publish/page.html?pageId=1670663863973978113&isTemplate=0"
            width="1110"
            height="560"
            frameBorder="0"
          ></iframe>
        </div>
      </ThemeProvider>
    </>
  );
}
