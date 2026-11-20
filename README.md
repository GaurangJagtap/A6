# MLOps Practical Assignment: Containerize a Machine Learning Model Using Docker and Expose It as a REST API

## 1. Assignment Title
**Containerize a Machine Learning Model Using Docker and Expose It as a REST API**

---

## 2. Aim and Objectives

### Aim
To develop an end-to-end Machine Learning pipeline that trains a classification model on the Iris dataset, packages it as a production-ready REST API using Flask, and containerizes the entire application using Docker to ensure reproducibility, platform independence, and seamless deployment.

### Objectives
- Train a machine learning model (`RandomForestClassifier`) on the classical Iris flower dataset using Scikit-Learn.
- Evaluate the model using standard metrics (Accuracy, Precision, Recall, F1-Score) and serialize the trained model using `joblib`.
- Construct a robust REST API using Flask with multiple endpoints (`/`, `/health`, `/predict`) with strict request validation and error handling.
- Author an optimized `Dockerfile` leveraging a lightweight Python image and multi-layer caching.
- Build and run the Docker container, exposing port 5000 for network communication.
- Perform black-box integration testing against the containerized REST API using both Python and PowerShell.
- Document Docker lifecycle commands and image registry workflows (Docker Hub).

---

## 3. Introduction to MLOps
**MLOps (Machine Learning Operations)** is an engineering practice that unites Machine Learning model development (Dev) with system operations (Ops). The goal of MLOps is to standardize and automate continuous delivery of ML models into production environments reliably and efficiently.

Unlike traditional software development, ML applications present unique lifecycle challenges:
- **Code & Dependency Drift:** Subtle version differences between libraries (e.g., Scikit-Learn, NumPy) can lead to silent errors, serialization incompatibilities, or shifted predictions.
- **Environment Discrepancies:** "It works on my machine" is a frequent failure mode when deploying to cloud servers or heterogeneous operating systems.
- **Reproducibility:** MLOps emphasizes tracking the code, data, model binaries, and container definitions so that experiments and production deployments are 100% reproducible.

Containerization with Docker is a foundational pillar of modern MLOps pipelines.

---

## 4. What is Docker?
**Docker** is an open-source platform that enables developers to package applications and all their dependencies (runtime, system libraries, configuration, binaries) into standardized executable units called **containers**.

By abstracting away OS-level inconsistencies, Docker ensures that an application built and verified in a development environment behaves identically across testing, staging, and production environments.

---

## 5. Docker Image vs. Docker Container

| Feature | Docker Image | Docker Container |
| :--- | :--- | :--- |
| **Definition** | A read-only, immutable blueprint or template containing the code, libraries, and instructions. | A runnable, live instance of a Docker image. |
| **State** | Static and stored on disk or in an image registry (e.g., Docker Hub). | Dynamic; has runtime state, memory, network interfaces, and ephemeral disk storage. |
| **Analogy** | A Class definition in Object-Oriented Programming, or an architectural blueprint. | An instantiated Object in OOP, or the actual physical building. |
| **Creation** | Built using `docker build -t <image-name> .` from a `Dockerfile`. | Spawned using `docker run <image-name>`. |

---

## 6. Containers vs. Virtual Machines (VMs)

| Characteristic | Docker Container | Virtual Machine (VM) |
| :--- | :--- | :--- |
| **Architecture** | Shares the Host OS kernel; isolates processes in user space using namespaces and cgroups. | Emulates complete hardware via a Hypervisor (Type 1 or Type 2); runs a full Guest OS. |
| **Startup Time** | Milliseconds to seconds (instantaneous process spawn). | Minutes (full operating system boot cycle). |
| **Resource Overhead** | Extremely lightweight; uses minimal RAM and host CPU. | Heavy footprint; reserves dedicated CPU cores, RAM, and large disk images (gigabytes). |
| **Portability** | High; runs anywhere Docker Engine is supported. | Moderate; VM disk formats (`.vmdk`, `.ova`) are large and hypervisor-dependent. |
| **Isolation** | Process-level isolation. | Full hardware-level isolation. |

---

## 7. Project Folder Structure

