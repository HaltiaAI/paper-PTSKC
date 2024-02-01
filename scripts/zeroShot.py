import json
import re
import subprocess
import sys

def transform_json(input_json):
    # Extracting values from the input JSON object
    subject_val = input_json.get("subject", "")
    predicate_val = input_json.get("relation", "")  # Using 'relation' value as the new 'predicate'
    object_val = input_json.get("object", "")

    # Creating the new JSON object
    new_json = {
        "subject": subject_val.lower(),
        "predicate": predicate_val.lower(),
        "object": object_val.lower()
    }
    return new_json

def do_inference_and_log_result(model, prompt, output_file):
    command = ['/usr/bin/python3', '-m', 'mlx_lm.generate', '--model', model, '--prompt', prompt]

    # Call the script and capture its output
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        print(f"Error in script execution: {result.stderr}")
    else:
        text_input = result.stdout
        # Regular expression to find the JSON object
        match = re.search(r'\{\s*"subject":\s*".*?",\s*"predicate":\s*".*?",\s*"object":\s*".*?",\s*"relation":\s*".*?"\s*\}', text_input, re.IGNORECASE)
        if match:
            json_str = match.group()
            try:
                json_obj = json.loads(json_str)
                transformed_json_obj = transform_json(json_obj)
                json_dump = json.dumps(transformed_json_obj)
                # Append the output to the file in jsonl format
                output_file.write(json_dump + '\n')
            except json.JSONDecodeError:
                print("Error: The extracted string is not a valid JSON.")
        else:
            output_file.write("{\"subject\":\"none\",\"predicate\":\"none\",\"object\":\"none\"}" + '\n')
            print("No JSON object found in the text.")

def main (model_file, prompt_base, test_file, results_file):
    # Clear the content of the output file before the first write
    open(results_file, 'w').close()

    prompt = None
    with open(test_file, 'r') as testFile:
        for line in testFile:
            # Parse the JSON line
            json_obj = json.loads(line)

            # The instructions are in the 'text 'field
            text = json_obj.get('text', '')

            # Regular expression to find text between [INST] and [/INST]
            match = re.search(r'\[INST\](.*?)\[/INST\]', text, re.IGNORECASE)
            if match:
                prompt = match.group(1).strip()
                # prompt_zero_shot = prompt_base + prompt + "[/INST]\n"
                prompt_zero_shot = prompt_base + prompt + "\n "
                with open(results_file, 'a') as resultsFile:
                    do_inference_and_log_result(model_file, prompt_zero_shot, resultsFile)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
    else:
        print("ZeroShot prompting benchmark requires 4 arguments.")
    sys.exit(0)
