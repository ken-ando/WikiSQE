## Usage
```shell-session
$ pip install -r ./requirements.txt
```
For parsing Wikipedia HTML json files.
```shell-session
$ pyton3 parse_jsonl.py ./tag_list.txt json_dir_path save_path
```
"tag_list.txt" is a file written inline templates list we made from https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Inline_Templates.
"json_dir_path" is directory path including converted Wikipedia json files. These can download by https://github.com/epfl-dlab/WikiHist.html.

For filtering sentences.
```shell-session
$ pyton3 filter.py taggedsents_path save_path
```
"taggedsents_path" is path of directory made by before process.
