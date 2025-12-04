import csv
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt

MODEL = "jy46604790/Fake-News-Bert-Detect"
clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)


def save_results_to_csv(results_dict, filename="result"):

    df = pd.DataFrame(results_dict)
    print(df)
    df.to_csv(f"results/{filename}.csv", index=False)

    print(f"saved in: {filename}.csv")


def check_fake_news(news_list):
    results_list_dicts = []
    for news in news_list:
        text = news[0][0]
        true_label = news[1][0]

        pred = clf(text)[0]
        raw_label = pred['label']
        score = pred['score']

        if raw_label == 'LABEL_0':
            predicted_label = 'FAKE'
        elif raw_label == 'LABEL_1':
            predicted_label = 'REAL'
        else:
            predicted_label = raw_label

        result_dict = {
            'text': text,
            'true_label': true_label,
            'predicted_label': predicted_label,
            'score': score
        }

        results_list_dicts.append(result_dict)
    return results_list_dicts

def csv_to_list(csv_file):
    result_list = []

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            result_list.append([[row[0]], [row[1]]])
    return result_list

def number_of_articles(articles_list):
    count = len(articles_list)
    fake = []
    real = []

    for index, row in enumerate(articles_list):
        if row[1][0] == 'FAKE':
            fake.append(index+1)
        elif row[1][0] == 'REAL':
            real.append(index+1)

    print(count, "\n", "Fake:\n", fake, "\n", "Real:\n", real)

def evaluate_model(results_list, plot_file="model_results.png"):

    correct = sum(1 for r in results_list if r['true_label'] == r['predicted_label'])
    incorrect = len(results_list) - correct

    accuracy = (correct / len(results_list)) * 100
    print(f"Accuracy modelu: {accuracy:.2f}%")

    labels = ['Correct', 'Incorrect']
    counts = [correct, incorrect]
    colors = ['green', 'red']

    plt.figure(figsize=(6, 4))
    plt.bar(labels, counts, color=colors)
    plt.title('Model Resaults')
    plt.ylabel('Number of news')
    plt.ylim(0, len(results_list))

    for i, count in enumerate(counts):
        plt.text(i, count + 0.1, str(count), ha='center')

    plt.tight_layout()
    plt.savefig(f"results/{plot_file}")

if __name__ == "__main__":
    list = csv_to_list("data/news_2.csv")
    number_of_articles(list)
    save_results_to_csv(check_fake_news(list),"results_2")
    evaluate_model(check_fake_news(list),"model_results_2.png")

