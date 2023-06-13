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
            <div style={{ fontSize: 28, paddingLeft: 10 }}>Dashboard</div>
          </Button>
        </div>
        <div className="menuheader">Input</div>
        <Grid item xs={4}>
          <Button
            href="/mysql/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <StorageRoundedIcon />
            <div className="menu">MySQL</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/hdfs/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <Inventory2RoundedIcon />
            <div className="menu">HDFS</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/minio/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <SaveRoundedIcon />
            <div className="menu">MinIO</div>
          </Button>
        </Grid>

        <div className="menuheader">Analysis</div>
        <Grid item xs={4}>
          <Button
            href="/ann1/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis1</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann2/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis2</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann3/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis3</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann4/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis4</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann5/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis5</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/ann6/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis6</div>
          </Button>
        </Grid>

        <div className="menuheader">Preferences</div>
        <Grid item xs={4}>
          <Button
            href="/doc/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <HelpOutlineRoundedIcon />
            <div className="menu">Documentation</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button
            href="/settings/"
            color="primary"
            sx={{ borderRadius: 50, paddingLeft: 5 }}
          >
            <SettingsSuggestRoundedIcon />
            <div className="menu">Settings</div>
          </Button>
        </Grid>
      </ThemeProvider>
    </>
  );
}