```text
iris-ml-docker/
│
├── model/
│   └── train_model.py       # Script to load data, train Random Forest, evaluate, and save model
│
├── screenshots/             # Storage for practical demonstration screenshots
│
├── app.py                   # Flask REST API exposing /, /health, and /predict endpoints
├── model.joblib             # Serialized trained Scikit-learn model
├── requirements.txt         # Pinned application dependencies (Flask, scikit-learn, joblib, numpy)
├── Dockerfile               # Docker configuration for containerizing the application
├── .dockerignore            # Excluded files and folders during Docker build
├── .gitignore               # Excluded files for Git version control
├── test_api.py              # Automated test suite using Python requests
├── test_api.ps1             # Automated test suite using PowerShell Invoke-RestMethod
└── README.md                # Comprehensive documentation
```

---

## 8. Dataset Description
The **Iris dataset** is one of the most renowned benchmarks in pattern recognition and machine learning, originally published by Ronald Fisher in 1936.

- **Total Samples:** 150 (50 samples per class).
- **Target Classes (3):**
  1. `setosa` (Class 0)
  2. `versicolor` (Class 1)
  3. `virginica` (Class 2)
- **Features (4 numeric measurements in centimeters):**
  1. `sepal length (cm)`
  2. `sepal width (cm)`
  3. `petal length (cm)`
  4. `petal width (cm)`

---

## 9. Model Training Explanation

The model training script is implemented in [`model/train_model.py`](model/train_model.py):
1. **Data Ingestion:** Loads the Iris dataset directly via `sklearn.datasets.load_iris()`.
2. **Train/Test Splitting:** Performs a stratified split into **80% training (120 samples)** and **20% testing (30 samples)** using `random_state=42`. Stratification preserves class balance across splits.
3. **Algorithm:** Uses `RandomForestClassifier(n_estimators=100, random_state=42)`. An ensemble of 100 decision trees is constructed using bagging and feature subspace sampling to achieve high generalization and reduce variance.
4. **Evaluation:** Evaluates predictions on the held-out test set using `accuracy_score` and `classification_report`.
5. **Serialization:** Persists the trained model to `model.joblib` in the project root directory using `joblib.dump()`.

### Actual Training Results
```text
Training set size: 120 samples
Testing set size:  30 samples
Model Accuracy: 90.00% (0.9000)

Classification Report:
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       0.82      0.90      0.86        10
   virginica       0.89      0.80      0.84        10

    accuracy                           0.90        30
   macro avg       0.90      0.90      0.90        30
weighted avg       0.90      0.90      0.90        30

Trained model saved successfully to: model.joblib (167,729 bytes)
```

---

## 10. Flask REST API Explanation

The web service is built with Flask in [`app.py`](app.py):

### Endpoints

#### 1. `GET /`
- **Purpose:** Verifies that the service is running.
- **Response:**
  ```json
  {
    "message": "Iris Model API is running"
  }
  ```

#### 2. `GET /health`
- **Purpose:** System health-check endpoint for container orchestrators and monitoring tools.
- **Response:**
  ```json
  {
    "status": "healthy",
    "model_loaded": true,
    "classes": ["setosa", "versicolor", "virginica"]
  }
  ```

#### 3. `POST /predict`
- **Purpose:** Accepts 4 numerical features and returns the predicted flower species.
- **Request Format:**
  ```json
  {
    "features": [5.1, 3.5, 1.4, 0.2]
  }
  ```
- **Response Format:**
  ```json
  {
    "prediction": "setosa"
  }
  ```

### Input Validation & Defensive Engineering
- **JSON Format Check:** Returns `400 Bad Request` if the body is not valid JSON.
- **Key Presence Check:** Returns `400 Bad Request` if the `"features"` key is omitted.
- **Type Check:** Ensures `"features"` is a JSON array.
- **Dimension Check:** Strictly validates that `len(features) == 4`.
- **Value Check:** Validates that each feature is a numerical value (`int` or `float`), rejecting strings, booleans, `NaN`, or `Infinity`.

---

## 11. Dockerfile Explanation

The [`Dockerfile`](Dockerfile) defines how the image is built step-by-step:

```dockerfile
# Step 1: Use an official lightweight Python image
FROM python:3.11-slim

# Step 2: Set working directory in container
WORKDIR /app

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code and serialized model
COPY app.py .
COPY model.joblib .

# Step 6: Expose port 5000 for Flask API
EXPOSE 5000

# Step 7: Command to run application on container start
CMD ["python", "app.py"]
```

