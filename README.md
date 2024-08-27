# Flow Log Parser

## Description

This Python script parses AWS flow log data and maps each entry to a tag based on a lookup table. It generates two CSV files:
1. `tag_counts.csv` - Contains counts of each tag.
2. `port_protocol_counts.csv` - Contains counts of port/protocol combinations.

**Note**: I assumed that the port in each port/protocol combination refers to either source or destination port.

## Files

1. **flow_logs.txt**: The input file containing flow log data.
2. **lookup_table.csv**: The CSV file with columns `dstport`, `protocol`, `tag`.
3. **protocol_numbers.csv**: The CSV file mapping protocol numbers to protocol names.

## Usage

### Command-Line Arguments

The script accepts up to four optional command-line arguments:

1. **lookup_table_filename**: Path to the lookup table CSV file (default: `lookup_table.csv`).
2. **flow_logs_filename**: Path to the flow logs text file (default: `flow_logs.txt`).
3. **tag_counts_filename**: Path to the output CSV file for tag counts (default: `tag_counts.csv`).
4. **port_protocol_counts_filename**: Path to the output CSV file for port/protocol counts (default: `port_protocol_counts.csv`).

### Running the Script

You can run the script with default filenames or provide your own:

- **Default usage**:
  ```bash
  python flow_log_parser.py
