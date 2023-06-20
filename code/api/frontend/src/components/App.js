import React from "react";
import { createRoot } from "react-dom/client";
import Routing from "./Routing";
import SideBar from "./Sidebar";
import Header from "./Header";

export default function App(props) {
  return (
    <>
      <div className="left">
        <SideBar />
      </div>
      <div
        style={{
          marginTop: 10,
          marginLeft: 10,
          marginBottom: 10,
          marginRight: 30,
          display: "block",
          width: "100%",
        }}
      >
        <div className="top">
          <Header />
        </div>
        <div className="content">
          <Routing />
        </div>
      </div>
    </>
  );
}

const root = createRoot(document.getElementById("app"));
root.render(<App />);
