import json
import re
import subprocess
import sys

if __name__ == "__main__":
    # Set the local model file
    model_path = 'Mistral-7B-Instruct-v0.2-4bit-mlx'

    # Set the QLoRA adapter file
    qlora_adapter_file = "adapters_b4_l16_1000.npz"

    # Set the test and result files 
    test_file = 'data/test.jsonl'
    results_file_zero_shot = 'results/zeroShot.jsonl'
    results_file_few_shot = 'results/fewShot.jsonl'
    results_file_fineTuned_shot = 'results/fineTuned.jsonl'

    # The instruction bases for the proposed methods
    prompt_base_zero_shot = '''
    Suppose you are a "subject", "predicate" and "object" extraction agent from a given sentence. Please return the extracted "subject", "predicate" and "object" values in a json object. Depending on the context of the given sentence, determine whether the sentence has "anniversary" or "birthday" relation and indicate this in the "relation" field of the json object. Given sentence is 
    '''

    prompt_base_few_shot = '''
    Exclusively use the following examples to generate a single triple.
    Example1:
    Sentence: Today is my birthday.
    {"subject":"I", "predicate": "birthday", "object": "today"}
    Example2:
    Sentence: My uncle was born in 1960.
    {"subject":"My uncle", "predicate": "birthday", "object": "1960"}
    Example3:
    Sentence: The anniversary of my first job is on March 1st.
    {"subject":"My first job", "predicate": "anniversary", "object": "March 1st"}
    Example4:
    Sentence: The anniversary of my aunt and uncle marriage falls on July 31st.
    {"subject":"My aunt and uncle", "predicate": "anniversary", "object": "July 31st"}
    Create a single triple from the following sentence, please do not provide any alternatives, and return the answer as JSON object. Sentence: 
    '''
    prompt_base_fineTuned_shot = '[INST]'

    # Run zero shot prompting benchmark on model (not fine-tuned)
    command = ['/usr/bin/python3', 'scripts/zeroShot.py', model_path, prompt_base_zero_shot, test_file, results_file_zero_shot]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in zeroShot.py script execution: {result.stderr}")
        sys.exit(1)

    # Run few shot prompting benchmark on model (not fine-tuned)
    command = ['/usr/bin/python3', 'scripts/fewShot.py', model_path, prompt_base_few_shot, test_file, results_file_few_shot]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in fewShot.py script execution: {result.stderr}")
        sys.exit(2)

    # Run fine-tuned benchmark on model
    command = ['/usr/bin/python3', 'scripts/fineTunedShot.py', model_path, prompt_base_fineTuned_shot, test_file, results_file_fineTuned_shot, qlora_adapter_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in fine-tuning script execution: {result.stderr}")
        sys.exit(3)

    print("Benchmarks completed. Please check 'results/' directory for benchmark results")

