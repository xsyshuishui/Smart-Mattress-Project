# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a WebSocket-based smart mattress visualization demo that simulates real-time pressure sensor data transmission and airbag control for sleep monitoring and adjustment.

## Architecture

- **Backend (`server.py`)**: Python WebSocket server using the `websockets` library
  - Loads JSON sensor data from `json.txt` and cycles through it
  - Sends real-time pressure data every 1.5 seconds to connected clients
  - Receives and logs airbag control commands from clients
  - Uses asyncio for concurrent handling of send/receive operations

- **Frontend (`clients.html`)**: Simple HTML client with WebSocket connection
  - Receives and displays real-time sensor data from server
  - Contains commented code for sending airbag control commands

- **Data Format**: JSON objects containing:
  - `pressure`: 40x26 matrix (1040 values) representing sensor grid
  - `posture`: Sleep position ("no", "supine", "side")  
  - `airbag_status`: Current airbag state
  - `avg_pressure`, `PI`, `com_level`, `PAI`: Various comfort metrics
  - `time`, `side`: Timestamp and positioning data

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (REQUIRED)
source ../venv/bin/activate
```

### Running the Application
```bash
# First activate environment, then start WebSocket server
source ../venv/bin/activate
python server.py

# Open clients.html in web browser to connect
```

### Server Configuration
- Host: `127.0.0.1` (change to `0.0.0.0` for cross-device access)
- Port: `8000`
- Data send interval: `1.5` seconds
- Data source: `json.txt` (cycles through frames)

## Key Files

- `server.py`: WebSocket server implementation
- `clients.html`: Web client for data visualization  
- `json.txt`: Sensor data frames (no person → supine → side → no person cycle)
- `prompt.md`: Project requirements and specifications
- `气囊-压力传感器 标注布置图.png`: Sensor/airbag layout diagram

## Data Flow

1. Server loads all JSON frames from `json.txt` on startup
2. For each connected client, server creates concurrent send/receive tasks
3. Send task cycles through frames, broadcasting current sensor state
4. Receive task processes incoming airbag control commands
5. Client displays received data and can send control commands back

## Development Notes

- Uses modern `websockets` library (≥12) compatible with Python 3.12
- Server supports multiple concurrent client connections
- Error handling for malformed JSON and connection drops
- Data represents real smart mattress sensor grid (40x26 pressure points)