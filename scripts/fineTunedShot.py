import json
import re
import subprocess
import sys

def do_inference_and_log_result(model_path, prompt, output_file, adapter_file):
    # Construct the command to call the script with arguments
    command = ['/usr/bin/python3', '-m','mlx_lm.lora', '--model', model_path, '--adapter-file', adapter_file,'--prompt', prompt]

    # Call the script and capture its output
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        print(f"Error in script execution: {result.stderr}")
    else:
        text_input = result.stdout
        # Regular expression to move to the "[/INST]"
        matchEOI = re.search(r'\[/INST\]\s*(\{.*?\})', text_input, re.IGNORECASE)

        if matchEOI:
            text_input = matchEOI.group(1)
            # Regular expression to find the JSON object
            match = re.search(r'\{\s*"subject":\s*".*?",\s*"predicate":\s*".*?",\s*"object":\s*".*?"\s*\}', text_input, re.IGNORECASE)
            if match:
                json_str = match.group()
                try:
                    json_obj = json.loads(json_str)
                    json_dump = json.dumps(json_obj)
                    # Append the output to the file in jsonl format
                    output_file.write(json_dump + '\n')
                except json.JSONDecodeError:
                    print("Error: The extracted string is not a valid JSON.")
            else:
                output_file.write("{\"subject\":\"none\",\"predicate\":\"none\",\"object\":\"none\"}" + '\n')
                print("No JSON object found in the response.")
        else:
                output_file.write("{\"subject\":\"none\",\"predicate\":\"none\",\"object\":\"none\"}" + '\n')
                print("No [/INST] found in the response.")



def main (model_file, prompt_base, test_file, results_file, adapter_file):
    # Clear the content of the output file before the first write
    # open(zeroShot_results_file, 'w').close()
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
                prompt_final = prompt_base + prompt + "[/INST]"
                # prompt_final = prompt_base + prompt + "[/INST]{"
                with open(results_file, 'a') as fineTunedFile:
                    do_inference_and_log_result(model_file, prompt_final, fineTunedFile, adapter_file)

if __name__ == "__main__":
    if len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4],sys.argv[5])
    else:
        print("Fine-tuned benchmark requires 5 arguments.")
    sys.exit(0)
