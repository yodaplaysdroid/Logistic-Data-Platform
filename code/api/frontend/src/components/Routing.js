import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Mysql from "./Mysql";
import Hdfs from "./Hdfs";
import Minio from "./Minio";
import Dashboard from "./Dashboard";

export default function HomePage(props) {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <div className="content">
                  <div className="inputform">
                    <Dashboard />
                  </div>
                </div>
              </>
            }
          />
          <Route
            path="/mysql/"
            element={
              <>
                <div className="content">
                  <div className="inputform">
                    <Mysql />
                  </div>
                </div>
              </>
            }
          />
          <Route
            path="/hdfs/"
            element={
              <>
                <div className="content">
                  <div className="inputform">
                    <Hdfs />
                  </div>
                </div>
              </>
            }
          />
          <Route
            path="/minio/"
            element={
              <>
                <div className="content">
                  <div className="inputform">
                    <Minio />
                  </div>
                </div>
              </>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}
