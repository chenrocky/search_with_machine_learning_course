import pandas as pd


# read in labaled products as list
products = []
with open("/workspace/datasets/fasttext/labeled_products.txt") as f:
    for line in f:
        s = line.split(" ", 1)
        products.append((s[0], s[1]))

# get df from list
df_products = pd.DataFrame(products, columns=["label", "title"])

# get value counts of labels that are ge 500
gt_500_products = list(df_products["label"].value_counts().loc[lambda x : x>=500].index)

# filter out rows with product labels with lt 500 occurances
df_filtered = df_products[df_products["label"].isin(gt_500_products)].reset_index(drop=True)

# turn filtered df into list
pruned_products = list(df_filtered["label"] + " " + df_filtered["title"])

# write
with open("/workspace/datasets/fasttext/pruned_labeled_products.txt", "w") as f:
    for product in pruned_products:
        f.write(product)
