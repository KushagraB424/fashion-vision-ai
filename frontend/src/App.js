import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [image, setImage] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const uploadImage = async (file) => {

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {

      const response = await axios.post(API + "/analyze", formData);

      setItems(response.data.items || []);

    } catch (err) {

      console.error(err);
      alert("Upload failed");

    }

    setLoading(false);
  };

  const handleUpload = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    setImage(URL.createObjectURL(file));

    uploadImage(file);
  };

  return (
    <div className="container">

      <h1>Fashion Vision AI</h1>
      <p>Upload an image to detect clothing items</p>

      <div className="upload-box">
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
        />
      </div>

      {loading && <p className="loading">Analyzing image...</p>}

      <div className="workspace">

        {/* LEFT SIDE IMAGE */}

        <div className="image-panel">

          {image && (

            <div className="image-container">

              <img src={image} alt="preview" />

              {items.map((item, index) => {

                if (!item.bbox) return null;

                const [x1, y1, x2, y2] = item.bbox;

                return (
                  <div
                    key={index}
                    className="bbox"
                    style={{
                      left: x1,
                      top: y1,
                      width: x2 - x1,
                      height: y2 - y1
                    }}
                  >
                    <span>
                      {item.color} {item.type}
                    </span>
                  </div>
                );

              })}

            </div>

          )}

        </div>


        {/* RIGHT SIDE RESULTS */}

        <div className="results-panel">

          {items.map((item, index) => (

            <div className="card" key={index}>

              <h3>{item.color} {item.type}</h3>

              <div className="links">

                <a
                  href={`https://www.amazon.in/s?k=${item.color}+${item.type}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  Amazon
                </a>

                <a
                  href={`https://www.myntra.com/${item.color}-${item.type}`}
                  target="_blank"
                  rel="noreferrer"
                >
                  Myntra
                </a>

              </div>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default App;