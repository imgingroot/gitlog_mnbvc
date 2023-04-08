# 从给定的目录，递归加载所有的jsonl文件，作为原始文件名，循环执行下面的程序
# 1.使用python调用执行s1.py 参数是原始文件名 和 s1_原始文件名
# 2.判断如果执行成功，继续
# 3.使用python调用执行s2.py 参数是s1_原始文件名 和 s1_原始文件名.txt
# 4.判断如果执行成功，继续
# 5.读取s1_原始文件名.txt，逐行遍历每行作为参数 使用python调用执行 s3.py


import os,sys
import subprocess
from tqdm.auto import tqdm

def run_s1(input_file):
    output_file = f"{input_file}.s1"
    try:
        subprocess.check_call([sys.executable, "s1_repo_jsonl_lite.py", input_file, output_file])
        return output_file
    except subprocess.CalledProcessError:
        print(f"ERROR: s1.py failed to execute on {input_file}", file=sys.stderr)
        return None

def run_s2(input_file):
    output_file = f"{input_file}.s2"
    try:
        subprocess.check_call([sys.executable, "s2_repo_filter.py", input_file, output_file])
        return output_file
    except subprocess.CalledProcessError:
        print(f"ERROR: s2.py failed to execute on {input_file}", file=sys.stderr)
        return None

def run_s3(line):
    try:
        subprocess.check_call([sys.executable, "s3_repo_clone.py",line,"--diff_filename","mnbvc_git_diff_commit.jsonl"])
    except subprocess.CalledProcessError:
        print(f"ERROR: s3.py failed to execute on {line}", file=sys.stderr)

def proc_one_file(file_path):
        # 运行s1.py
        s1_output_file = run_s1(file_path)
        if not s1_output_file:
            return

        # 运行s2.py
        s2_output_file = run_s2(s1_output_file)
        if not s2_output_file:
            return

        # 读取s1_XXX.txt并逐行运行s3.py
        with open(s2_output_file, "r") as f, \
            tqdm(total=100, desc=f'{s2_output_file} Progress', leave=False) as pbar:

            for line in f:
                pbar.update(1)
                line = line.strip()
                run_s3(line)

        print(f"Execution completed for {file_path}")


def main(dir_path):
    # 获取符合条件的文件路径
    file_paths = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".jsonl"):
                file_paths.append(os.path.join(root, file))

    # 循环执行
    for file_path in tqdm(file_paths):
        proc_one_file(file_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py path")
        exit(1)

    path = sys.argv[1]
    if os.path.isdir(path):
        main(path)
    elif os.path.isfile(path):
        proc_one_file(path)
    else:
        print("Error: Invalid path")
        exit(1)
