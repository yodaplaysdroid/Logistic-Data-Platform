import * as React from "react";
import { useState } from "react";

import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { ThemeProvider, createTheme } from "@mui/material";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

const theme = createTheme({
  palette: {
    primary: {
      main: "#d46969",
    },
  },
});

export default function Hdfs() {
  const [endpoint, setEndpoint] = useState(
    "hadoopa-namenode.damenga-zone.svc:9000"
  );
  const [user, setUser] = useState("root");
  const [table, setTable] = useState("");
  const [directory, setDirectory] = useState("remote:/dir/");
  const [filetype, setFileType] = useState("csv");
  const [sheetname, setSheetname] = useState("");
  const [filename, setFilename] = useState("");
  const [connection, setConnection] = useState(0);
  const [res, setRes] = useState(<></>);

  function handleConnect() {
    setRes(
      <>
        {res}
        <br />
        正在连接...
      </>
    );
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint: endpoint,
        directory: directory,
        filetype: filetype,
        table: table,
        filename: filename,
        sheetname: sheetname,
        test: 1,
      }),
    };
    console.log(requestOptions);
    fetch("/api/hdfs/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setRes(
          <>
            {res}
            <br />[{data.status}]:{data.message}
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
        提交中...
      </>
    );
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        endpoint: endpoint,
        directory: directory,
        filetype: filetype,
        table: table,
        filename: filename,
        sheetname: sheetname,
        test: 0,
      }),
    };
    console.log(requestOptions);
    fetch("/api/hdfs/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setRes(
          <>
            {res}
            <br />[{data.status}]:{data.message}
          </>
        );
      });
  }

  return (
    <>
      <ThemeProvider theme={theme}>
        <div className="inputformouter">
          <div className="inputform">
            <div className="subtitle">HDFS 数据导入</div>

            <FormControl fullWidth>
              <TextField
                sx={{ margin: 2, marginTop: 0 }}
                type="text"
                id="endpoint"
                label="HDFS 平台地址"
                variant="outlined"
                disabled
                defaultValue={endpoint}
                onChange={(e) => setEndpoint(e.target.value)}
              />
            </FormControl>

            <FormControl fullWidth>
              <TextField
                sx={{ margin: 2 }}
                type="text"
                id="user"
                label="用户名"
                variant="outlined"
                disabled
                defaultValue={user}
                onChange={(e) => setUser(e.target.value)}
              />
            </FormControl>

            <FormControl fullWidth>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <div style={{ display: "block" }}>
                  <FormLabel id="filetype" sx={{ marginTop: 2, marginLeft: 2 }}>
                    文件类型
                  </FormLabel>
                  <RadioGroup
                    row
                    sx={{ marginLeft: 2, marginBottom: 2 }}
                    aria-labelledby="filetype"
                    name="filetype"
                    defaultValue={filetype}
                    onChange={(e) => setFileType(e.target.value)}
                  >
                    <FormControlLabel
                      value="csv"
                      control={<Radio />}
                      label="CSV"
                    />
                    <FormControlLabel
                      value="txt"
                      control={<Radio />}
                      label="TSV"
                    />
                    <FormControlLabel
                      value="xls"
                      control={<Radio />}
                      label="EXCEL"
                    />
                  </RadioGroup>
                </div>
                {filetype === "xls" ? (
                  <TextField
                    sx={{ width: "40%", marginRight: 2, marginTop: 2 }}
                    type="text"
                    id="sheetname"
                    label="表格名称"
                    variant="outlined"
                    defaultValue={sheetname}
                    onChange={(e) => setSheetname(e.target.value)}
                  />
                ) : null}
              </div>
            </FormControl>

            <FormControl fullWidth>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <TextField
                  sx={{ width: "70%", margin: 2, marginRight: 1 }}
                  type="text"
                  id="directory"
                  label="目录/"
                  variant="outlined"
                  defaultValue={directory}
                  onChange={(e) => setDirectory(e.target.value)}
                />
                <TextField
                  sx={{ width: "30%", margin: 2, marginLeft: 1 }}
                  type="text"
                  id="filename"
                  label="文件名"
                  variant="outlined"
                  defaultValue={filename}
                  onChange={(e) => setFilename(e.target.value)}
                />
              </div>
            </FormControl>

            <FormControl fullWidth>
              <Select
                sx={{ margin: 2 }}
                defaultValue={""}
                displayEmpty
                inputProps={{ "aria-label": "Without label" }}
                onChange={(e) => setTable(e.target.value)}
              >
                <MenuItem value={""}>输入表选择</MenuItem>
                <MenuItem value={"物流公司"}>物流公司</MenuItem>
                <MenuItem value={"客户信息"}>客户信息</MenuItem>
                <MenuItem value={"物流信息"}>物流信息</MenuItem>
                <MenuItem value={"集装箱动态"}>集装箱动态</MenuItem>
                <MenuItem value={"装货表"}>装货表</MenuItem>
                <MenuItem value={"卸货表"}>卸货表</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <Button
                  color="primary"
                  variant="contained"
                  sx={{ width: "40%", margin: 4, borderRadius: 10 }}
                  onClick={handleConnect}
                >
                  连接测试
                </Button>
                {connection === 1 ? (
                  <Button
                    color="primary"
                    variant="contained"
                    sx={{ width: "40%", margin: 4, borderRadius: 10 }}
                    onClick={handleSubmit}
                  >
                    提交
                  </Button>
                ) : (
                  <Button
                    color="primary"
                    variant="contained"
                    disabled
                    sx={{ width: "40%", margin: 4, borderRadius: 10 }}
                    onClick={handleSubmit}
                  >
                    提交
                  </Button>
                )}
              </div>
            </FormControl>
          </div>
          <div className="consolepanel">
            <div className="console">
              <div style={{ marginLeft: 10 }}>{res}</div>
            </div>
          </div>
        </div>
      </ThemeProvider>
    </>
  );
}
