import fasttext


# # read in top 1000 words as list
# with open("/workspace/datasets/fasttext/top_words.txt") as f:
#     topwords = f.readlines()

# read in top 1000 words as list
topwords = []
with open("/workspace/datasets/fasttext/top_words.txt") as f:
    for line in f:
        topwords.append(line.rstrip('\n'))

# load in synonym model
model = fasttext.load_model("/workspace/datasets/fasttext/title_model.bin")

# get nearest neighbor
nn = model.get_nearest_neighbors("black")

synonyms = [x[1] for x in nn]

synonyms.insert(0, "black")

output = ', '.join(synonyms)