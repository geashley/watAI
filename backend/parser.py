import json

def parse_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

if __name__ == '__main__':
    # Path to the JSON file
    json_file_path = 'data.json'
    
    # Parse the JSON file
    parsed_data = parse_json_file(json_file_path)
    
    # Print the parsed JSON in a pretty format
    print(json.dumps(parsed_data, indent=2))
