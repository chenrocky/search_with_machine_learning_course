# obtain the 1,000 most frequent words on normalized titles
cat /workspace/datasets/fasttext/normalized_titles.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > /workspace/datasets/fasttext/top_words.txt

# index
./index-data.sh -r -p /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json # DOES NOT WORK
