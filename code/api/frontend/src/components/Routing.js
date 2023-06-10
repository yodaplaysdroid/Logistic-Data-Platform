import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Typography } from "@mui/material";

import Mysql from "./Mysql";
import Hdfs from "./Hdfs";
import Minio from "./Minio";
import Home from "./Home";

export default function HomePage(props) {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <div className="left">
                  <Home />
                </div>
              </>
            }
          />
          <Route
            path="/mysql/"
            element={
              <>
                <div className="left">
                  <Home />
                </div>
                <div className="content">
                  <Mysql />
                </div>
              </>
            }
          />
          <Route
            path="/hdfs/"
            element={
              <>
                <div className="left">
                  <Home />
                </div>
                <div className="content">
                  <Hdfs />
                </div>
              </>
            }
          />
          <Route
            path="/minio/"
            element={
              <>
                <div className="left">
                  <Home />
                </div>
                <div className="content">
                  <Minio />
                </div>
              </>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}
