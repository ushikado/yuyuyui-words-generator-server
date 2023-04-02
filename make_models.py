import gzip
import os.path
import sys

import markovify
import MeCab
import pandas
import pickle


if len(sys.argv) != 4:
   print(
"""
usage: python make_models.py path/to/corpus.txt path/to/chara.txt path/to/output_model_dir
""")

output_model_dir = sys.argv[3]
main_charas = pandas.read_table(sys.argv[2], names=("character",), dtype=str)["character"]
corpus_df = pandas.read_table(sys.argv[1], names=(
    "0", "1",
    "character", "3", "4",
    "5", "normalized_message", "7"
    ), dtype=str)

tagger = MeCab.Tagger("-Owakati")

model_dict = {}
for character in main_charas:
    wakati_texts = ""
    for text in corpus_df[corpus_df["character"] == character]["normalized_message"]:
        wakati_text = tagger.parse(text)  # 最後に \n が追加される
        wakati_texts += wakati_text
    model_dict[character] = markovify.NewlineText(wakati_texts, state_size=2)

# 保存

for character in model_dict:
    model_path = os.path.join(output_model_dir, character + ".pkl.gz")
    with gzip.open(model_path, 'wb') as fp:
        pickle.dump(model_dict[character].to_dict(), fp)

# サンプル

for character in model_dict:
    sentence = model_dict[character].make_short_sentence(max_chars=120, min_words=1, tries=100)
    print("%s「%s」" % (character, ''.join(sentence.split())))
