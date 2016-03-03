#!/usr/bin/python

import os
import sys
from collections import defaultdict
import re

'''
   Given an input file and a bunch of parameters, this module calculates
   2 things: the number of annotations per paper for every paper listed
   in the input file and the other is, calculate how many papers are
   associated with every protein annotation pair. The first helps to filter
   out high throughput papers (if required) and the second helps to identify 
   confident annotations. The assumption is annotations in more papers are
   considered confident over others.
'''

def count(infile, EEC=set([]), ann_conf_filter=False, paper_conf_filter=False):
    paper_conf = defaultdict(lambda:defaultdict(set))
    ann_conf = defaultdict(lambda:defaultdict(set))
    infile_handle = open(infile, 'r')

    print 'Creating paper-term frequency file.....'

    for line in infile_handle:
        if line[0] == '!':
            continue
        fields = line.strip().split('\t')
        if not fields[5] == '' and re.match('^PMID', fields[5]):
            paper_id = fields[5].split(':')[1]
        
            if (not EEC) or (fields[6] in EEC):
                if ann_conf_filter and paper_conf_filter:
                    ann_conf[fields[1]][fields[4]].add(str(paper_id))
                    paper_conf[paper_id][fields[4]] = 1
                elif ann_conf_filter:
                    ann_conf[fields[1]][fields[4]].add(str(paper_id))
                elif paper_conf_filter:
                    paper_conf[paper_id][fields[4]] = 1
    
    infile_handle.close()
    return ann_conf, paper_conf


if __name__ == '__main__':
    infile = sys.argv[1]
    paper_term = count(infile, EEC)
