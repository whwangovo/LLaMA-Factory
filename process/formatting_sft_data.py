import json

def transform_json(input_file, output_file):
    # Read the input JSON file
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Transform the JSON structure
    transformed_data = []
    for entry in data:
        transformed_entry = {
            "instruction": entry.get("question", ""),
            "input": "",
            "output": entry.get("answer", "")
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
    input_json_file = "data/archived/zhulong@2@20250225_original.json"  # Replace with your input JSON file
    output_json_file = "data/finetune@zhulong@2@20250306.json"  # Replace with your desired output JSON file
    transform_json(input_json_file, output_json_file)