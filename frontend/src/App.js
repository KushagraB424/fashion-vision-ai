import { useState } from "react";
import axios from "axios";

function App() {

  const [image, setImage] = useState(null);
  const [results, setResults] = useState([]);

  const uploadImage = async (e) => {

    const file = e.target.files[0];

    setImage(URL.createObjectURL(file));

    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
      "https://ideal-chainsaw-97xxrj4jx5xp2x646-8000.app.github.dev/analyze",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    );

    setResults(response.data.items);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>

      <h1>Fashion Vision AI</h1>

      <input type="file" onChange={uploadImage} />

      {image && (
        <div>
          <h3>Uploaded Image</h3>
          <img src={image} alt="preview" width="400"/>
        </div>
      )}

      <h2>Detected Items</h2>

      {results.map((item, index) => (
        <div key={index} style={{border:"1px solid gray", margin:"10px", padding:"10px"}}>

          <p>
            <strong>{item.color} {item.type}</strong>
          </p>

          {item.products?.map((p, i) => (
            <div key={i}>
              <a href={p.link} target="_blank">
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