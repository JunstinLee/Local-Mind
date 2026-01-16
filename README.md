<!-- 在 README.md 中 -->
<div align="center">
  <a href="./README_ZH.md"><img src="https://img.shields.io/badge/Lang-简体中文-red.svg" alt="Chinese"></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/Lang-English-blue.svg" alt="English"></a>
</div>
**Local Mind** is a local-first RAG (Retrieval-Augmented Generation) tool dedicated to stability, speed, and reproducibility. It stores user data entirely on the local device, reading and filtering file information through explicit engineering processes. The system prioritizes deterministic algorithms to answer questions, invoking local AI only when necessary, aiming to provide users with authentic and trustworthy productivity enhancements.
**Tip："Recommended to run overnight for large datasets" **

## Features

**One-Click Deployment & Dependency Management**
*   Provides a full installation package (~1.2GB) for one-click runtime environment configuration.
*   Includes a built-in Embedding Model downloader to manage model resources directly within the application.
*   *Note: Full functionality requires Ollama.*

**Supports Multiple File Types**: md, txt, log, html, pptx, pdf, docx

**Explicit Workflow Design**
Local Mind adopts a transparent "3+1" stage workflow, rejecting black-box operations:
1.  **Document Preparation Mode**: The "File Copy" button physically isolates target files into a preparation area, ensuring that only user-authorized data is processed.
2.  **Vectorization**:
    *   Supports one-click knowledge base construction.
    *   **Smart Deduplication**: A built-in check component automatically identifies and skips files that have already been vectorized to avoid redundancy.
3.  **Semantic Search Mode**: Based on local embedding models, the system performs high-precision semantic matching on vectorized files to quickly locate targets.

**Deterministic-First Q&A Engine**
The system handles the vast majority of queries through engineering means, **invoking local AI only when necessary**, to ensure precise and controlled results. The answer format automatically switches based on data characteristics:
*   **Table**: Triggered when there is an excessive number of relevant headings, or when a structured summary of dates or amounts is required.
*   **List**: Triggered when a small number of files are involved, or when numerical calculations are needed.
*   **Summary**: Triggered when the number of relevant files is $\le$ 3.

## Philosophy

*   **Complete Process Control**
    Users have the right to decide how to allocate their time and computing power. Local Mind rejects silent background operations; all high-consumption tasks (such as vectorization) are manually triggered by the user.

*   **Asset Status Transparency**
    Files are the user's core assets. Users have the right to know in real-time whether files are in the preparation, vectorization, or indexing state, rejecting the "black box" approach to data processing.

*   **Rejecting Uncontrollable Automation**
    **Why invoke local AI only when necessary?**
    Given limited local hardware and AI conditions, fully automatic RAG workflows lead to completely uncontrollable response times and result quality—it is like "a car with a blown tire speeding on the highway," where you never know what will happen next. Local Mind has invested heavily in building an engineering system solely to provide the most stable and factual answers under specific conditions.
## Quick Start
  There are 3 modes in total, with each tab representing a mode:
  
**Document Preparation Mode**
<img width="1915" height="1007" alt="Docs" src="https://github.com/user-attachments/assets/09f899eb-e0f1-4aeb-8727-87b85129e33f" />


Search Mode
<img width="1919" height="1004" alt="Search" src="https://github.com/user-attachments/assets/becc80bd-b392-41e7-a3c2-6270a5dfa9a3" />

Q&A Mode

<img width="1919" height="1003" alt="Q A" src="https://github.com/user-attachments/assets/526a79f1-64f0-4417-8dda-1d1d7b672d53" />



Upon entering the application, you first need to go to the Settings interface to download the embedding model.

<img width="1911" height="1008" alt="First" src="https://github.com/user-attachments/assets/8294b6c0-cf95-4800-9abf-df8b8aefd993" />

Once the download is complete, click the "Upload File" button to copy files to the preparation area.

<img width="1919" height="1002" alt="Second" src="https://github.com/user-attachments/assets/686c9088-9b7f-49ae-9f11-f9b6b75e3876" />


After file copying is complete, click the "Build Knowledge Base" button to vectorize the files and import them into the knowledge base.

<img width="1919" height="1013" alt="thrid" src="https://github.com/user-attachments/assets/88faf4d3-f6cf-4b41-8a9d-53c5972fbeb0" />


Once construction is complete, you can confidently use Search Mode and Q&A Mode.
## Use Cases

*   **Rapid Retrieval from Massive Files**: Proven in testing to precisely filter and locate 200, 70, or even just 1 relevant target file from 265 files within 30 seconds.
*   **Cross-Document Data Calculation**: Quickly extract monetary data from tables across multiple files, perform accurate aggregation calculations, and trace the original sources.
*   **On-Demand AI Intervention**:
    *   Once specific files are located, you can manually request the AI to extract specific content.
    *   When the system-generated "Summary" lacks detail, you can follow up with the AI for a deep analysis.
    *   When the content meets your needs but the language is a barrier, you can instruct the AI to translate it.

## Limitations & Known Issues

1.  **Vectorization Time**: Currently, vectorization operations rely on the **CPU**. Processing takes longer when file counts or data volumes are large (Reference data: Vectorizing 230 files takes about 30 minutes in a 32GB DDR5 RAM environment). Please plan your processing time accordingly.
2.  **Network Status Determination**: The system determines service status via Ollama interface signals rather than the actual service load completion status. Consequently, if network connectivity is poor, it may display "Not Downloaded" even if the model has already been downloaded.
3.  **Document Preparation Area Functionality**: Currently supports only file viewing and basic filtering; advanced file management features are not yet available.
4.  **Full Vectorization**: It is currently not possible to selectively vectorize files in the preparation area; all files entering the preparation area will be processed by default. Please remove irrelevant information in advance.
5.  **Storage Requirements**: The installation package size is approximately **1.2GB**. Please ensure sufficient disk space.
6.  **Language Support**: Currently supports **Simplified Chinese, en-US, and en-UK**; more languages will be added in the future.
7.  **File Copy Progress Inaccuracy**: The file copy progress bar may not reflect the precise progress in real-time. Please wait patiently.
8.  **Vectorization Time Estimation Deviation**: Estimated vectorization time is for reference only. **Do not interrupt vectorization midway**. In the current version, interrupting requires restarting from unprocessed files, and the interrupted progress cannot be perfectly resumed.
9.  **Embedding Model Status Detection Issue**: Even when network conditions are good and the embedding model is already downloaded, clicking the settings interface may sometimes prompt you to download the model. Simply click the download button and wait a few seconds to update the model status.
10. **Search Result Limit**: When the number of search results exceeds a certain limit, only the 20 most relevant results will be displayed.
