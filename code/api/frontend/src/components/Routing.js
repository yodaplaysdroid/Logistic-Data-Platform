import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Mysql from "./Mysql";
import Hdfs from "./Hdfs";
import Minio from "./Minio";
import Dashboard from "./Dashboard";
import Analysis1 from "./Analysis1";
import Analysis2 from "./Analysis2";
import Analysis3 from "./Analysis3";
import Analysis4 from "./Analysis4";
import Analysis5 from "./Analysis5";
import Analysis6 from "./Analysis6";
import Documentation from "./Documentation";
import Settings from "./Settings";

export default function HomePage(props) {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Dashboard />
              </>
            }
          />
          <Route
            path="/mysql/"
            element={
              <>
                <Mysql />
              </>
            }
          />
          <Route
            path="/hdfs/"
            element={
              <>
                <Hdfs />
              </>
            }
          />
          <Route
            path="/minio/"
            element={
              <>
                <Minio />
              </>
            }
          />
          <Route
            path="/ann1/"
            element={
              <>
                <Analysis1 />
              </>
            }
          />
          <Route
            path="/ann2/"
            element={
              <>
                <Analysis2 />
              </>
            }
          />
          <Route
            path="/ann3/"
            element={
              <>
                <Analysis3 />
              </>
            }
          />
          <Route
            path="/ann4/"
            element={
              <>
                <Analysis4 />
              </>
            }
          />
          <Route
            path="/ann5/"
            element={
              <>
                <Analysis5 />
              </>
            }
          />
          <Route
            path="/ann6/"
            element={
              <>
                <Analysis6 />
              </>
            }
          />
          <Route
            path="/doc/"
            element={
              <>
                <Documentation />
              </>
            }
          />
          <Route
            path="/settings/"
            element={
              <>
                <Settings />
              </>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}
