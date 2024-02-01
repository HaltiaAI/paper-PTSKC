import json

def calculate_metrics(TP, FP, FN):
    # Calculate Precision
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0

    # Calculate Recall
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0

    # Calculate F1 Score
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

def load_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

def compare_prediction(prediction, ground_truth, compare_triples):
    # Initialize TP, FP, FN
    TP, FP, FN = 0, 0, 0

    # 1) Check if fields match
    if prediction.keys() != ground_truth.keys():
        FN = 1
        return TP, FP, FN

    # 2) Check if predicate prediction value is "none"
    if prediction["predicate"].lower() == "none":
        FN = 1
        return TP, FP, FN

    # 3) Check predicate value
    if prediction["predicate"].lower() != ground_truth["predicate"].lower():
        if prediction["predicate"].lower() in ["anniversary", "birthday"]:
            FP = 1
        else:
            FN = 1
        return TP, FP, FN

    if compare_triples:
        # 4) Check subject value
        if prediction["subject"].lower() == "none":
            FN = 1
            return TP, FP, FN
        if (prediction["subject"].lower() not in ground_truth["subject"].lower()) and (ground_truth["subject"].lower() not in prediction["subject"].lower()):
            FP = 1
            return TP, FP, FN

        if (prediction["subject"].lower() not in ground_truth["subject"].lower()) and (ground_truth["subject"].lower() not in prediction["subject"].lower()):
            FP = 1
            return TP, FP, FN

        # 5) Check object value
        if prediction["object"].lower() == "none":
            FN = 1
            return TP, FP, FN
        if (prediction["object"].lower() not in ground_truth["object"].lower()) and (ground_truth["object"].lower() not in prediction["object"].lower()):
            FP = 1
            return TP, FP, FN

    # If all checks pass, it's a true positive
    TP = 1
    return TP, FP, FN

def evaluate_results(result_files, ground_truth_file):
    ground_truths = load_jsonl(ground_truth_file)
    results = {file: load_jsonl(file) for file in result_files}

    evaluation = {}

    for file, result_data in results.items():
        relation_tp, relation_fp, relation_fn, triple_tp, triple_fp, triple_fn = 0, 0, 0, 0, 0, 0
        relation_rec, relation_pre, relation_f1, triple_rec, triple_pre, triple_f1 = 0, 0, 0, 0, 0, 0

        for prediction, ground_truth in zip(result_data, ground_truths):
            r_tp, r_fp, r_fn = 0, 0 , 0
            r_tp, r_fp, r_fn = compare_prediction(prediction, ground_truth, False)
            relation_tp += r_tp
            relation_fp += r_fp
            relation_fn += r_fn

            r_tp, r_fp, r_fn = 0, 0 , 0
            r_tp, r_fp, r_fn = compare_prediction(prediction, ground_truth, True)
            triple_tp += r_tp
            triple_fp += r_fp
            triple_fn += r_fn

        relation_rec, relation_pre, relation_f1 = calculate_metrics(relation_tp, relation_fp, relation_fn)
        triple_rec, triple_pre, triple_f1 = calculate_metrics(triple_tp, triple_fp, triple_fn)
        evaluation[file] = {
            'relation_matching': {'TP': relation_tp, 'FP': relation_fp, 'FN': relation_fn, "PRE": relation_pre, "REC": relation_rec, "F1": relation_f1},
            'triple_matching': {'TP': triple_tp, 'FP': triple_fp, 'FN': triple_fn, "PRE": triple_pre, "REC": triple_rec, "F1": triple_f1},
        }

    return evaluation

def write_evaluation_to_file(evaluation, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for file_name, data in evaluation.items():
            file.write(f'Results for {file_name}:\n')
            for match_type, scores in data.items():
                file.write(f'  {match_type}:\n')
                for score_type, value in scores.items():
                    file.write(f'    {score_type}: {value}\n')
            file.write('\n')

# Replace these file paths with your actual file paths
result_files = ['results/zeroShot.jsonl', 'results/fewShot.jsonl', 'results/fineTuned.jsonl']
ground_truth_file = 'results/test_ground_truth.jsonl'
evaluation_file = 'results/evaluation_results.txt'

evaluation = evaluate_results(result_files, ground_truth_file)
write_evaluation_to_file(evaluation, evaluation_file)

print("Precision, recall and f1-score calculated. Results are written to 'evaluation_results.txt'")
