import React from "react";
import { createRoot } from "react-dom/client";
import Routing from "./Routing";

import Typography from "@mui/material/Typography";

export default function App(props) {
  return (
    <>
      <div className="top">
        <div className="title">
          <h1>A5赛题-基于达梦云原生大数据平台的物流信息数据中台系统</h1>
        </div>
      </div>
      <div>
        <Routing />
      </div>
    </>
  );
}

const root = createRoot(document.getElementById("app"));
root.render(<App />);
