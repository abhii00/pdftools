import os
from posixpath import split
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

def split_pdf(directory, old_pdf_name, new_pdf_name, page_range): 
    """splits a pdf in the directory specified.

    Parameters:
    directory (str) - the directory path of the folder which the pdf to split is in.
    old_pdf_name (str) - the name of the pdf to split (excluding .pdf)
    new_pdf_name (str) - the name of the split pdf (excluding .pdf)
    page_range (str) - the page range to split for (inclusive)
    """

    #open old and new pdfs in dir specified
    old_pdf = PdfFileReader(open(f'{directory}\\{old_pdf_name}', 'rb')) 
    new_pdf = PdfFileWriter()

    #calculate pages
    page_ranges = (x.split('-') for x in page_range.split(','))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    #add pages iteratively from old pdf to new pdf
    for p in range_list:
        new_pdf.addPage(old_pdf.getPage(p - 1))

    #write new pdf to file
    new_pdf.write(open(f'{directory}\\{new_pdf_name}.pdf','wb'))

def merge_pdf(directory, files_to_merge_nums, new_pdf_name):
    """merges the pdfs in the directory specified.

    Parameters:
    directory (str) - the directory path of the folder containing the pdfs
    files_to_merge (list(int)) - a list of integers of the files to merge
    new_pdf_name (str) - the file name of the merged pdf (excluding .pdf)
    Returns:
    None    
    """

    #open old and new pdfs in dir specified
    old_pdfs = [file for file in os.listdir(directory)]
    pdfs_to_merge = [old_pdfs[i] for i in files_to_merge_nums]
    new_pdf = PdfFileMerger(strict=False)

    #add pdf iteratively from old pdf to new pdf
    for pdf_to_merge in pdfs_to_merge: 
        new_pdf.append(open(f'{directory}\\{pdf_to_merge}', 'rb'))

    #write new pdf to file
    new_pdf.write(open(f'{directory}\\{new_pdf_name}.pdf','wb'))

if __name__=='__main__':
    
    op = input('Split (s) or Merge (m)?')
    dir = input('Directory:')
    dir_dict = os.listdir(dir)
    for i, file in enumerate(dir_dict):
        print(f'{i}: {file}')

    if op in ['s', 'S']:
        old_num = int(input('Old File Number:'))
        old_name = dir_dict[old_num]
        new_names = input('CommaSpace-Sep New File Names (w/o .pdf):').split(', ')
        pgs = input('CommaSpace-Sep Page Ranges to Split for:').split(', ')
        for new_name, pg in zip(new_names, pgs):
            split_pdf(dir, old_name, new_name, pg)
    elif op in ['m', 'M']:
        new_name = input('New File Name:')
        files_to_merge = input('CommaSpace-Sep File Numbers:').split(', ')
        files_to_merge_num = [int(n) for n in files_to_merge]
        merge_pdf(dir, files_to_merge_num, new_name)
    else:
        print('Incorrect Configuration')
    