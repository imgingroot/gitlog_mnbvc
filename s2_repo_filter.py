# 逐行读取jsonl文件，加载成json，如果它的 stargazers_count watchers_count forks_count 都大于0 则把clone_url 保存到文本文件中。
# 输入的jsonl文件和输出的文本文件，都使用命令行参数传入，注意好异常处理

import json
import sys

if len(sys.argv) != 3:
    print("Usage: python s2_repo_filter.py input_file.jsonl output_file.txt")
    exit(1)

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

try:
    with open(input_file_name, "r") as input_file, \
         open(output_file_name, "w") as output_file:
        for line in input_file:
            try:
                data = json.loads(line)
                if isinstance(data, str):
                    data = json.loads(data)
                if (data.get("stargazers_count", 0) > 0 and
                    data.get("watchers_count", 0) > 0 and
                    data.get("forks_count", 0) > 0):
                    output_file.write(data["clone_url"] + "\n")
            except (KeyError, TypeError):
                print("ERROR: Invalid input format at line", line.strip(), file=sys.stderr)
                exit(-1)

except FileNotFoundError:
    print("ERROR: Input file not found", file=sys.stderr)
    exit(-2)

# print(f"Filtered clone urls saved to {output_file_name}")
