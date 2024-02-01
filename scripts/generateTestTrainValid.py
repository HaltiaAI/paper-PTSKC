import json
import re

# Path to your JSONL file
input_file_path = 'data/base.jsonl'
output_file_paths = ['data/train.jsonl', 'data/valid.jsonl', 'data/test.jsonl']
output_file_line_limits = [1000, 200, 200]  # Line limits for each output file

# Function to parse and reformat the output
def parse_and_reformat_output(output):
    # Parse the JSON content
    data = json.loads(output)

    # Extract the values
    statements = data.get('statements', [])
    if statements:
        subject = statements[0].get('subject', '')
        predicate = statements[0].get('predicate', '')
        object = statements[0].get('object', '')

        # Reformat and return
        return subject, predicate, object
    else:
        return "none", "none", "none"

def format_and_generate_json(line):
    # Parse the JSON content from the line
    data = json.loads(line)

    # Extract fields
    instruction_field = data.get('instruction', '')
    output_field = data.get('output', '')

    subject, predicate, object = parse_and_reformat_output(output_field)

    # Concatenate 'instruction' and 'output_field' fields
    new_text = f'<s>[INST]{instruction_field}[/INST] {{"subject":"{subject}", "predicate":"{predicate}", "object":"{object}"}}</s>'

    # Create a dictionary with the provided values
    new_data = {
        "text": new_text
    }
    return new_data

def main():
    try:
        with open(input_file_path, 'r') as input_file:
            for output_file_path, line_limit in zip(output_file_paths, output_file_line_limits):
                with open(output_file_path, 'w') as output_file:
                    for _ in range(line_limit):
                        line = input_file.readline()
                        # Break if the end of the file is reached
                        if not line:
                            break
                        # Write the modified data to the output file
                        new_data = format_and_generate_json(line)
                        output_file.write(json.dumps(new_data) + '\n')
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    print("Processing completed.Test, train and valid files are created.")