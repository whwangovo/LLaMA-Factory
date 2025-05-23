import json

def transform_json(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Transform the JSON structure
    transformed_data = []
    for entry in data:
        transformed_entry = {
            # "instruction": entry.get("instruction", ""),
            # "input": "",
            "question": entry.get("output", "")
            # "input": entry.get("output", "")
            # "chosen": entry.get("answer", ""),
            # "rejected": entry.get("predict", ""),
        }
        transformed_data.append(transformed_entry)

    # Write the transformed data to the output JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(transformed_data, outfile, ensure_ascii=False, indent=4)

    print(f"Transformed data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_json_file = "data/test/ai_test_rebuild.json"  # Replace with your input JSON file
    output_json_file = "data/test/ai_test_rebuild.json"  # Replace with your desired output JSON file
    transform_json(input_json_file, output_json_file)