import json
import sys
import os

#从输入的jsonl中，逐行遍历，在每行的json中的取出id\ clone_url\stargazers_count\watchers_count\forks_count\language\open_issues_count\ 并导出成新的jsonl
def process_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, "r") as input_file, \
            open(output_file_path, "w") as output_file:
            for line in input_file:
                try:
                    data = json.loads(line)
                    if isinstance(data, str):
                        data = json.loads(data)
                    result = {}
                    result["id"] = data["id"]
                    result["clone_url"] = data["clone_url"]
                    result["stargazers_count"] = data.get("stargazers_count", 0)
                    result["watchers_count"] = data.get("watchers_count", 0)
                    result["forks_count"] = data.get("forks_count", 0)
                    result["language"] = data.get("language", "")
                    result["open_issues_count"] = data.get("open_issues_count", 0)
                    output_file.write(json.dumps(result) + "\n")
                except KeyError:
                    print("ERROR: Invalid input format at line", line.strip(), file=sys.stderr)
                    exit(-1)

    except FileNotFoundError:
        print("ERROR: Input file not found", file=sys.stderr)
        exit(-2)

    # print("Output file:", output_file_path)

if __name__ == "__main__":
    # 检查命令行参数的个数
    if len(sys.argv) < 3:
        print("Usage: python s1_repo_jsonl_lite.py [input_file_path] [output_file_path]")
    else:
        # 读取命令行参数
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        # 处理输入文件并输出到输出文件
        process_file(input_file_path, output_file_path)
