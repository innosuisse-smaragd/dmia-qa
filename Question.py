import csv


class Question:
    def __init__(self, id, text, answer):
        self.id = id
        self.text = text
        self.answer = answer


def read_csv(file_path):
    # Open the CSV file
    with open(file_path, "r") as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Skip the header row
        header = next(csv_reader)

        # Create a list to store objects
        object_list = []

        # Read the CSV data row by row
        for row in csv_reader:
            # Create an object using the row data
            my_object = Question(row[0], row[1], row[2])
            # Append the object to the list
            object_list.append(my_object)
    return object_list
