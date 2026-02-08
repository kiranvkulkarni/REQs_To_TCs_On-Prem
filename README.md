# Camera Test Generation System

This project automates the generation of test cases for camera applications using AI and computer vision techniques. It processes screenshots of camera UIs using the qwen2.5vl:32b vision model (via Ollama), extracts metadata, generates Gherkin test cases, and executes them on actual devices.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Setup & Deployment](#setup--deployment)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Reporting](#reporting)
- [Troubleshooting](#troubleshooting)

## Features

- **Screenshot Ingestion**: Processes camera app screenshots using qwen2.5vl:32b (Ollama) to extract UI metadata
- **Test Case Generation**: Uses LLMs (Ollama) and rule-based systems to generate Gherkin test cases
- **Test Execution**: Runs tests on Android devices using uiautomator2
- **Reporting**: Generates detailed HTML reports with screenshots and videos
- **Alerting**: Monitors test execution metrics and sends alerts for failures
- **Multi-language Support**: Generates test cases in both English and Korean

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional, for containerized deployment)
- Android SDK (for test execution on devices/emulators)

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/camera-testgen.git
cd camera-testgen
```

### Step 2: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Node.js dependencies (for frontend)
```bash
cd src/frontend
npm install
cd ../..
```

### Step 4: Set up the database
```bash
# Create the necessary directories
mkdir -p data/kb data/logs data/exports data/reports data/screenshots data/videos data/input_screenshots

# Initialize the SQLite database
python -c "import sqlite3; conn = sqlite3.connect('data/kb/kb.sqlite'); conn.execute('CREATE TABLE IF NOT EXISTS screenshots (id INTEGER PRIMARY KEY, filename TEXT, feature_name TEXT, metadata TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'); conn.commit(); conn.close()"
```

## Setup & Deployment

### Option 1: Local Development
```bash
# Start the backend server
cd src/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start the frontend development server
cd ../frontend
npm run dev
```

### Option 2: Docker Deployment
```bash
# Build the Docker images
docker-compose build

# Start the services
docker-compose up -d

# Access the application at http://localhost:5173
```

### Option 3: Production Deployment
```bash
# Build the frontend
cd src/frontend
npm run build

# Start the backend with production settings
cd src/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Usage

### 1. Add Screenshots
Place camera app screenshots in the `data/input_screenshots` directory. The ingestion module will use the qwen2.5vl:32b vision model (Ollama) to analyze and extract state machine logic from these images.

### 2. Generate Test Cases
```bash
# Process screenshots and generate test cases
python src/ingestion/processor.py
# (Requires Ollama running locally with the qwen2.5vl:32b model pulled)
```

### 3. Execute Tests
```bash
# Run tests on connected devices
python src/execution/executor.py
```

### 4. View Reports
Access the reports at `data/reports` directory or through the web interface at http://localhost:5173

### 5. Monitor Metrics
Access Prometheus metrics at http://localhost:9090 and Grafana dashboard at http://localhost:3000

## Configuration

The main configuration file is `config/settings.yaml`. Key settings include:

- **Ingestion**: Controls how screenshots are processed
- **Generation**: Configures the LLM and rule-based test case generation
- **Execution**: Sets up test execution parameters (devices, timeouts, etc.)
- **Reporting**: Configures report generation and alerting
- **Frontend**: Sets up the web interface
- **Backend**: Configures the API server

## Project Structure

```
camera-testgen/
├── config/                  # Configuration files
├── data/                    # Data storage (screenshots, exports, reports, etc.)
├── docker/                  # Docker configuration
├── scripts/                 # Deployment and setup scripts
├── src/                     # Source code
│   ├── backend/             # FastAPI backend
│   ├── frontend/            # React frontend
│   ├── execution/           # Test execution components
│   ├── generation/          # Test case generation
│   ├── ingestion/           # Screenshot processing
│   └── reporting/           # Reporting and alerting
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Testing

Run the test suite:
```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_ingestion.py
python -m pytest tests/test_backend.py
```

## Reporting

The system generates comprehensive reports with:
- Test execution results
- Screenshots of test failures
- Video recordings of test runs
- Performance metrics
- Alert notifications for critical issues

## Troubleshooting

### Common Issues

1. **Test execution fails on devices**
   - Ensure devices are connected and USB debugging is enabled
   - Check device serials in config/settings.yaml
   - Verify app_package and app_activity are correct

2. **Vision model or LLM generation fails**
   - Ensure Ollama is running and the qwen2.5vl:32b model is available locally
   - Pull the model with: `ollama pull qwen2.5vl:32b`
   - Check LLM and vision model configuration in config/settings.yaml

3. **Frontend not loading**
   - Ensure backend is running on port 8000
   - Check CORS settings in config/settings.yaml
   - Verify frontend is built and served correctly

### Support

For additional help, please open an issue on GitHub or contact the development team.