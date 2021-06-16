import pandas as pd
import argparse

def relative_abundance(SampleID):        
    abundance_sum = abundance[SampleID].sum()
    abundance[SampleID] = abundance[SampleID].apply(lambda x: x/abundance_sum)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--original', type=str, default='feature-table_w_tax.txt', help='The input original abundance data as tsv, columns represent samples and rows represent taxa.')
    parser.add_argument('-o', '--result', type=str, default='abundance.csv', help='The output abundancedata adjusted to csv')
    args = parser.parse_args()
    
    abundance = pd.read_csv(args.original, sep='\t')
    abundance.insert(0, 'Samples', abundance['taxonomy'])       
    abundance = abundance.drop(['#OTU ID', 'taxonomy'], axis=1)  
    abundance = abundance.drop_duplicates('Samples')            
    
    for i in abundance.columns[1:]:
        relative_abundance(i)
    
    abundance = abundance.fillna(0)
    abundance.to_csv(args.result, index=0)