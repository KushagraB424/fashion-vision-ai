import React, { useState, useRef } from "react";
import axios from "axios";

function App() {

  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);
  const canvasRef = useRef(null);

  const drawBoxes = (img, detections) => {

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    canvas.width = img.width;
    canvas.height = img.height;

    ctx.drawImage(img, 0, 0);

    ctx.strokeStyle = "red";
    ctx.lineWidth = 3;
    ctx.font = "16px Arial";
    ctx.fillStyle = "red";

    detections.forEach(item => {

      const [x1, y1, x2, y2] = item.bbox;

      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      ctx.fillText(
        `${item.color} ${item.type}`,
        x1,
        y1 - 5
      );

    });

  };


  const uploadImage = async (e) => {

    const file = e.target.files[0];

    if (!file) return;

    const imageURL = URL.createObjectURL(file);
    setImage(imageURL);

    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
      "https://ideal-chainsaw-97xxrj4jx5xp2x646-8000.app.github.dev/analyze",
      formData
    );

    setResults(response.data.items);

    const img = new Image();
    img.src = imageURL;

    img.onload = () => {
      drawBoxes(img, response.data.items);
    };

  };


  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>Fashion Vision AI</h1>

      <input type="file" onChange={uploadImage} />

      <h2>Detected Image</h2>

      <canvas ref={canvasRef}></canvas>

      <h2>Detected Items</h2>

      {results.map((item, index) => (
        <div key={index} style={{border:"1px solid gray", margin:"10px", padding:"10px"}}>

          <p>
            <strong>{item.color} {item.type}</strong>
          </p>

          {item.products.map((p, i) => (
            <div key={i}>
              <a href={p.link} target="_blank" rel="noreferrer">
                {p.name}
              </a>
            </div>
          ))}

        </div>
      ))}

    </div>
  );
}

export default App;