A full-stack, deep learning-driven web application designed to seamlessly bridge the gap between computer vision and visual commerce through automated clothing detection.

---

## Executive Overview

Fashion Vision AI is an advanced computer vision platform that leverages state-of-the-art deep learning models to autonomously identify apparel within user-uploaded images. By integrating precise object localization with algorithmic color extraction, the system transforms static images into interactive, highly relevant e-commerce search vectors. 

---

## Core Capabilities

* **Algorithmic Object Detection:** Utilizes the Ultralytics YOLO framework for accurate and rapid localization of clothing garments within diverse image environments.
* **Intelligent Color Extraction:** Processes localized bounding box regions to determine the dominant hex codes and primary color classifications of detected items.
* **Seamless User Experience:** Features a highly responsive frontend tailored for effortless image uploading and real-time inference previews.
* **Integrated Commerce Routing:** Dynamically generates contextual shopping queries across major platforms, including Amazon, Myntra, and Google Shopping.
* **Asynchronous Processing:** Powered by an optimized FastAPI backend to ensure low-latency inference and high concurrent request handling.

---

## Technology Architecture

### Backend Systems
* FastAPI
* PyTorch
* Ultralytics YOLOv8
* OpenCV
* NumPy

### Frontend Systems
* React.js
* Axios
* CSS

---


## Environment Setup and Deployment

### 1. Initialize the Repository

git clone https://github.com/KushagraB424/fashion-vision-ai.git

cd fashion-vision-ai

### 2. Configure the Backend API

pip install -r requirements.txt

python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000


### 3. Initialize the Frontend Client

cd frontend

npm install

npm start


---

## API Documentation

**Endpoint:** `POST /analyze`

**Payload:** Multipart Form Data (Image File)

**Response Schema:**

json
{
  "items": [
    {
      "color": "black",
      "type": "jacket"
    },
    {
      "color": "blue",
      "type": "jeans"
    }
  ]
}

---

## Operational Workflow

1. **Ingestion:** The user uploads a target image via the frontend interface.
2. **Inference:** The backend receives the payload and passes it through the YOLOv8 detection pipeline.
3. **Feature Extraction:** The system isolates detected regions and extracts the dominant color properties.
4. **Data Serialization:** The backend constructs and returns a structured JSON payload of the identified garments.
5. **Display & Routing:** The frontend maps the returned data to the UI, presenting the user with categorized items and direct e-commerce search links.
<img width="1132" height="687" alt="image" src="https://github.com/user-attachments/assets/93989854-711c-43fa-a652-35cc296d1890" />

---

## Author

**Kushagra Gupta** LinkedIn: [Kushagra Gupta](https://www.linkedin.com/in/kushagra-gupta-8861663a0/)
