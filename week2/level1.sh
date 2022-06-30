# generate training data
python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products.txt

# shuffle data
shuf /workspace/datasets/fasttext/labeled_products.txt > /workspace/datasets/fasttext/shuffled_labeled_products.txt

# normalize data
cat /workspace/datasets/fasttext/shuffled_labeled_products.txt |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt

# get training data
head -10000 /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt > training_data.txt

# get test data
tail -10000 /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt > test_data.txt

# train model
~/fastText-0.9.2/fasttext supervised -input training_data.txt -output product_classifier -lr 1.0 -epoch 25 -wordNgrams 2

# test model interactively
# ~/fastText-0.9.2/fasttext predict product_classifier.bin -

# test model @1
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt

# test model @5
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt 5
