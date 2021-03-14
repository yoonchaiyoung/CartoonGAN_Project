import React, { useState, useEffect } from "react";
import Plot from "react-plotly.js";
import Plotly from "plotly.js";
import Loading from "../../../Components/Loading";

export default function PlotPresenter({ csvFile }) {
  const [data, setData] = useState({
    x: [],
    y: [],
    z: [],
    color: [],
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let newData = {
      x: [],
      y: [],
      z: [],
      color: [],
    }
    setLoading(true);
    Plotly.d3.csv(
      `https://raw.githubusercontent.com/luckycontrol/bit-cartoon/master/public/colors/${csvFile}.csv`,
      (err, rows) => {
        for (let row of rows) {
          newData.x.push(row.x);
          newData.y.push(row.y);
          newData.z.push(row.z);
          newData.color.push({ x: row.x, y: row.y, z: row.z });
        }

        setData(newData);
        setLoading(false);
      }
    );
  }, [csvFile]);

  return (
    <>
      {loading ? (
        <Loading text={"로딩중..."} usage={"load"} />
      ) : (
        <div className="filter_box">
          <img src={`poster/${csvFile}.jpg`} alt="애니 이미지"></img>
          <Plot
            data={[
              {
                x: data.x,
                y: data.y,
                z: data.z,
                type: "scatter3d",
                mode: "markers",
                marker: {
                  line: {
                    color: data.color.map(
                      (color) => `rgba(${color.x}, ${color.y}, ${color.z})`
                    ),
                    width: 0.5,
                    opacity: 0.8,
                  },
                  color: data.color.map(
                    (color) => `rgba(${color.x}, ${color.y}, ${color.z})`
                  ),
                  size: [1, 5, 12, 20, 25],
                  bgcolor: "rgba(0, 0, 0, 0.5)",
                },
                labels: ["red (x)", "green (y)", "blue (z)"],
              },
            ]}
            layout={{
              width: 500,
              height: 500,
              margin: { l: 0, r: 0, b: 0, t: 0 },
            }}
          />
        </div>
      )}
    </>
  );
}
