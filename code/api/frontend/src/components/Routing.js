import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Mysql from "./Mysql";
import Hdfs from "./Hdfs";
import Minio from "./Minio";
import RecordCount from "./RecordCount";
import Analysis1 from "./Analysis1";
import Analysis2 from "./Analysis2";
import Analysis3 from "./Analysis3";
import Analysis4 from "./Analysis4";
import Analysis5 from "./Analysis5";
import Analysis6 from "./Analysis6";

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
                  <div className="mainpanel">
                    <div className="recordcountpanel">
                      <RecordCount />
                    </div>
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
                  <Mysql />
                </div>
              </>
            }
          />
          <Route
            path="/hdfs/"
            element={
              <>
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
                <div className="content">
                  <Minio />
                </div>
              </>
            }
          />
          <Route
            path="/ann1/"
            element={
              <>
                <div className="content">
                  <Analysis1 />
                </div>
              </>
            }
          />
          <Route
            path="/ann2/"
            element={
              <>
                <div className="content">
                  <Analysis2 />
                </div>
              </>
            }
          />
          <Route
            path="/ann3/"
            element={
              <>
                <div className="content">
                  <Analysis3 />
                </div>
              </>
            }
          />
          <Route
            path="/ann4/"
            element={
              <>
                <div className="content">
                  <Analysis4 />
                </div>
              </>
            }
          />
          <Route
            path="/ann5/"
            element={
              <>
                <div className="content">
                  <Analysis5 />
                </div>
              </>
            }
          />
          <Route
            path="/ann6/"
            element={
              <>
                <div className="content">
                  <Analysis6 />
                </div>
              </>
            }
          />
        </Routes>
      </BrowserRouter>
    </>
  );
}
