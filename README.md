# paper-PTSKC
This is the official repository that contains code and access to dataset used for our paper titled `Prompt-Time Symbolic Knowledge Capture with Large Language Models`. 
This document is intended for researchers, developers and those who would like to build, run, and experiment with paper-PTSKC.  

## Prerequisites and Dependencies

* requires M series Apple silicon 
* Requires native Python 3.8 - 3.11. In our work, we utilized the system-managed Python installation on macOS, located at `/usr/bin/python3`, which is pre-installed with the operating system. To use it, you can either create aliases for `/usr/bin/python3` and `/usr/bin/pip3` as `python` and `pip` or directly reference them in every command involving `python` or `pip`. It's important to note that if you opt to use a different version of Python, you will need to update the Python path in the `runBenchmarks.py`` file.  
* requires macOS>= 13.3, Please note that MLX platform developers highly recommend using macOS 14 (Sonoma)

## Installation

`mlx-lm` is available on [PyPI]. Please refer to the official [MLX documentation] and  [MLX examples] for more details on the MLX platform.  
To install the Python API, run:

```bash
pip install mlx-lm
```

## How To Use

### Generating test, train, and validation files
To generate the `data/test.jsonl`, `data/train.jsonl`, and `data/valid.jsonl` files, run the following command:

```bash
python scripts/generateTestTrainValid.py
```

Details about the dataset generation are as follows: 
* `data/base.jsonl` is the fundemental dataset file that holds 1600 user-prompt and prompt response pairs.
* `generateTestTrainValid.py` script parses the base file and generates the required files for (Q)LoRA and performance evaluation. Please note that the generated output format is compatibale with `Mistral-7B-Instruct` model. Modifications might be required for different instruction formats.
* The number of lines that each output file will contain can be configured from `generateTestTrainValid.py`.
* All generated files are written under `data` directory.

### Generating ground-truth file
To generate the `results/test_ground_truth.jsonl`file, run the following command:

```bash
python scripts/generateGroundTruth.py 
```

`generateGroundTruth.py` script processes the `data/test.jsonl` file and writes the expected prompt response for each user input. The generated ground-turth file will be used in performance evaluations.

### Model file
In our work, we utilize the 4-bit quantized and mlx-converted version of the `Mistral-7B-Instruct-v0.2` model. All model files must be placed under the `Mistral-7B-Instruct-v0.2-4bit-mlx` folder located in the main directory of our repository. To replicate our test results accurately, please download the [mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx] file from the mlx-community on Hugging Face and ensure it is placed in the specified path.

### Fine-tuning
In our paper, we run QLoRA finetuning with following parameters and generated the adapter file `adapters_b4_l16_1000.npz`. Please use the same naming for the adapter file to be able to run following scripts without any change.

```bash
python -m mlx_lm.lora --train --model Mistral-7B-Instruct-v0.2-4bit-mlx --iters 1000 --data ./data --batch-size 4 --lora-layers 16 --adapter-file adapters_b4_l16_1000.npz
```

### Running the benchmarks
The proposed zero-shot prompting, few-shot prompting and fine-tuning methods are implemented in files `zeroShot.py`, `fewShot.py`, and `fineTunedShot.py`, respectively.  
The `runBenchmarks.py` script calls these methods, reading input from `data/test.jsonl` and writing the results to the `results` directory.

```bash
python scripts/runBenchmarks.py
```

### Evaluation
`calculateF1Score.py` script compares each method's result file with the ground-truth file and calculates precision, recall and f1-score. All results are written to the `evaluation_results.txt` file under `results` directory.

```bash
python scripts/calculateF1Score.py
```

## Troubleshooting
* if any script complains about jinja2 library please install it seperately using the following command:
```bash
pip install jinja2
```

## Cite
Will be updated when available


[PyPI]: https://pypi.org/project/mlx-lm/
[MLX documentation]: https://ml-explore.github.io/mlx/build/html/install.html
[MLX examples]: https://github.com/ml-explore/mlx-examples
[mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx]: https://huggingface.co/mlx-community/Mistral-7B-Instruct-v0.2-4bit-mlx/tree/main
