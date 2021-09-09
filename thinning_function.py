# !/usr/bin/env python
# encoding: utf-8

"""
SNP thinning function
Created by Andre E. Moncrieff on 2 July 2018.
Copyright 2018 Andre E. Moncrieff. All rights reserved.

"""


import argparse
import pandas
import numpy
import csv
from itertools import chain


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inp_name", required=True,
                        help="Enter the file name (including txt extension)",
                        type=str)
    args = parser.parse_args()
    return args


def read_in_csv(inp_name):
    #Note: Before reading vcf file in, remove header lines before line starting with '#CHROM'.
    #Also, remove the '#' from in front of 'CHROM'. Then change extension to .txt
    vcf_df = pandas.read_csv(inp_name, sep='\t', encoding = "ISO-8859-1")
    return vcf_df


def thinning(vcf_df):
    chrom_pos_dict = {}
    for chromosome in vcf_df.CHROM.unique():
        chrom_filtered_df = vcf_df.loc[vcf_df['CHROM'].isin([chromosome])]
        minim_position = chrom_filtered_df['POS'].min()
        sorted_chrom_filtered_df = chrom_filtered_df.sort_values(by='POS', ascending='TRUE')
        linkage_block = 75000
        thinned_chromosome_positions = []
        for index, row in sorted_chrom_filtered_df.iterrows():
            chrom_pos_list = []
            chrom_pos_list.extend([row['CHROM'], row['POS']])
            #print(list_of_lines)
            #print(row['CHROM'])
            POS = chrom_pos_list[1]
            if POS == minim_position:
                thinned_chromosome_positions.append(POS)
            elif POS > thinned_chromosome_positions[-1] + linkage_block:
                    thinned_chromosome_positions.append(POS)
            else:
                pass
        #create dictionary of a scaffold key and multiple position values
        chrom_pos_dict[chrom_pos_list[0]] = thinned_chromosome_positions
    return chrom_pos_dict


def dict_to_dataframe(chrom_pos_dict):
    df = pandas.DataFrame(list(chain.from_iterable(
        ((k, v) for v in vals) for (k, vals) in chrom_pos_dict.items())),
        columns=('CHROM', 'POS'))
    return df


def filter_vcf(df_SNPs_to_keep, vcf_df):
    chrom_list = df_SNPs_to_keep['CHROM'].tolist()
    pos_list = df_SNPs_to_keep['POS'].tolist()
    chrom_filtered_df = vcf_df.loc[vcf_df['CHROM'].isin(chrom_list)
                                  & vcf_df['POS'].isin(pos_list)]
    return chrom_filtered_df
    #return len(pos_list)


def write_to_csv(vcf_filtered):
    vcf_filtered.to_csv(path_or_buf='vcf_filtered.txt', sep='\t', header='TRUE')
    #Note: Manually add header and # back into vcf file

def main():
    args = parser()
    vcf_df = read_in_csv(args.inp_name)
    chrom_pos_dict = thinning(vcf_df)
    #print(chrom_pos_dict)
    df_SNPs_to_keep = dict_to_dataframe(chrom_pos_dict)
    #print(df_SNPs_to_keep)
    #print(vcf_df.head())
    vcf_filtered = filter_vcf(df_SNPs_to_keep, vcf_df)
    #print(vcf_filtered)
    #filter_vcf(df_SNPs_to_keep, vcf_df)
    write_to_csv(vcf_filtered)

if __name__ == '__main__':
    main()
