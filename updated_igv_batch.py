#!/usr/bin/env python
# coding: utf-8

""" Script Summary
A Python script that takes in parameters such as session, window size, batch file name, 
snapshot directory and variant positions,etc. to produce a unique batch script and automate 
the image generation process. 

Andrey Kuzin
"""

# In[2]:

#import needed packages
import argparse
import pandas as pd
import os
import time
import sys

def main():

    """ 
    Main Function
    """
    # Creates arguements so that parameters can be passed in from command line
    parser = argparse.ArgumentParser(description = "Generate a Batch Script")
    parser.add_argument('igvSession', type = str, help="Name of IGV Session")
    parser.add_argument('windowSize', type = str, help = "Size of Window")
    parser.add_argument('batchFile', type = str, help = 'Batch File Name')
    parser.add_argument('snapshotDir', type = str, help = 'Snapshots Directory')
    parser.add_argument('variantPos', type = str, help = 'Variant Positions')
    parser.add_argument('pathToIGV', type = str, help = 'Path to IGV batch')

    # Optional arguement that allows the user to decide whether they want to run the batch script automatically or just generate it
    parser.add_argument('--runScript', help = 'Choice to run script in IGV automatically (Optional)', action = 'store_true')
    args = parser.parse_args() 

    
    # Checks if file with Variant Positions Exists
    file_exists(args.variantPos, exit = True)

    #Checks if Snapshot directory exists and creates one if necessary
    check_dir(args.snapshotDir)

    # Creates pandas data fram object
    df = pd.read_csv(args.variantPos)

    # Adjusts columns to appropriate names 
    for i in range(0, len(df.columns)):
        if df.columns[i].lower() == 'chromosome' or df.columns[i].lower == 'chrom':
            df.rename(columns = {df.columns[i] : 'CHROM'}, inplace=True)
        elif df.columns[i].lower() == 'position' or df.columns[i].lower == 'pos':
            df.rename(columns = {df.columns[i] : 'POS'}, inplace=True)

    #Saves batch script to Snapshot Directory
    if ":\\" in args.batchFile or "/Volumes/" in args.batchFile:
       pathToFi = (args.batchFile + '.txt')
       outputFile = open(pathToFi, 'w')
    else:
       pathToFi = (os.path.join(args.snapshotDir, args.batchFile) + ".txt")
       outputFile = open(pathToFi, 'w')

    #prints the files that were used in igv session to create snapshots
    print_files_used(outputFile, args)

    #creates the batch script portion of text file 
    print_specs(args, outputFile)
    print_locations(df, outputFile)
    outputFile.close()

    print("Batch Script has been Successfully Generated")
    
    # Runs Batch Script in IGV automatically using terminal, if user specifies that they want to do it.
    if args.runScript:
        run_in_terminal(pathToFi, args.pathToIGV)

    #Closes IGV out once done taking snapshots
    lastFile = os.path.join(args.snapshotDir, "Chr" + str(df.loc[len(df.index)-1,'CHROM']) + "_" + str(df.loc[len(df.index)-1,'POS']) + ".png")
    i = False
    while i == False:
        time.sleep(1)
        i = file_accessible(lastFile, 'r')

    print("Process Complete...")
    os.system("taskkill /F /im javaw.exe")


def print_specs(args, outputFile):
    """
    This function prints out the format specifics to the text file.
    More specifically it prints out which igv session to load, what to set the maxPanelheight to,
    and specifies the Snapshot Directory where photos will be saved.
    """
    
    outputFile.write("load " + args.igvSession + "\ngenome hg19 \n")
    outputFile.write("maxPanelHeight " + args.windowSize + "\n")
    outputFile.write("snapshotDirectory " + args.snapshotDir + "\n") 


def print_locations(df, outputFile):
    """
    This function is responsible for looping through the spreadsheet and extracting the Chromosome and Position
    and then prints the information to the output text file.
    """

    for i in range(0, len(df.index)):
        outputFile.write("goto chr"+ str(df.loc[i,'CHROM']) + ":" + str(df.loc[i,'POS']-50) + "-" + str(df.loc[i,'POS']+50) + "\n" )
        outputFile.write("snapshot "+ "Chr" + str(df.loc[i,'CHROM']) + "_" + str(df.loc[i,'POS']) + ".png\n")

def file_exists(checkFile, exit = False):
    """
    This function checks if a file exists, and exits script if necessary
    """

    try:
        fileHolder = open(checkFile, 'r')
        fileHolder.close()
    except FileNotFoundError:
        print("ERROR: File '{}' containing Variant Positions does not exist!".format(checkFile))
        if exit == True:
            print("Exiting...")
            sys.exit()
    

def run_in_terminal(outputFile, pathToIGV):
    """
    This function automatically runs the created batch script in IGV
    """

    pathToBatch = os.path.abspath(outputFile)
    os.system(pathToIGV + ' -b ' + pathToBatch)

def print_files_used(outputFile, args):
    """
    This function prints out the files used at the top of the batch script
    """

    with open(args.igvSession) as f:
        outputFile.write("Files used in IGV session: " + "\n")
        for line in f:
            str = line
            if ("Resource path" in str) and ((".cram" in str) or (".bam" in str) or (".vcf" in str) or (".gz" in str)):
                data = str.split("\"")
                outputFile.write(data[1] + "\n")
        outputFile.write("\n")

def check_dir(directory):
    """This function checks if the snapshot directory exists and creates one if necessary"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('Snapshot directory was created')
    else:
        print("Snapshot directory already exists")

def file_accessible(filepath, mode):
    """Check if a file exists and is accessible. """
    try:
        fileHolder = open(filepath, mode)
        fileHolder.close()
    except FileNotFoundError:
        return False
    
 
    return True
    



if __name__ == "__main__":
    """ This runs when the application is run from the command line"""
    main()




# python updated_igv_batch.py Y:\data\igv_sessions\igv_test_session_ak_hg002.xml 400 FilesUsedBatch C:\Users\ank22\Documents\SnapShots\test C:\Users\ank22\Documents\PositionSet.csv C:\IGV_2.5.0\igv.bat --runScript
