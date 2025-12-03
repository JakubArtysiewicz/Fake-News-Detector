import csv

def csv_to_list(csv_file):
    list = []

    with open(csv_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            list.append([[row[0]], [row[1]]])
    return list

def number_of_articles(list):
    count = len(list)
    fake = []
    real = []
    for index, row in enumerate(list):

        if row[1][0] == 'FAKE':
            fake.append(index+1)
        elif row[1][0] == 'REAL':
            real.append(index+1)

    print(count, "\n", "Fake:\n", fake, "\n", "Real:\n", real)



if __name__ == "__main__":
    list = csv_to_list("data/wiadomosci.csv")
    number_of_articles(list)