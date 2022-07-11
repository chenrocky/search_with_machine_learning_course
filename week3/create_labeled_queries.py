import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/fasttext/labeled_queries.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
# lowercase
df["query_normalized"] = df["query"].str.lower()
# stripping quotation marks, and removing any other punctuation or unusual characters. Treat anything that’s not a number or letter as a space
df["query_normalized"].replace({r"[^a-zA-Z0-9]": " "}, regex=True, inplace=True)
# trim multiple spaces to a single space
df["query_normalized"].replace({r"\s+": " "}, regex=True, inplace=True)

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.
if len(list(df["category"].value_counts().loc[lambda x : x<args.min_queries].index)) == 0:
    done = True
else:
    done = False
while not done:
    # get categories to map to ancestor
    map_to_ancestors = list(df["category"].value_counts().loc[lambda x : x<args.min_queries].index)
    # get category to parent maps
    maps_df = parents_df[parents_df["category"].isin(map_to_ancestors)].reset_index(drop=True)
    maps_dict = dict(zip(maps_df["category"], maps_df["parent"]))
    # map categories to parent
    # TODO: instead of mapping all at once, could map one by one (in ascending order of occurance count) then check to see if the parent has enough after each map but cba
    df["category"].replace(maps_dict, inplace=True)
    # check if done
    if len(list(df["category"].value_counts().loc[lambda x : x<args.min_queries].index)) == 0:
        done = True
    else:
        done = False

# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
