import re
import matplotlib.pyplot as plt
import os
import numpy as np
import statistics

# Functions for ping measurements
def read_ping_logs(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

def extract_ping_data(ping_logs):
    # Regular expressions to extract loss rate and RTT
    loss_rate_pattern = r"(\d+)% packet loss"
    rtt_pattern = r"min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms"

    loss_rate = re.findall(loss_rate_pattern, ping_logs)
    rtt_data = re.findall(rtt_pattern, ping_logs)

    return loss_rate, rtt_data

def classify_loss_rate(loss_rate):
    if not loss_rate:
        return "loss free"
    loss_rate = int(loss_rate[0])
    if loss_rate < 5:
        return "minor losses"
    elif 5 <= loss_rate < 10:
        return "significant losses"
    else:
        return "major losses"

def plot_loss_rate_and_rtt(targets, loss_rates, rtt_data):
    # Plot loss rate
    plt.figure(figsize=(10, 5))
    for i, target in enumerate(targets):
        plt.plot(loss_rates[i], label=target)
    plt.title('Loss Rate Over Time')
    plt.xlabel('Time')
    plt.ylabel('Loss Rate (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot RTTs
    plt.figure(figsize=(10, 5))
    for i, target in enumerate(targets):
        rtts = [float(rtt[1]) for rtt in rtt_data[i]]  # Extract average RTT
        plt.plot(rtts, label=target)
    plt.title('Average RTT Over Time')
    plt.xlabel('Time')
    plt.ylabel('RTT (ms)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analyze_rtt(targets, rtt_data):
    for i, target in enumerate(targets):
        rtts = [float(rtt[1]) for rtt in rtt_data[i]]  # Extract average RTT
        print("For target '{}':".format(target))
        print("Minimum RTT:", min(rtts))
        print("Maximum RTT:", max(rtts))
        print("Mean RTT:", np.mean(rtts))
        print("Median RTT:", statistics.median(rtts))
        print()

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
    log_dir = "logs"
    targets = ["altnews.in", "www.2345.com"]

    stable_targets_routing = []
    changing_targets_routing = []
    all_routing_data = {target: "" for target in targets}  # Dictionary to hold all routing data for each target

    all_loss_rates = []
    all_rtt_data = []
    all_ping_logs = {target: [] for target in targets}  # Dictionary to hold all ping data for each target

    # Loop over each target
    for target in targets:
        # Perform traceroute measurements
        for filename in os.listdir(log_dir):
            if target.replace('.', '_') in filename:
                file_path = os.path.join(log_dir, filename)
                all_routing_data[target] += read_routing_data(file_path) + "\n---------------------------------------------\n"

        # Extract and analyze routing data for the current target
        routing_data = extract_routing_data(target, all_routing_data[target])
        if routing_data:  # Only plot and analyze if data was found
            plot_routing_changes(target, routing_data)
            stable, changing = analyze_routing_changes(target, routing_data)
            stable_targets_routing.extend(stable)
            changing_targets_routing.extend(changing)

            # Perform ping measurements
        for filename in os.listdir(log_dir):
            if target.replace('.', '_') in filename:
                file_path = os.path.join(log_dir, filename)
                ping_logs = read_ping_logs(file_path)
                all_ping_logs[target].append(ping_logs)

        # Extract and analyze ping data for the current target
        loss_rates = []
        rtt_data = []
        for ping_logs in all_ping_logs[target]:
            loss_rate, rtt = extract_ping_data(ping_logs)
            loss_rates.append(loss_rate)
            rtt_data.append(rtt)
        all_loss_rates.append(loss_rates)
        all_rtt_data.append(rtt_data)

        # Analyze the data for the current target after measurements
        # Classify targets based on loss rate
        loss_rate_classification = classify_loss_rate(all_loss_rates[-1][-1])
        print("For target '{}':".format(target))
        print("Loss Rate Classification:", loss_rate_classification)

        # Analyze RTT data
        analyze_rtt([target], [all_rtt_data[-1]])

        # Plot loss rate and RTTs over time
        plot_loss_rate_and_rtt([target], [all_loss_rates[-1]], [all_rtt_data[-1]])

    print("\nStable Targets (Routing):", stable_targets_routing)
    print("Changing Targets (Routing):", changing_targets_routing)

if __name__ == "__main__":
    main()

