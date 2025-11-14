#!/bin/bash

# Start the progress HTTP server in the background
python3 /workspace/serve_progress.py &

# Start Streamlit in the foreground
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
