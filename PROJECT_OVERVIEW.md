# Project Overview

## Purpose
This project automates the extraction of state machine logic from mobile UX flowcharts and generates structured test cases for QA automation. It leverages vision models (Ollama) to analyze screenshots, builds a knowledge base, and executes tests on Android devices.

## Architecture

### High-Level Diagram

- **Frontend**: React-based UI for dashboard, review, export, and feedback.
- **Backend**: FastAPI server providing REST APIs for ingestion, generation, export, and feedback.
- **Ingestion Module**: Processes screenshots using Ollama vision models, extracts structured metadata, and stores it in a knowledge base (SQLite + FAISS).
- **Generation Module**: Converts metadata into Gherkin test cases using rule-based logic and LLMs.
- **Execution Module**: Runs tests on Android devices/emulators using uiautomator2, records results, screenshots, and videos.
- **Reporting Module**: Generates HTML/PDF/JSON reports and exposes Prometheus metrics for monitoring.

### Data Flow

1. **Screenshot Ingestion**
    - Screenshots are placed in `data/input_screenshots`.
    - The ingestion module processes each image, calls Ollama, and extracts state machine logic.
    - Metadata is stored in SQLite and FAISS for search and retrieval.

2. **Test Case Generation**
    - Metadata is passed to the generation module.
    - RuleEngine and LLMAdapter generate Gherkin test cases.
    - Test cases are exported as `.feature` files.

3. **Test Execution**
    - Feature files are executed on Android devices/emulators.
    - Results, screenshots, and videos are collected.

4. **Reporting & Monitoring**
    - Reports are generated in HTML/PDF/JSON formats.
    - Prometheus metrics are exposed for monitoring test status and performance.

## Key Components

- **Ollama Vision Model**: Used for extracting structured logic from screenshots.
- **SQLite & FAISS**: Store metadata and enable fast vector search.
- **RuleEngine & LLMAdapter**: Generate test cases using deterministic rules and LLMs.
- **UIAutomator2Adapter**: Executes tests on Android devices.
- **PrometheusExporter**: Provides metrics for monitoring.

## Folder Structure

- `src/backend`: FastAPI backend, routes, services, and utilities.
- `src/ingestion`: Image processing, metadata extraction, and KB writing.
- `src/generation`: Test case generation logic.
- `src/execution`: Test execution and reporting.
- `src/reporting`: Metrics and report generation.
- `data/`: Input screenshots, exports, logs, reports, videos.
- `config/`: Project configuration (settings.yaml).
- `tests/`: Unit and integration tests.

## Typical Flow

1. Place screenshots in `data/input_screenshots`.
2. Run ingestion to build the knowledge base.
3. Generate Gherkin test cases from metadata.
4. Execute tests on devices/emulators.
5. Review reports and monitor metrics.

## Extensibility
- Easily add new vision models or LLMs.
- Customizable rule logic and prompt templates.
- Supports parallel test execution and multiple device serials.

## Onboarding Tips
- Review `config/settings.yaml` for all configurable options.
- Explore the `src/` folder for modular code organization.
- Use the Prometheus dashboard for real-time monitoring.
- Run unit tests in `tests/` to validate functionality.

---
For further details, see the README.md and inline code documentation.
