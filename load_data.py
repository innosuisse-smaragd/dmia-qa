def load_text(file_path):
    # Read lines from the file and store them in a list
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Remove newline characters and whitespace from each line
    return [line.strip() for line in lines]
