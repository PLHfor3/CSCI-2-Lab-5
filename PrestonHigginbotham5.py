import csv
import os.path
import re


def main():
    create_output_file(get_input_file_name())
    print("Data Stored!")


def get_input_file_name():
    while True:
        print("Input file name: ", end="")
        try:
            inputString = input("").strip()
            file = open(f"files\\{inputString}", 'r')
            return file
        except:
            print("File does not exist!")


def check_if_output_file_already_exists(fileName):
    if os.path.isfile(f"files\\{fileName}"):
        return True
    return False


def create_output_file(inputFile):
    outputFileName = input("Output File name: ").strip()
    if check_if_output_file_already_exists(outputFileName):
        duplicate_file_handler(inputFile, outputFileName)
    else:
        prepare_to_write_to_output(inputFile, outputFileName)


def duplicate_file_handler(inputFile, outputFileName):
    overwriteFileSelection = input("Overwrite existing file (y/n): ").strip().lower()
    while True:
        if overwriteFileSelection == "y":
            prepare_to_write_to_output(inputFile, outputFileName)
            break
        elif overwriteFileSelection == "n":
            outputFileName = input("New output file name: ").strip()
            if not check_if_output_file_already_exists(outputFileName):
                prepare_to_write_to_output(inputFile, outputFileName)
                break
            overwriteFileSelection = input("Overwrite existing file (y/n): ").strip().lower()
        else:
            overwriteFileSelection = input("Enter (y/n) ").strip().lower()


def prepare_to_write_to_output(inputFile, outputFileName):
    fileLines = inputFile.readlines()
    listOfEmails = read_input_from_file(fileLines, '^From: ')
    listOfTimeValues = read_input_from_file(fileLines, 'X-DSPAM-Processed: ')
    listOfConfidenceValues = read_input_from_file(fileLines, 'X-DSPAM-Confidence: ')
    write_output_to_file(listOfEmails, listOfTimeValues, listOfConfidenceValues, outputFileName)
    inputFile.close()


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


def read_input_from_file(fileLines, regexPattern):
    lineList = list()
    for line in fileLines:
        if (re.search(regexPattern, line)):
            lineList.append(line)
    return lineList


if __name__ == '__main__':
    main()
