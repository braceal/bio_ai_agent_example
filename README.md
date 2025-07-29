# Bio AI Agent Example

A Python application for automated phylogenetic analysis using Galaxy workflows. This tool fetches protein sequences from NCBI, performs multiple sequence alignment, and builds phylogenetic trees.

## Prerequisites

- Python 3.8 or higher
- A Galaxy account with API access
- Internet connection for NCBI database queries

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd bio_ai_agent_example
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment to isolate dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Galaxy API key:

```
GALAXY_API_KEY=your_actual_api_key_here
```

To get your Galaxy API key:
1. Go to [Galaxy](https://usegalaxy.org)
2. Log in to your account
3. Navigate to User > Preferences > Manage API Key
4. Generate or copy your API key

## Usage

Run the phylogenetic analysis workflow:

```bash
python galaxy_workflow.py
```

The script will:
1. Connect to Galaxy using your API key
2. Create a new history for the analysis
3. Fetch flagellin protein sequences from multiple bacterial species
4. Perform multiple sequence alignment using MAFFT
5. Build a phylogenetic tree using IQ-TREE
6. Export the resulting tree file

## Project Structure

- `galaxy_workflow.py` - Main workflow script
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)
- `README.md` - This file

## Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

- **ImportError**: Make sure you've activated the virtual environment and installed dependencies
- **API Key Error**: Verify your Galaxy API key is correctly set in the `.env` file
- **Connection Error**: Check your internet connection and Galaxy server status