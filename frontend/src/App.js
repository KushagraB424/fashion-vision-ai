import React, { useState, useRef } from "react";
import axios from "axios";

function App() {

  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);
  const canvasRef = useRef(null);

  const drawMasks = (img, detections) => {

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    canvas.width = img.width;
    canvas.height = img.height;

    ctx.drawImage(img, 0, 0);

    detections.forEach(item => {

      const poly = item.polygon;

      ctx.beginPath();

      poly.forEach((point, index) => {

        const [x, y] = point;

        if (index === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);

      });

      ctx.closePath();

      ctx.fillStyle = "rgba(255,0,0,0.25)";
      ctx.fill();

      ctx.strokeStyle = "red";
      ctx.stroke();

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
      drawMasks(img, response.data.items);
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