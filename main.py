import re
import matplotlib.pyplot as plt
import os

def read_routing_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def extract_routing_data(target, routing_data):
    measurements = []
    # Split the data into individual measurements
    measurements_data = re.split(r'[-]{10,}', routing_data)
    for measurement_data in measurements_data:
        if target in measurement_data:
            measurement = {}
            # Extract timestamp
            timestamp = re.search(r'Traceroute to .* at (.+?)\n', measurement_data).group(1)
            measurement['timestamp'] = timestamp
            # Extract routing hops
            hops = re.findall(r'\d+\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+) ms\s+(\d+\.\d+) ms\s+(\d+\.\d+) ms', measurement_data)
            measurement['hops'] = hops
            measurements.append(measurement)
    return measurements

def plot_routing_changes(target, routing_data):
    timestamps = [measurement['timestamp'] for measurement in routing_data]
    num_hops = [len(measurement['hops']) for measurement in routing_data]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, num_hops, marker='o')
    plt.title('Routing Path Stability for {}'.format(target))
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Hops')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analyze_routing_changes(target, routing_data):
    stable_targets = []
    changing_targets = []

    # Extract routing paths for each measurement
    routing_paths = [[hop[0] for hop in measurement['hops']] for measurement in routing_data]

    # Check if all routing paths are the same for each target
    if all(routing_paths[0] == paths for paths in routing_paths):
        print("For target '{}':".format(target))
        print("All measurements have the same routing path.")
        stable_targets.append(target)
    else:
        print("For target '{}':".format(target))
        print("Routing path changed in at least one measurement.")
        changing_targets.append(target)

    return stable_targets, changing_targets

def main():
    log_dir = "logs"  # Use the directory where your log files are
    targets = ["altnews.in", "www.2345.com"]

    stable_targets = []
    changing_targets = []

    # Dictionary to hold all routing data for each target
    all_routing_data = {target: "" for target in targets}

    # Read data from each file
    for filename in os.listdir(log_dir):
        for target in targets:
            if target.replace('.', '_') in filename:
                file_path = os.path.join(log_dir, filename)
                all_routing_data[target] += read_routing_data(file_path) + "\n---------------------------------------------\n"

    # Process data for each target
    for target in targets:
        routing_data = extract_routing_data(target, all_routing_data[target])
        if routing_data:  # Only plot and analyze if data was found
            plot_routing_changes(target, routing_data)
            stable, changing = analyze_routing_changes(target, routing_data)
            stable_targets.extend(stable)
            changing_targets.extend(changing)

    print("\nStable Targets:", stable_targets)
    print("Changing Targets:", changing_targets)

if __name__ == "__main__":
    main()