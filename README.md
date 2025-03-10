# Git批量更新工具

这是一个简单的Python脚本，用于批量更新多个Git仓库。该工具会遍历指定目录下的所有子目录，检查每个子目录是否为Git仓库，如果是则执行`git pull`操作。

## 功能特点

- 自动遍历指定目录下的所有子目录
- 识别Git仓库（检查.git目录是否存在）
- 对每个Git仓库执行git pull操作
- 提供详细的执行结果和统计信息
- 支持中文输出
- 支持PyInstaller打包为可执行文件

## 使用方法

1. 确保您的系统已安装Python 3.x和Git
2. 将`git_batch_update.py`脚本放置在包含多个Git仓库的父目录中
3. 运行脚本：

```bash
python git_batch_update.py
```

## 使用PyInstaller打包

如果您想将脚本打包为独立的可执行文件，可以使用PyInstaller：

1. 安装PyInstaller：
```bash
pip install pyinstaller
```

2. 打包脚本：
```bash
pyinstaller --onefile git_batch_update.py
```

3. 打包完成后，可执行文件将位于`dist`目录中
4. 将可执行文件复制到您想要批量更新Git仓库的父目录中运行

## 注意事项

- 脚本默认使用其所在目录作为根目录进行扫描
- 当使用PyInstaller打包后，将使用可执行文件所在目录作为根目录
- 脚本会跳过不包含`.git`目录的子目录
- 如果某个仓库更新失败，脚本会继续处理其他仓库
- 脚本执行完毕后会显示统计信息

## 系统要求

- Python 3.x
- Git 命令行工具 