### Explanation of Dockerfile Instructions:
- **`FROM python:3.11-slim`**: Sets the base operating system and runtime. The `slim` variant contains the minimal Debian packages needed to run Python, keeping the image size small and secure.
- **`WORKDIR /app`**: Creates and sets `/app` as the active working directory inside the container for all subsequent instructions (`COPY`, `RUN`, `CMD`).
- **`COPY requirements.txt .`**: Copies only the requirements file into the container first. This maximizes **Docker layer caching**: if the code changes but dependencies do not, Docker reuses the cached layer and skips the time-consuming `pip install` step.
- **`RUN pip install --no-cache-dir -r requirements.txt`**: Installs the required Python packages (`Flask`, `scikit-learn`, `joblib`, `numpy`). The `--no-cache-dir` flag prevents pip from caching installation wheels, reducing final image footprint.
- **`COPY app.py .` & `COPY model.joblib .`**: Copies the application server and the pre-trained model artifact into `/app`.
- **`EXPOSE 5000`**: Documents that the container process listens on network port 5000.
- **`CMD ["python", "app.py"]`**: Specifies the default command executed when the container starts. Unlike `RUN` (which runs at image build time), `CMD` executes at container runtime.

---

## 12. Docker Image Building Instructions

Ensure Docker Desktop is running, then open PowerShell in the project directory:

```powershell
cd "c:\College\SEM 5\MLOPs\Assignment_6\iris-ml-docker"
```

Build the Docker image with the name `iris-model-api` and tag `1.0`:

```powershell
docker build -t iris-model-api:1.0 .
```

Verify that the image was built:

```powershell
docker images
```

**Expected output:**
```text
REPOSITORY         TAG       IMAGE ID       CREATED          SIZE
iris-model-api     1.0       a1b2c3d4e5f6   10 seconds ago   ~350MB
```

---

## 13. Container Execution Instructions

Run the container in detached mode (`-d`), binding host port 5000 to container port 5000 (`-p 5000:5000`), and giving it a recognizable name (`--name iris-container`):

```powershell
docker run -d -p 5000:5000 --name iris-container iris-model-api:1.0
```

Verify the container is actively running:

```powershell
docker ps
```

Inspect the container logs to ensure Flask initialized correctly:

```powershell
docker logs iris-container
```

**Expected log output:**
```text
[INFO] Model loaded successfully from /app/model.joblib
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

---

## 14. API Testing Instructions

### Option A: Using the Automated Python Test Script
```powershell
python test_api.py
```

### Option B: Using the Automated PowerShell Script
```powershell
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

### Option C: Manual Testing via PowerShell / curl

#### 1. Test Root Endpoint (`GET /`)
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/" -Method GET | ConvertTo-Json
```
*Expected:*
```json
{
  "message": "Iris Model API is running"
}
```

#### 2. Test Health Endpoint (`GET /health`)
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET | ConvertTo-Json
```
*Expected:*
```json
{
  "classes": ["setosa", "versicolor", "virginica"],
  "model_loaded": true,
  "status": "healthy"
}
```

#### 3. Test Prediction 1 - Setosa (`POST /predict`)
```powershell
$body = '{"features": [5.1, 3.5, 1.4, 0.2]}'
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```
*Expected:*
```json
{
  "prediction": "setosa"
}
```

#### 4. Test Prediction 2 - Versicolor (`POST /predict`)
```powershell
$body = '{"features": [6.0, 2.7, 5.1, 1.6]}'
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```
*Expected:*
```json
{
  "prediction": "versicolor"
}
```

#### 5. Test Prediction 3 - Virginica (`POST /predict`)
```powershell
$body = '{"features": [6.7, 3.3, 5.7, 2.5]}'
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body -ContentType "application/json" | ConvertTo-Json
```
*Expected:*
```json
{
  "prediction": "virginica"
}
```

#### 6. Test Input Validation - Invalid Length
```powershell
$body = '{"features": [5.1, 3.5]}'
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body -ContentType "application/json"
```
*Expected Status:* `400 Bad Request` with error message explaining that exactly 4 features are required.

---

## 15. Useful Docker Commands

```powershell
# List all locally available Docker images
docker images

# List currently running containers
docker ps

# List all containers (running, stopped, exited)
docker ps -a

# View container logs (standard output / standard error)
docker logs iris-container

# Follow container logs in real-time
docker logs -f iris-container

# Stop the running container gracefully
docker stop iris-container

# Restart a stopped container
docker start iris-container

# Execute an interactive bash/sh shell inside the running container
docker exec -it iris-container /bin/sh

# Remove the container
docker rm iris-container

# Remove the Docker image
docker rmi iris-model-api:1.0
```

---

## 16. Expected Outputs

