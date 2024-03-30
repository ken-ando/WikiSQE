import gzip
import json
import glob
import re
import os
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
import pysbd

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_sort_key(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def extract_strings(html, strip=False):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(strip=strip)
    return text.strip()

def filter_sentences(content, checked_sents):
    # Remove any numbered references (e.g., [1], [2]) from the content
    content = re.sub('\[[0-9]+\]', '', content)
    sents = seg.segment(content)
    sents = [s for s in sents if s.strip() != '']

    # Find set differences between current and already checked sentences to save costs
    new_sents = set(sents).difference(checked_sents)
    return list(new_sents), checked_sents.union(new_sents), sents

def extract_sentences(sents, tags, memory, save_path):
    for tag in tags:
        save_list = []
        tag = tag.lower()
        tagged_sents = [s for s in sents if tag in s.lower()]
        for sent in tagged_sents:
            flag = False
            # Check if a sentence starts with inline templates, and if so, attach a tag to the previous sentence.
            # This may be caused by errors during previous HTML conversion process.
            while sent.lower().strip()[:len(tag)] == tag:
                lastsent_index = memory.index(sent) - 1
                if lastsent_index >= 0:
                    sent = memory[lastsent_index]
                    flag = True
                    if len(sent) < len(tag):
                        break
                else:
                    break
            if flag:
                sent += ' ' +tag
            save_list.append(sent.strip().replace('\n',''))
        with open(os.path.join(save_path, tag.replace('/','[slash]')), 'a')as f:
            f.write('\n'.join(save_list))

def get_tags(path):
    tags = []
    # Open a file listed inline templates
    for line in open(path):
        # Remove "*" at the head
        if line[0] == '*':
            tags.append(line[1:])
        # Remove "(" at the head
        elif line[0] == '(':
            tags.append(line)
        # Add "[]" to other tags to fit representation of articles
        else:
            tags.append(f'[{line}]')
    return tags

def main():
    args = sys.argv
    tagsfile_path = args[1]
    tags = get_tags(tagsfile_path)

    json_dir_path = args[2]
    save_path = args[3]
    page_id = ''
    
    # Get a list of all JSON files in a directory
    files = glob.glob(os.path.join(json_dir_path, '*.json.gz'))
    files = sorted(files, key=natural_sort_key)
    for file in tqdm(files, total=len(files)):
        # Open a gzipped jsonl file in text mode with UTF-8 encoding
        with gzip.open(file, mode='rt', encoding='utf-8') as f:
            # Read each revision
            for line in f:
                data = json.loads(line)
                if data['page_id'] != page_id:
                    # If a page ID of current revision has changed, reset the set of checked sentences
                    checked_sents = set()
                    page_id = data['page_id']
                content = data['html']
                # Split into sentences and get new sentences seen for the first time  
                sents, checked_sents, memory = filter_sentences(extract_strings(content), checked_sents)
                # Extract tagged sentences and save them to file
                extract_sentences(sents, tags, memory, save_path)


if __name__ == '__main__':
    seg = pysbd.Segmenter(language='en', clean=False)
    main()