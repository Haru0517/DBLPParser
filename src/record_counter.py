from lxml import etree
from datetime import datetime
import csv
import codecs
import ujson
import re
from time import time
from collections import defaultdict

# all of the element types in dblp
all_elements = {"article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www"}

def log_msg(message):
    """Produce a log with current time"""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)


def context_iter(dblp_path):
    """Create a dblp data iterator of (event, element) pairs for processing"""
    return etree.iterparse(source=dblp_path, dtd_validation=True, load_dtd=True)  # required dtd


def clear_element(element):
    """Free up memory for temporary element tree after processing the element"""
    element.clear()
    while element.getprevious() is not None:
        del element.getparent()[0]


def count_record(dblp_path):
    """Parse specific elements according to the given type name and features"""
    log_msg("PROCESS: Start parsing...")

    counter = defaultdict(int)
    for _, elem in context_iter(dblp_path):
        if elem.tag in all_elements:
            # もしelemがレコード開始地点なら，
            counter[elem.tag] += 1
        clear_element(elem)

    print(counter)
    return counter



def main():
    dblp_path = 'dataset/dblp.xml'
    log_path = 'dataset/_dblp_parser_log.txt'
    try:
        context_iter(dblp_path)
        log_msg("LOG: Successfully loaded \"{}\".".format(dblp_path))
    except IOError:
        log_msg("ERROR: Failed to load file \"{}\". Please check your XML and DTD files.".format(dblp_path))
        exit()

    count_record(dblp_path)


if __name__ == '__main__':
    main()