### 1. Training Output
```text
Model Accuracy: 90.00% (0.9000)
Trained model saved successfully to: model.joblib
```

### 2. Prediction JSON
```json
{
  "prediction": "setosa"
}
```

### 3. Error JSON on Bad Input
```json
{
  "error": "Invalid feature length: Expected exactly 4 numerical features (sepal_length, sepal_width, petal_length, petal_width), but received 2."
}
```

---

## 17. Advantages of Containerization in MLOps

1. **Environment Reproducibility:** Eliminates dependency version conflicts across developer workstations, CI/CD runners, and production clusters.
2. **Portability:** The container image runs identically on Windows, Linux, macOS, AWS ECS/EKS, Azure Container Instances, or Google Cloud Run.
3. **Isolation & Security:** The application and its Python runtime are sandboxed from the host OS, preventing unauthorized file system access and system dependency pollution.
4. **Scalability:** Containerized microservices can be easily scaled horizontally using orchestration tools like Kubernetes or Docker Swarm based on incoming traffic.
5. **Continuous Deployment (CI/CD):** Docker images serve as immutable release artifacts that can be tested in automated pipelines and promoted directly to production.

---

## 18. Conclusion
In this practical assignment, we successfully implemented an end-to-end MLOps workflow:
- Trained and evaluated a machine learning classification model on the Iris dataset.
- Exposed the trained model via a production-grade Flask REST API with defensive input validation.
- Packaged the complete solution into a lightweight, standalone Docker container.
- Verified live inference queries and error handling against the containerized service.

Containerization transforms a local machine learning script into an enterprise-ready microservice, cementing a critical bridge between data science and operational engineering.

---

## 19. Optional Docker Hub Extension

Docker Hub is a cloud-based registry service that allows developers to store, share, and distribute Docker images globally.

### Step 1: Create a Docker Hub Account
Visit [https://hub.docker.com/](https://hub.docker.com/) and register for a free account. Note your **Docker Hub username** (e.g., `yourusername`).

### Step 2: Log in via CLI
Open PowerShell and authenticate:
```powershell
docker login
```
Enter your Docker Hub username and password (or Personal Access Token).

### Step 3: Tag Your Image
Docker Hub requires image names in the format `<username>/<repository>:<tag>`:
```powershell
docker tag iris-model-api:1.0 yourusername/iris-model-api:1.0
```

### Step 4: Push the Image to Docker Hub
```powershell
docker push yourusername/iris-model-api:1.0
```

### Step 5: Pull and Run on Any Other Machine
Anyone with Docker installed can now run your model without cloning code or installing Python:
```powershell
docker run -d -p 5000:5000 yourusername/iris-model-api:1.0
```

---

## 20. Required Screenshot Checklist for College Submission

| # | Screenshot Item | Description / Window to Capture |
| :---: | :--- | :--- |
| **SS 1** | **Model Training & Evaluation** | Terminal showing execution of `python model/train_model.py`, displaying accuracy (90.00%), classification report, and `model.joblib` generation. |
| **SS 2** | **Docker Image Build** | Terminal showing `docker build -t iris-model-api:1.0 .` successfully finishing with step-by-step layer outputs. |
| **SS 3** | **Docker Images List** | Terminal showing `docker images` with `iris-model-api` listed alongside its size and tag `1.0`. |
| **SS 4** | **Docker Container Status** | Terminal showing `docker ps` with `iris-container` active, displaying port mapping `0.0.0.0:5000->5000/tcp`. |
| **SS 5** | **Browser Root Endpoint** | Web browser open to `http://localhost:5000/` displaying `{"message": "Iris Model API is running"}`. |
| **SS 6** | **Browser / Postman Health Check** | Browser or Postman showing `http://localhost:5000/health` with `status: "healthy"` and `model_loaded: true`. |
| **SS 7** | **POST /predict Inference** | Terminal or Postman showing POST request with `{"features": [5.1, 3.5, 1.4, 0.2]}` returning `{"prediction": "setosa"}`. |
| **SS 8** | **POST /predict Error Handling** | Terminal or Postman showing POST request with invalid features returning HTTP 400 with an informative error. |
| **SS 9** | **Docker Logs** | Terminal showing `docker logs iris-container` showing Flask startup and incoming HTTP 200/400 requests. |
| **SS 10** | **Docker Stop & Restart** | Terminal showing `docker stop iris-container` followed by `docker ps -a`, and `docker start iris-container`. |
