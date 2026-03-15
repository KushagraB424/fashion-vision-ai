import React, { useState, useRef } from "react";
import axios from "axios";

function App() {

  const [image, setImage] = useState(null);
  const [items, setItems] = useState([]);

  const canvasRef = useRef(null);

  const uploadImage = async (file) => {

    const formData = new FormData();
    formData.append("file", file);

    try {

      const response = await axios.post(
        "https://cuddly-space-winner-4jrr5w9wrq6gc9wq-8000.app.github.dev/analyze",
        formData
      );

      console.log("Backend response:", response.data);

      if (!response.data || !response.data.items) {
        alert("Backend returned invalid response");
        return;
      }

      setItems(response.data.items);

      drawBoxes(file, response.data.items);

    } catch (err) {

      console.error("UPLOAD FAILED:", err);
      alert("Upload failed. Check console.");

    }

  };

  const drawBoxes = (file, detections) => {

    const img = new Image();

    img.onload = () => {

      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");

      canvas.width = img.width;
      canvas.height = img.height;

      ctx.drawImage(img, 0, 0);

      detections.forEach(item => {

        const [x1, y1, x2, y2] = item.bbox;

        ctx.strokeStyle = "red";
        ctx.lineWidth = 3;

        ctx.strokeRect(
          x1,
          y1,
          x2 - x1,
          y2 - y1
        );

        ctx.fillStyle = "red";
        ctx.font = "18px Arial";

        ctx.fillText(
          `${item.color} ${item.type}`,
          x1,
          y1 - 5
        );

      });

    };

    img.src = URL.createObjectURL(file);

  };

  const handleFileChange = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    setImage(file);

    uploadImage(file);

  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>

      <h1>Fashion Vision AI</h1>

      <input
        type="file"
        onChange={handleFileChange}
      />

      <h2>Detected Image</h2>

      <canvas ref={canvasRef} />

      <h2>Detected Items</h2>

      {items.map((item, index) => (

        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: "10px",
            marginBottom: "10px"
          }}
        >

          <h3>{item.color} {item.type}</h3>

          <a
            href={`https://www.amazon.in/s?k=${item.color}+${item.type}`}
            target="_blank"
            rel="noreferrer"
          >
            Search Amazon
          </a>

          <br/>

          <a
            href={`https://www.myntra.com/${item.color}-${item.type}`}
            target="_blank"
            rel="noreferrer"
          >
            Search Myntra
          </a>

          <br/>

          <a
            href={`https://www.google.com/search?q=${item.color}+${item.type}&tbm=shop`}
            target="_blank"
            rel="noreferrer"
          >
            Google Shopping
          </a>

        </div>

      ))}

    </div>
  );
}

export default App;