import React, { useState } from "react";
import ReactDOM from "react-dom";
import axios from "axios";

import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormHelperText from "@mui/material/FormHelperText";
import FormControl from "@mui/material/FormControl";
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

export default function Mysql(props) {
  const [username, setUsername] = useState("mysqluser");
  const [password, setPassword] = useState("Dameng123");
  const [host, setHost] = useState("mysqla-mysqld.damenga-zone.svc");
  const [database, setDatabase] = useState("cnsoft");
  const [inputtable, setInputtable] = useState("");
  const [outputtable, setOutputtable] = useState("");
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
        username: username,
        password: password,
        host: host,
        database: database,
        inputtable: inputtable,
        outputtable: outputtable,
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
        username: username,
        password: password,
        host: host,
        database: database,
        inputtable: inputtable,
        outputtable: outputtable,
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
            <div className="subtitle">MySql 数据迁移</div>
            <FormControl fullWidth>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <TextField
                  sx={{ width: "48%", margin: 2, marginRight: 1 }}
                  type="text"
                  id="username"
                  label="用户名"
                  variant="outlined"
                  defaultValue={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                  sx={{ width: "48%", margin: 2, marginLeft: 1 }}
                  type="password"
                  id="password"
                  label="密码"
                  variant="outlined"
                  defaultValue={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </FormControl>

            <FormControl fullWidth>
              <TextField
                sx={{ margin: 2 }}
                type="text"
                id="host"
                label="MySql 平台主机地址"
                variant="outlined"
                defaultValue={host}
                onChange={(e) => setHost(e.target.value)}
              />
            </FormControl>

            <FormControl fullWidth>
              <TextField
                sx={{ margin: 2 }}
                type="text"
                id="database"
                label="数据库"
                variant="outlined"
                defaultValue={database}
                onChange={(e) => setDatabase(e.target.value)}
              />
            </FormControl>

            <FormControl fullWidth>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <TextField
                  sx={{ width: "60%", margin: 2, marginRight: 1 }}
                  type="text"
                  id="inputtable"
                  label="MySql 输入表名"
                  variant="outlined"
                  onChange={(e) => setInputtable(e.target.value)}
                />
                <Select
                  sx={{ width: "40%", margin: 2, marginLeft: 1 }}
                  defaultValue={""}
                  displayEmpty
                  inputProps={{ "aria-label": "Without label" }}
                  onChange={(e) => setOutputtable(e.target.value)}
                >
                  <MenuItem value={""}>输入表选择</MenuItem>
                  <MenuItem value={"物流公司"}>物流公司</MenuItem>
                  <MenuItem value={"客户信息"}>客户信息</MenuItem>
                  <MenuItem value={"物流信息"}>物流信息</MenuItem>
                  <MenuItem value={"集装箱动态"}>集装箱动态</MenuItem>
                  <MenuItem value={"装货表"}>装货表</MenuItem>
                  <MenuItem value={"卸货表"}>卸货表</MenuItem>
                </Select>
              </div>
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
                  sx={{ width: "40%", margin: 5, borderRadius: 10 }}
                  onClick={handleConnect}
                >
                  连接测试
                </Button>
                {connection === 1 ? (
                  <Button
                    color="primary"
                    variant="contained"
                    sx={{ width: "40%", margin: 5, borderRadius: 10 }}
                    onClick={handleSubmit}
                  >
                    提交
                  </Button>
                ) : (
                  <Button
                    color="primary"
                    variant="contained"
                    disabled
                    sx={{ width: "40%", margin: 5, borderRadius: 10 }}
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
