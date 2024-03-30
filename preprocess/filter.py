import glob
import sys
import os
import re
from tqdm import tqdm


def cleanup(text):
    # Remove Wiki markups, this may be caused by previous HTML conversion process
    text = text.replace("Template:Cat handler/numbered","").replace("Template:Category handler/numbered","")
    
    # Remove other inline templates
    text = re.sub("\[.*?\]","",line)
    
    # Make one continuous space.
    line = re.sub("\s+"," ",line)
    
    # Remove file references
    text = re.sub(r'File:.*(?:jpg|JPG|png|PNG|svg|SVG|JPEG|jpeg|gif|GIF|webm|WEBM)', "", text)
    
    # Define patterns to be removed
    patterns = [" Error: unknown archive URL", "Error: unknown archive URL",
                " (archived )", "(archived )",
                " (13px Page will play audio when loaded.)", "(13px Page will play audio when loaded.)",
                " (Registration required.)", "(Registration required.)",
                " (in Chinese.)", "(in Chinese.)",
                " (subscription or UK public library membership required.)", "(subscription or UK public library membership required.)",
                " (Subscription or UK public library membership required.)", "(Subscription or UK public library membership required.)",
                " (Subscription required.)", "(Subscription required.)",
                " (subscription required.)", "(subscription required.)",
                " (Warning: Check ISSN.)", "(Warning: Check ISSN.)",
                " (13px Page will play audio when loaded)", "(13px Page will play audio when loaded)",
                " (Registration required)", "(Registration required)",
                " (in Chinese)", "(in Chinese)",
                " (subscription or UK public library membership required)", "(subscription or UK public library membership required)",
                " (Subscription or UK public library membership required)", "(Subscription or UK public library membership required)",
                " (Subscription required)", "(Subscription required)",
                " (subscription required)", "(subscription required)",
                " (Warning: Check ISSN)", "(Warning: Check ISSN)",
                " (\"\")", "(\"\")"]
    for pattern in patterns:
        if pattern in text:
            text = text.replace(pattern,"")

    # Remove incomplete brackets and braces
    text = re.sub(r'\(s*\)', "", text)
    patterns = [["]","}"], ["[","{"]]
    patterns2 = [["[ ","{ "], [" ]"," }"]]
    for pattern, pattern2 in zip(patterns,patterns2):
        for p, p2 in zip(pattern, pattern2):
            if p not in text:
                text = text.replace(p2,"")

    # Remove unnecessary spaces at the end of sentences and in parentheses
    text = text.replace("( ","(")
    text = re.sub(r" \.$", ".", text.strip())

    text = re.sub(r'.*?', "", text)

    return text

def main():
    args = sys.argv
    taggedsents_path = args[1]
    save_path = args[2]
    files = glob.glob(taggedsents_path)

    for taggedsents in tqdm(files, total=len(files)):
        filtered_lines = []
        for line in open(taggedsents):
            # Remove inline templates
            text = text.replace(os.path.basename(taggedsents),"")
            line = cleanup(line.strip())

            # Delete less than 10 words
            if not re.match("[A-Z]",line) or line.count(" ") < 9:
                continue
            
            filtered_lines.append(line.strip())
        filtered_lines = set(filtered_lines)
        with open(os.path.join(save_path, os.path.basename(taggedsents)), "w")as f:
            f.write("\n".join(filtered_lines))

if __name__ == '__main__':
    main()