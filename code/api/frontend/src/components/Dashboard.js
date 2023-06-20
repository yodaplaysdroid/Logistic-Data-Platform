import * as React from "react";
import { useState } from "react";
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";

import ArchiveRoundedIcon from "@mui/icons-material/ArchiveRounded";
import UnarchiveRoundedIcon from "@mui/icons-material/UnarchiveRounded";
import CategoryRoundedIcon from "@mui/icons-material/CategoryRounded";
import ApartmentRoundedIcon from "@mui/icons-material/ApartmentRounded";
import Face4RoundedIcon from "@mui/icons-material/Face4Rounded";
import WidgetsRoundedIcon from "@mui/icons-material/WidgetsRounded";

import { Button } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3e2b2b",
    },
  },
});
export default function Dashboard(request) {
  const [res, setRes] = useState();
  const [status, setStatus] = useState(0);

  if (status === 0) {
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    fetch("/api/dashboard/", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        setRes(data);
        setStatus(1);
      });
  }
  console.log(res);
  return (
    <>
      <ThemeProvider theme={theme}>
        <div style={{ height: "15%", width: "100%" }}>
          <div
            style={{
              borderRadius: 30,
              backgroundColor: "#fdd9d9",
              padding: 20,
              marginTop: 10,
            }}
          >
            <div className="recordcountpanel">
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <ApartmentRoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    物流公司: {status === 1 ? res["记录数量"][0] : "-"}
                  </div>
                </Button>
              </div>
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <Face4RoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    客户信息: {status === 1 ? res["记录数量"][1] : "-"}
                  </div>
                </Button>
              </div>
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <CategoryRoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    物流信息: {status === 1 ? res["记录数量"][2] : "-"}
                  </div>
                </Button>
              </div>
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <WidgetsRoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    集装箱动态: {status === 1 ? res["记录数量"][3] : "-"}
                  </div>
                </Button>
              </div>
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <UnarchiveRoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    装货表: {status === 1 ? res["记录数量"][4] : "-"}
                  </div>
                </Button>
              </div>
              <div>
                <Button color="primary" sx={{ borderRadius: 50 }}>
                  <ArchiveRoundedIcon />
                  <div style={{ fontSize: 15, paddingLeft: 2 }}>
                    卸货表: {status === 1 ? res["记录数量"][5] : "-"}
                  </div>
                </Button>
              </div>
            </div>
          </div>
        </div>

        {status === 1 ? (
          <>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                height: "83%",
              }}
            >
              <div
                className="subpanel"
                style={{
                  flexDirection: "column",
                  justifyContent: "space-between",
                  display: "flex",
                  width: "40%",
                  height: "100%",
                }}
              >
                <Button
                  color="primary"
                  sx={{ borderRadius: 5, display: "block", margin: 2 }}
                >
                  <div className="subpanelheader">近期港口吞吐量排行</div>
                  <div className="subpanelcontent">
                    {res["港口排行"][0][0]}:{res["港口排行"][0][1]}单<br></br>
                    {res["港口排行"][1][0]}: {res["港口排行"][1][1]}单<br></br>
                    {res["港口排行"][2][0]}: {res["港口排行"][2][1]}单<br></br>
                  </div>
                </Button>
                <Button
                  color="primary"
                  sx={{
                    borderRadius: 5,
                    display: "block",
                    margin: 2,
                  }}
                >
                  <div className="subpanelheader">近期货物吞吐趋势</div>
                  <div className="subpanelcontent">
                    {res["货物排行"][0][0]}: {res["货物排行"][0][1]}单:{" "}
                    {res["货物排行"][0][2]}吨<br></br>
                    {res["货物排行"][1][0]}: {res["货物排行"][1][1]}单:{" "}
                    {res["货物排行"][1][2]}吨<br></br>
                    {res["货物排行"][2][0]}: {res["货物排行"][2][1]}单:{" "}
                    {res["货物排行"][2][2]}吨<br></br>
                  </div>
                </Button>
                <Button
                  color="primary"
                  sx={{ borderRadius: 5, display: "block", margin: 2 }}
                >
                  <div className="subpanelheader">各省货物消费情况</div>
                  <div className="subpanelcontent">
                    {res["各省消费"][0][0]}: {res["各省消费"][0][1]}单<br></br>
                    {res["各省消费"][1][0]}: {res["各省消费"][1][1]}单<br></br>
                    {res["各省消费"][2][0]}: {res["各省消费"][2][1]}单<br></br>
                  </div>
                </Button>
              </div>

              <div
                style={{
                  width: "59%",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                }}
              >
                <div
                  className="subpanel"
                  style={{ right: 0, height: "71%", top: 0 }}
                >
                  <Line
                    style={{ marginLeft: 10 }}
                    data={{
                      labels: res["时间周期"][0],
                      datasets: [
                        {
                          label: "货物传送时间周期趋势",
                          data: res["时间周期"][1],
                          fill: false,
                          borderColor: "#711490",
                          tension: 0.1,
                        },
                      ],
                    }}
                  />
                </div>
                <div
                  className="subpanel"
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    height: "27%",
                  }}
                >
                  <Button
                    color="primary"
                    sx={{
                      borderRadius: 5,
                      display: "block",
                      width: "45%",
                      margin: 1.5,
                    }}
                  >
                    <div className="subpanelheader">入库堆存港口排行</div>
                    {res["入库排行"][0][0]}: {res["入库排行"][0][1]}单<br></br>
                    {res["入库排行"][1][0]}: {res["入库排行"][1][1]}单<br></br>
                    {res["入库排行"][2][0]}: {res["入库排行"][2][1]}单<br></br>
                  </Button>
                  <Button
                    color="primary"
                    sx={{
                      borderRadius: 5,
                      display: "block",
                      width: "45%",
                      margin: 1.5,
                    }}
                  >
                    <div className="subpanelheader">出库堆存港口排行</div>
                    {res["出库排行"][0][0]}: {res["出库排行"][0][1]}单<br></br>
                    {res["出库排行"][1][0]}: {res["出库排行"][1][1]}单<br></br>
                    {res["出库排行"][2][0]}: {res["出库排行"][2][1]}单<br></br>
                  </Button>
                </div>
              </div>
            </div>
          </>
        ) : null}
      </ThemeProvider>
    </>
  );
}
