import subprocess
import os


def execute_command(command_string):
    # 使用 subprocess.run 执行命令
    result = subprocess.run(command_string.split(), capture_output=True, text=True, shell=True)

    # 如果你想获取命令的输出
    output = result.stdout
    error = result.stderr

    return output, error


def run_command_in_directory(dir_path, command):
    # 切换到指定目录
    original_dir = os.getcwd()  # 记录当前工作目录
    os.chdir(dir_path)  # 改变当前工作目录
    try:
        # 在新目录下执行命令
        process = subprocess.run(command, shell=True, check=True, text=True)
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败：{e}")
    finally:
        # 执行完命令后切换回原始目录
        os.chdir(original_dir)
