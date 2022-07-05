# generate training data
python create_labeled_queries.py

# shuffle data
shuf /workspace/datasets/fasttext/labeled_queries.txt > /workspace/datasets/fasttext/shuffled_labeled_queries.txt

# get training data
head -50000 /workspace/datasets/fasttext/shuffled_labeled_queries.txt > training_data.txt

# get test data
tail -10000 /workspace/datasets/fasttext/shuffled_labeled_queries.txt > test_data.txt

# train model
~/fastText-0.9.2/fasttext supervised -input training_data.txt -output query_classifier -lr 0.5 -epoch 5 -wordNgrams 2

# test model interactively
# ~/fastText-0.9.2/fasttext predict query_classifier.bin -

# test model @1
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt

# test model @3
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt 3

# test model @5
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt 5
