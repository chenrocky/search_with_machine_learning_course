# remove the first column to get an unlabeled list of product names
cut -d' ' -f2- /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/titles.txt

# feed the output from above to fasttext skipgram
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/titles.txt -output /workspace/datasets/fasttext/title_model

# get a sense of the quality of the candidate synonyms it generates
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model.bin

# normalize  product names
cat /workspace/datasets/fasttext/titles.txt | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_titles.txt

# feed the normalized titles from above to fasttext skipgram
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_titles.txt -output /workspace/datasets/fasttext/normalized_title_model

# get a sense of the quality of the candidate synonyms the normalized version generates
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/normalized_title_model.bin

# try increasing the number of epochs to 25 and setting -minCount to 20
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_titles.txt -output /workspace/datasets/fasttext/normalized_title_model -epoch 25 -minCount 20
