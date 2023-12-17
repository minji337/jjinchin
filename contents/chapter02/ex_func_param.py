def sum_data(data):
    return sum(data)

def average_data(data):
    return sum(data) / len(data)

def process_data(func, data):
    if len(data) >= 3:
        result = func(data)
        print(f"Processed result: {result}")

data = [10, 20, 30, 40, 50]

process_data(sum_data, data)         # Processed result: 150
process_data(average_data, data)     # Processed result: 30.0
