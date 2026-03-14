import React, { useState } from "react";
import axios from "axios";

function App() {

  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const uploadImage = async (e) => {
    try {

      const file = e.target.files[0];

      if (!file) return;

      setImage(URL.createObjectURL(file));
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "https://ideal-chainsaw-97xxrj4jx5xp2x646-8000.app.github.dev/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          timeout: 60000
        }
      );

      console.log("API response:", response.data);

      setResults(response.data.items || []);
      setLoading(false);

    } catch (error) {

      console.error("Upload error:", error);

      alert("Upload failed. Check console for details.");

      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>Fashion Vision AI</h1>

      <input type="file" onChange={uploadImage} />

      {image && (
        <div style={{ marginTop: "20px" }}>
          <h3>Uploaded Image</h3>
          <img src={image} alt="preview" width="400" />
        </div>
      )}

      {loading && (
        <p>Processing image...</p>
      )}

      <h2>Detected Items</h2>

      {results.map((item, index) => (
        <div
          key={index}
          style={{
            border: "1px solid gray",
            margin: "10px",
            padding: "10px",
            borderRadius: "8px"
          }}
        >

          <p>
            <strong>
              {item.color} {item.type}
            </strong>
          </p>

          {item.products && item.products.map((p, i) => (
            <div key={i}>
              <a
                href={p.link}
                target="_blank"
                rel="noreferrer"
              >
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