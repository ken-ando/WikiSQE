## Installation
```shell-session
$ pip install -r ./requirements.txt
```

## Parsing JSON files
For parsing Wikipedia HTML JSON files.
```shell-session
$ pyton3 parse_jsonl.py ./tag_list.txt json_dir_path save_path
```
"tag_list.txt" is a file written inline templates list we made from https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Inline_Templates.
"json_dir_path" is a directory path including converted Wikipedia JSON files. These can be downloaded by https://github.com/epfl-dlab/WikiHist.html.

## Clean-up sentences
For filtering sentences.
```shell-session
$ pyton3 filter.py taggedsents_path save_path
```
"taggedsents_path" is the path of directory made before process.
