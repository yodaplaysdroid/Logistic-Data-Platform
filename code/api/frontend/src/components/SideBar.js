import React from "react";

import StorageRoundedIcon from "@mui/icons-material/StorageRounded";
import Inventory2RoundedIcon from "@mui/icons-material/Inventory2Rounded";
import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import HelpOutlineRoundedIcon from "@mui/icons-material/HelpOutlineRounded";
import DonutSmallRoundedIcon from "@mui/icons-material/DonutSmallRounded";
import SettingsSuggestRoundedIcon from "@mui/icons-material/SettingsSuggestRounded";
import DirectionsBoatFilledRoundedIcon from "@mui/icons-material/DirectionsBoatFilledRounded";

import { createTheme, ThemeProvider } from "@mui/material/styles";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3e2b2b",
    },
  },
});

export default function SideBar(props) {
  return (
    <>
      <ThemeProvider theme={theme}>
        <div id="sidebarheader">
          <Button
            href="/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 2, paddingRight: 2 }}
          >
            <DirectionsBoatFilledRoundedIcon fontSize="large" />
            <div style={{ fontSize: 28, paddingLeft: 10 }}>主页</div>
          </Button>
        </div>
        <div className="menuheader">数据导入</div>
        <Grid item xs={4}>
          <Button
            href="/mysql/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <StorageRoundedIcon />
            <div className="menu">MySQL数据迁移</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/hdfs/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <Inventory2RoundedIcon />
            <div className="menu">HDFS数据导入</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/minio/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <SaveRoundedIcon />
            <div className="menu">MinIO数据导入</div>
          </Button>
        </Grid>

        <div className="menuheader">数据分析</div>
        <Grid item xs={4}>
          <Button
            href="/ann1/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">港口吞吐量</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann2/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">货物吞吐量趋势</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann3/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">货物吞吐量同比环比</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann4/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">货物吞吐量占比</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann5/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">货物流向</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann6/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">货物堆场流转周期</div>
          </Button>
        </Grid>

        <div className="menuheader">其他</div>
        <Grid item xs={4}>
          <Button
            href="/doc/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <HelpOutlineRoundedIcon />
            <div className="menu">文档</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/settings/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <SettingsSuggestRoundedIcon />
            <div className="menu">设置</div>
          </Button>
        </Grid>
      </ThemeProvider>
    </>
  );
}
