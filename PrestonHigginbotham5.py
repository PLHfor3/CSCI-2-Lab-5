import csv
import os.path
import re


def main():
    while True:
        try:
            create_output_file(get_input_file_name())
        except NameError as e:
            print(e)
        else:
            print("Data Stored!")
            break


def get_input_file_name():
    inputString = ""
    print("Input file name: ", end="")
    inputString = input("").strip()
    if not os.path.isfile(f"files\\{inputString}"):
        raise NameError("File does not exist!")
    else:
        return inputString


def check_if_output_file_already_exists(fileName):
    if os.path.isfile(f"files\\{fileName}"):
        return True
    return False


def create_output_file(inputFileName):
    outputFileName = input("Output File name: ")
    if check_if_output_file_already_exists(outputFileName):
        duplicate_file_handler(inputFileName)
    else:
        prepare_to_write_to_output(inputFileName, outputFileName)


def duplicate_file_handler(inputFileName):
    overwriteFileSelection = input("Overwrite existing file (y/n): ").strip().lower()
    while True:
        if overwriteFileSelection == "y":
            prepare_to_write_to_output(inputFileName, outputFileName)
            break
        elif overwriteFileSelection == "n":
            outputFileName = input("New output file name: ")
            if not check_if_output_file_already_exists(outputFileName):
                prepare_to_write_to_output(inputFileName, outputFileName)
                break
            overwriteFileSelection = input("Overwrite existing file (y/n): ").strip().lower()
        else:
            overwriteFileSelection = input("Enter (y/n) ")


def prepare_to_write_to_output(inputFileName, outputFileName):
    listOfEmails = read_input_from_file(inputFileName, '^From: ')
    listOfTimeValues = read_input_from_file(inputFileName, 'X-DSPAM-Processed: ')
    listOfConfidenceValues = read_input_from_file(inputFileName, 'X-DSPAM-Confidence: ')
    write_output_to_file(listOfEmails, listOfTimeValues, listOfConfidenceValues, outputFileName)


def write_output_to_file(emailList, timeList, confidenceList, fileName):
    with open(f"files\\{fileName}", 'w', newline='') as csvfile:
        content = csv.writer(csvfile)
        content.writerow(["Email", "Time", "Confidence"])
        confidenceTotal = 0
        for i in range(len(emailList)):
            parsedEmailList = emailList[i].split()
            parsedTimeList = timeList[i].split()
            parsedConfidenceList = confidenceList[i].split()
            email = parsedEmailList[1]
            time = parsedTimeList[4]
            confidence = parsedConfidenceList[1]
            content.writerow([email, time, confidence])
            confidenceTotal += float(parsedConfidenceList[1])
        confidenceAverage = confidenceTotal / len(emailList)
        content.writerow(['', "Average", f'{confidenceAverage:.4f}'])


def read_input_from_file(fileName, regexPattern):
    file = open(f"files\\{fileName}", 'r')
    inputFileLines = file.readlines()
    lineList = list()
    for line in inputFileLines:
        if (re.search(regexPattern, line)):
            lineList.append(line)
    file.close()
    return lineList


if __name__ == '__main__':
    main()
