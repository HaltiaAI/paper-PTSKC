import json
import re

# Path to your JSONL file
input_file_path = 'data/test.jsonl'
output_file_path = 'results/test_ground_truth.jsonl'

# Function to parse and reformat the text
def parse_and_reformat_text(text):
    # Extract JSON part from the string
    json_str = re.search(r'{.*}', text, re.IGNORECASE).group()

    # Parse the JSON content
    data = json.loads(json_str)

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

    # Extract text field
    text_field = data.get('text', '')

    # Extract JSON part from the string
    json_str = re.search(r'{.*}', text_field, re.IGNORECASE).group()

    return json_str

def main():
    try:
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
            for line in input_file:
                # Write the modified data to the output file
                new_data = format_and_generate_json(line)
                output_file.write(new_data + '\n')
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    print("Processing completed. test_ground_truth.jsonl file generated.")