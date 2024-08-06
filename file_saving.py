import json

def save_to_file(filename, data):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")
