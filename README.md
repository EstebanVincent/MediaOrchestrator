# Media File Orchestrator

## Description
This script organizes media files by moving them through different storage stages: bronze, silver, and gold. Each stage represents a different level of processing or organization.

## Installation
To run this script, you need Python installed on your system. Additionally, ensure all dependencies are installed by navigating to the project's root directory and running:

```bash
pip install -r requirements.txt
```

### Download the World Borders Dataset
First, download the TM_WORLD_BORDERS_SIMPL dataset from [ThematicMapping.org](https://thematicmapping.org/downloads/world_borders.php).
This dataset contains the borders of countries in a shapefile format.

## Usage
To use this script, navigate to your project's root directory and run the following command:

```bash
python src/main.py --bronze <path-to-bronze> --silver <path-to-silver> --gold <path-to-gold>
```

### Arguments:
- `--bronze`: Required. Path to the bronze storage directory.
- `--silver`: Required. Path to the silver storage directory.
- `--gold`: Required. Path to the gold storage directory.
