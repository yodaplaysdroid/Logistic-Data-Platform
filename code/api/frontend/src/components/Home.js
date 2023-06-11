import React from "react";

import { Link } from "react-router-dom";

import StorageRoundedIcon from "@mui/icons-material/StorageRounded";
import Inventory2RoundedIcon from "@mui/icons-material/Inventory2Rounded";
import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import HelpOutlineRoundedIcon from "@mui/icons-material/HelpOutlineRounded";
import DonutSmallRoundedIcon from "@mui/icons-material/DonutSmallRounded";
import SettingsSuggestRoundedIcon from "@mui/icons-material/SettingsSuggestRounded";

import { createTheme, ThemeProvider } from "@mui/material/styles";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";

const theme = createTheme({
  palette: {
    primary: {
      main: "#000000",
      light: "#505050",
    },
  },
});

export default function Home(props) {
  return (
    <>
      <ThemeProvider theme={theme}>
        <div id="sidebarheader">Dashboard</div>
        <div className="menuheader">Input</div>
        <Grid item xs={4}>
          <Button href="/mysql/">
            <StorageRoundedIcon />
            <div className="menu">MySQL</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/hdfs/">
            <Inventory2RoundedIcon />
            <div className="menu">HDFS</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/minio/">
            <SaveRoundedIcon />
            <div className="menu">MinIO</div>
          </Button>
        </Grid>

        <div className="menuheader">Analysis</div>
        <Grid item xs={4}>
          <Button href="/ann1/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis1</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/ann2/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis2</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/ann3/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis3</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/ann4/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis4</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/ann5/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis5</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/ann6/">
            <DonutSmallRoundedIcon />
            <div className="menu">Analysis6</div>
          </Button>
        </Grid>

        <div className="menuheader">Preferences</div>
        <Grid item xs={4}>
          <Button href="/doc/">
            <HelpOutlineRoundedIcon />
            <div className="menu">Documentation</div>
          </Button>
        </Grid>
        <Grid item xs={4}>
          <Button href="/settings/">
            <SettingsSuggestRoundedIcon />
            <div className="menu">Settings</div>
          </Button>
        </Grid>
      </ThemeProvider>
    </>
  );
}
