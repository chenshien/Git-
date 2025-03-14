#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time

def is_git_repo(path):
    """检查指定路径是否为Git仓库"""
    return os.path.isdir(os.path.join(path, '.git'))

def git_pull(repo_path):
    """在指定的Git仓库路径执行git pull操作"""
    try:
        print(f"\n正在更新仓库: {os.path.basename(repo_path)}")
        print(f"路径: {repo_path}")
        
        # 切换到仓库目录
        os.chdir(repo_path)
        
        # 执行git pull命令
        result = subprocess.run(['git', 'pull'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True,
                               encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ 更新成功: {os.path.basename(repo_path)}")
            print(f"输出信息: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ 更新失败: {os.path.basename(repo_path)}")
            print(f"错误信息: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ 更新过程中出错: {str(e)}")
        return False

def batch_update(root_dir, max_depth=2):
    """批量更新指定目录下的所有Git仓库，支持二级目录
    
    Args:
        root_dir: 根目录路径
        max_depth: 最大扫描深度，默认为2（支持二级目录）
    """
    print(f"开始批量更新Git仓库，根目录: {root_dir}\n")
    print(f"扫描深度: {max_depth} 级目录\n")
    
    # 统计信息
    total_repos = 0
    updated_repos = 0
    failed_repos = 0
    skipped_dirs = 0
    
    # 递归扫描目录函数
    def scan_directory(current_dir, current_depth=1):
        nonlocal total_repos, updated_repos, failed_repos, skipped_dirs
        
        # 如果当前目录是Git仓库，则更新它
        if is_git_repo(current_dir):
            total_repos += 1
            if git_pull(current_dir):
                updated_repos += 1
            else:
                failed_repos += 1
            # 如果是Git仓库，不再往下扫描
            return
        
        # 如果已达到最大深度，不再往下扫描
        if current_depth > max_depth:
            return
        
        # 获取所有子目录
        try:
            subdirs = [os.path.join(current_dir, d) for d in os.listdir(current_dir) 
                      if os.path.isdir(os.path.join(current_dir, d))]
            
            # 遍历每个子目录
            for subdir in subdirs:
                scan_directory(subdir, current_depth + 1)
                
        except Exception as e:
            print(f"扫描目录 {current_dir} 时出错: {str(e)}")
            skipped_dirs += 1
    
    # 开始扫描，跳过根目录自身的检查
    try:
        subdirs = [os.path.join(root_dir, d) for d in os.listdir(root_dir) 
                  if os.path.isdir(os.path.join(root_dir, d))]
        
        for subdir in subdirs:
            if is_git_repo(subdir):
                total_repos += 1
                if git_pull(subdir):
                    updated_repos += 1
                else:
                    failed_repos += 1
            else:
                print(f"检查子目录: {os.path.basename(subdir)}")
                scan_directory(subdir)
    except Exception as e:
        print(f"扫描根目录时出错: {str(e)}")
    
    # 打印统计信息
    print("\n" + "="*50)
    print(f"批量更新完成，统计信息:")
    print(f"- 检测到的Git仓库总数: {total_repos}")
    print(f"- 成功更新的仓库数: {updated_repos}")
    print(f"- 更新失败的仓库数: {failed_repos}")
    print(f"- 跳过的目录数: {skipped_dirs}")
    print("="*50)

def main():
    # 使用当前脚本所在目录作为根目录
    # root_dir = os.path.dirname(os.path.abspath(__file__))
    # 使用更兼容的方式获取运行目录，支持PyInstaller打包后的情况
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            root_dir = os.path.dirname(sys.executable)
        else:
            # 如果是普通Python脚本
            root_dir = os.path.dirname(os.path.abspath(__file__))
    except:
        # 如果上述方法失败，使用当前工作目录
        root_dir = os.getcwd()
    
    print("Git批量更新工具")
    print("="*50)
    
    # 确认是否继续
    confirm = input(f"将对目录 '{root_dir}' 下的所有Git仓库执行pull操作，是否继续？(y/n): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        sys.exit(0)
    
    # 执行批量更新
    start_time = time.time()
    batch_update(root_dir)
    end_time = time.time()
    
    print(f"\n总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main() 