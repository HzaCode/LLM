import pandas as pd

def calculate_precision_recall_f1(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def evaluate_model_performance(gold_standard_path, model_output_path):
    gold_standard_df = pd.read_csv(gold_standard_path)
    model_output_df = pd.read_csv(model_output_path)

    assert all(gold_standard_df['id'] == model_output_df['id'])

    # Define parameter
    parameters = [
        "Drug1", "Herb (Drug2)", "PK/PD", "Object", "Direction", 
        "DrugAdminRoute", "StudyTypes", "Interaction", "HerbAdminRoute", "Conclusions"
    ]

    results = {}
    total_tp = total_fp = total_fn = 0

   
    for param in parameters:
        column_tp = column_fp = column_fn = 0

        for i in range(len(gold_standard_df)):
            true_items = set(str(gold_standard_df.at[i, param]).split(';'))
            predicted_items = set(str(model_output_df.at[i, param]).split(';'))

            tp = len(true_items & predicted_items)
            fp = len(predicted_items - true_items)
            fn = len(true_items - predicted_items)

            column_tp += tp
            column_fp += fp
            column_fn += fn

        # Sum overall performance
        total_tp += column_tp
        total_fp += column_fp
        total_fn += column_fn

        precision, recall, f1 = calculate_precision_recall_f1(column_tp, column_fp, column_fn)
        results[param] = {
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
        }


    for param, scores in results.items():
        print(f"{param}: Precision={scores['Precision']:.2f}, Recall={scores['Recall']:.2f}, F1 Score={scores['F1 Score']:.2f}")


    overall_precision, overall_recall, overall_f1_score = calculate_precision_recall_f1(total_tp, total_fp, total_fn)
    print(f"Overall: Precision={overall_precision:.2f}, Recall={overall_recall:.2f}, F1 Score={overall_f1_score:.2f}")

if __name__ == "__main__":
    gold_standard_path = 'path_to_gold_standard.csv'
    model_output_path = 'path_to_model_output.csv'
    evaluate_model_performance(gold_standard_path, model_output_path)
