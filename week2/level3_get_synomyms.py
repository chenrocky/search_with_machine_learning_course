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
model = fasttext.load_model("/workspace/datasets/fasttext/normalized_title_model.bin")


# topword followed by neighbors exceeding threshold
output = []
threshold = 0.70
for word in topwords:
    # get nearest neighbor
    nn = model.get_nearest_neighbors(word)
    
    # filter on threshold
    synonyms = [x[1] for x in nn if x[0] >= threshold]
    
    # insert topword at beginning of list
    synonyms.insert(0, word)

    # csv
    stage = ', '.join(synonyms)

    # append to output list
    output.append(stage)

# write
with open("/workspace/datasets/fasttext/synonyms.csv", "w") as f:
    for item in output:
        f.write(item+'\n')
