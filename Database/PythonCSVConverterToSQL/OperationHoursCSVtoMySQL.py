import csv
import os

OPERATIONHOURS_CSV_FILEPATH = "Database/CSV/OperationHours.csv"
OPERATIONHOURS_SQL_FILEPATH = "Database/SQL/OperationHoursInsertData.sql"


def generate_insert_statement(row):
    columns = ["Place_ID", "Monday_Open", "Monday_Close", "Tuesday_Open", "Tuesday_Close",
               "Wednesday_Open", "Wednesday_Close", "Thursday_Open", "Thursday_Close",
               "Friday_Open", "Friday_Close", "Saturday_Open", "Saturday_Close", "Sunday_Open", "Sunday_Close"]

    insert_statement = "INSERT INTO OperationHours ("
    values = []

    for column in columns:
        if row[column] is not None and row[column] != "":
            insert_statement += column + ", "
            if isinstance(row[column], str):
                # Escape single quotes by doubling them
                value = row[column].replace("'", "''")
                values.append("'" + value + "'")
            else:
                values.append(str(row[column]))

    insert_statement = insert_statement.rstrip(
        ", ") + ") VALUES (" + ", ".join(values) + ");"
    return insert_statement


with open(OPERATIONHOURS_CSV_FILEPATH, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    total_rows = sum(1 for row in reader)
    csvfile.seek(0)  # Reset the file pointer
    next(reader)  # Skip the header row
    with open(OPERATIONHOURS_SQL_FILEPATH, 'w', encoding='utf-8') as sqlfile:
        for i, row in enumerate(reader, 1):
            insert_statement = generate_insert_statement(row)
            sqlfile.write(insert_statement)
            if i != total_rows:
                # Add a new line after each insert statement, except for the last one
                sqlfile.write("\n")
            print("Progress: {}/{}".format(i, total_rows))

print("DONE!")
