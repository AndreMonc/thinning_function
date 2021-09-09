# thinning_function.py: A program to thin SNPs in VCF files.

##### Written by Andre E. Moncrieff, 2018.

## Introduction 

This program serves to select variants in a VCF file based on a specified distance (default is 75kb) and then write these selected variants to a new file. This program works by selecting the first variant on a "chromosome" ('CHROM' column in VCF file) and then selecting subsequest variants that are >75kb from the first or previous variant,marching down the "chromosome" through the final variant. This maximizes the number of selected (and putatively unlinked) variants on each "chromosome". VCFtools has a thinning function, which, in theory, does a similar process, but I found this tool to not always perform as expected, sometimes including variants closer than the specified thinning distance. I was not able to find a satisfactory explanation for this behavior in VCFtools, so I wrote this program.

## Step-by-step instructions 
#### (*Sorry, a few quick manual steps--I know, needs an update!*)

- Remove the header lines in your VCF before the line starting with '#CHROM'
- Delete the '#' before 'CHROM'
- Change your vcf file extension to .txt
- Run: `python thinning_function.py --inp_name yourVCF.txt` 
- To change the thinning distance, update the "linkage block" variable in the .py script
- In the output file, add '#' before 'CHROM', add full VCF header info, and change extension back to .vcf

## Citation
[![DOI](https://zenodo.org/badge/404800974.svg)](https://zenodo.org/badge/latestdoi/404800974)

**Moncrieff, A.E.** 2018. Thinning_function v1.0: a program to thin SNPs in VCF files. DOI:10.5281/zenodo.2540861


