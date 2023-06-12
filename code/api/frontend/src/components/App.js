import React from "react";
import { createRoot } from "react-dom/client";
import Routing from "./Routing";
import SideBar from "./Sidebar";
import Header from "./Header";

export default function App(props) {
  return (
    <>
      <div className="top">
        <Header />
      </div>
      <div className="left">
        <SideBar />
      </div>
      <div>
        <Routing />
      </div>
    </>
  );
}

const root = createRoot(document.getElementById("app"));
root.render(<App />);
