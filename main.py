import csv
import argparse
from collections import defaultdict

def load_lookup_table(filename):
    """Load the lookup table from a CSV file into a dictionary."""
    lookup_table = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip().lower()
            lookup_table[(dstport, protocol)] = tag
    return lookup_table

def load_protocol_map(filename):
    """Load the protocol mapping from a CSV file into a dictionary."""
    protocol_map = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            decimal = row['Decimal'].strip()
            keyword = row['Keyword'].strip().lower()
            protocol_map[decimal] = keyword
    return protocol_map

def parse_flow_logs(flow_logs_filename, lookup_table, protocol_map):
    """Parse the flow logs and count tags and port/protocol combinations."""
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0

    with open(flow_logs_filename, mode='r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 11:
                continue  

            srcport = parts[5].strip()  
            dstport = parts[6].strip()  
            protocol_number = parts[7].strip()
            
            protocol = protocol_map.get(protocol_number, 'unknown').lower()
            
            tag = lookup_table.get((dstport, protocol), 'untagged')
            
            if tag == 'untagged':
                untagged_count += 1
            else:
                tag_counts[tag] += 1

            port_protocol_counts[(dstport, protocol)] += 1
            port_protocol_counts[(srcport, protocol)] += 1

    return tag_counts, port_protocol_counts, untagged_count

def write_results(tag_counts, port_protocol_counts, untagged_count, tag_counts_filename, port_protocol_counts_filename):
    """Write the results to output CSV files."""
    # Write tag counts
    with open(tag_counts_filename, mode='w') as file:
        file.write("Tag,Count\n")
        for tag, count in sorted(tag_counts.items()):
            file.write(f"{tag},{count}\n")
        file.write(f"Untagged,{untagged_count}\n")
    
    # Write port/protocol combination counts
    with open(port_protocol_counts_filename, mode='w') as file:
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            file.write(f"{port},{protocol},{count}\n")

def main():
    default_lookup_table_filename = 'lookup_table.csv'
    default_flow_logs_filename = 'flow_logs.txt'
    default_protocol_map_filename = 'protocol_numbers.csv'
    default_tag_counts_filename = 'tag_counts.csv'
    default_port_protocol_counts_filename = 'port_protocol_counts.csv'
    
    parser = argparse.ArgumentParser(description='Parse flow logs and map to tags based on a lookup table.')
    parser.add_argument('lookup_table_filename', nargs='?', default=default_lookup_table_filename, help='Path to the lookup table CSV file.')
    parser.add_argument('flow_logs_filename', nargs='?', default=default_flow_logs_filename, help='Path to the flow logs text file.')
    parser.add_argument('tag_counts_filename', nargs='?', default=default_tag_counts_filename, help='Path to the output CSV file for tag counts.')
    parser.add_argument('port_protocol_counts_filename', nargs='?', default=default_port_protocol_counts_filename, help='Path to the output CSV file for port/protocol counts.')

    args = parser.parse_args()

    lookup_table = load_lookup_table(args.lookup_table_filename)
    protocol_map = load_protocol_map(default_protocol_map_filename)
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(args.flow_logs_filename, lookup_table, protocol_map)
    write_results(tag_counts, port_protocol_counts, untagged_count, args.tag_counts_filename, args.port_protocol_counts_filename)

if __name__ == "__main__":
    main()
