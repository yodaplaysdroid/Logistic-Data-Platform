import React from "react";
import { createRoot } from "react-dom/client";
import Routing from "./Routing";

import Typography from "@mui/material/Typography";

export default function App(props) {
  return (
    <>
      <div className="top">
        <div className="title">
          <Typography
            component="h4"
            variant="h4"
            sx={{ fontWeight: "bold" }}
            noWrap
          >
            物流平台
          </Typography>
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
