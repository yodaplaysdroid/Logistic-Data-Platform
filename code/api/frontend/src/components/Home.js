import React from "react";
import {
  Sidebar,
  Menu,
  MenuItem,
  SubMenu,
  SidebarHeader,
} from "react-pro-sidebar";

import { Link } from "react-router-dom";

import { Typography } from "@mui/material";

import InputRoundedIcon from "@mui/icons-material/InputRounded";
import StorageRoundedIcon from "@mui/icons-material/StorageRounded";
import Inventory2RoundedIcon from "@mui/icons-material/Inventory2Rounded";
import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import HelpOutlineRoundedIcon from "@mui/icons-material/HelpOutlineRounded";
import DonutSmallRoundedIcon from "@mui/icons-material/DonutSmallRounded";

export default function Home(props) {
  return (
    <>
      <Sidebar width="200px" backgroundColor="aliceblue">
        <Menu>
          <SubMenu
            icon={<InputRoundedIcon />}
            label={<Typography variant="button">Input</Typography>}
          >
            <MenuItem
              icon={<StorageRoundedIcon />}
              component={<Link to="/mysql/" />}
            >
              <Typography variant="button">MySql</Typography>
            </MenuItem>
            <MenuItem
              icon={<Inventory2RoundedIcon />}
              component={<Link to="/minio/" />}
            >
              <Typography variant="button">MinIO</Typography>
            </MenuItem>
            <MenuItem
              icon={<SaveRoundedIcon />}
              component={<Link to="/hdfs/" />}
            >
              <Typography variant="button">HDFS</Typography>
            </MenuItem>
          </SubMenu>
          <MenuItem icon={<DonutSmallRoundedIcon />}>
            <Typography variant="button">Analysis</Typography>
          </MenuItem>
          <MenuItem icon={<HelpOutlineRoundedIcon />}>
            <Typography variant="button">Help</Typography>
          </MenuItem>
        </Menu>
      </Sidebar>
    </>
  );
}
