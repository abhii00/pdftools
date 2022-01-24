import os
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
    old_pdf = PdfFileReader(open(directory+'/'+old_pdf_name+'.pdf', 'rb')) 
    new_pdf = PdfFileWriter()

    #calculate pages
    page_ranges = (x.split('-') for x in page_range.split(','))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    #add pages iteratively from old pdf to new pdf
    for p in range_list:
        new_pdf.addPage(old_pdf.getPage(p - 1))

    #write new pdf to file
    new_pdf.write(open(directory+'\\'+new_pdf_name+'.pdf','wb'))

def merge_pdf(directory, new_pdf_name):
    """merges the pdfs in the directory specified.

    Parameters:
    directory (str) - the directory path of the folder containing the pdfs
    new_pdf_name (str) - the file name of the merged pdf (excluding .pdf)
    Returns:
    None    
    """

    #open old and new pdfs in dir specified
    old_pdfs = [name for name in os.listdir(directory)]
    new_pdf = PdfFileMerger(strict=False)

    #add pdf iteratively from old pdf to new pdf
    for old_pdf in old_pdfs: 
        new_pdf.append(open(directory+'\\'+old_pdf, 'rb'))

    #write new pdf to file
    new_pdf.write(open(directory+'\\'+new_pdf_name+'.pdf','wb'))

if __name__=='__main__':
    
    op = input('Split (s) or Merge (m)?')
    dir = input('Directory:')
    print('\n'.join(os.listdir(dir)))

    if op in ['s', 'S']:
        old_name = input('Old File Name:')
        new_name = input('New File Name:')
        pg = input('Page Range to Split for:')
        split_pdf(dir, old_name, new_name, pg)
    elif op in ['m', 'M']:
        new_name = input('New File Name:')
        merge_pdf(dir, new_name)
    else:
        print('Incorrect Configuration')
    