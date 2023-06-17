import * as React from "react";
import { useState } from "react";

import ArchiveRoundedIcon from "@mui/icons-material/ArchiveRounded";
import UnarchiveRoundedIcon from "@mui/icons-material/UnarchiveRounded";
import CategoryRoundedIcon from "@mui/icons-material/CategoryRounded";
import ApartmentRoundedIcon from "@mui/icons-material/ApartmentRounded";
import Face4RoundedIcon from "@mui/icons-material/Face4Rounded";
import WidgetsRoundedIcon from "@mui/icons-material/WidgetsRounded";
import CloudSyncRoundedIcon from "@mui/icons-material/CloudSyncRounded";

import { Button } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3e2b2b",
    },
  },
});
export default function RecordCount(request) {
  const [t1, setT1] = useState(0);
  const [t2, setT2] = useState(0);
  const [t3, setT3] = useState(0);
  const [t4, setT4] = useState(0);
  const [t5, setT5] = useState(0);
  const [t6, setT6] = useState(0);

  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  };

  fetch("/api/dashboard/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      setT1(data.t1);
      setT2(data.t2);
      setT3(data.t3);
      setT4(data.t4);
      setT5(data.t5);
      setT6(data.t6);
    });

  function handleRefresh() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        refresh: 1,
      }),
    };

    fetch("/api/dashboard/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setT1(data.t1);
        setT2(data.t2);
        setT3(data.t3);
        setT4(data.t4);
        setT5(data.t5);
        setT6(data.t6);
      });
  }
  return (
    <>
      <ThemeProvider theme={theme}>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <ApartmentRoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>物流公司: {t1}</div>
          </Button>
        </div>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <Face4RoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>客户信息: {t2}</div>
          </Button>
        </div>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <CategoryRoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>物流信息: {t3}</div>
          </Button>
        </div>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <WidgetsRoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>集装箱动态: {t4}</div>
          </Button>
        </div>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <UnarchiveRoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>装货表: {t5}</div>
          </Button>
        </div>
        <div>
          <Button color="primary" sx={{ borderRadius: 50 }}>
            <ArchiveRoundedIcon />
            <div style={{ fontSize: 15, paddingLeft: 2 }}>卸货表: {t6}</div>
          </Button>
        </div>
        <div>
          <Button
            color="primary"
            sx={{ borderRadius: 50 }}
            onClick={handleRefresh}
          >
            <CloudSyncRoundedIcon />
          </Button>
        </div>
      </ThemeProvider>
    </>
  );
}
