import subprocess
import os
from pathlib import Path

fontUse = '''
  fonts:
    - family: font
      fonts:
        - asset: fonts/NotoSansSC-Regular.ttf
'''

file = open('pubspec.yaml', 'r')
content = file.read()
file.close()
file = open('pubspec.yaml', 'a')
file.write(fontUse)
file.close()

subprocess.run(["flutter", "build", "windows"], shell=True)

file = open('pubspec.yaml', 'w')
file.write(content)

if os.path.exists("build/app-windows.zip"):
    os.remove("build/app-windows.zip")

version = str.split(str.split(content, 'version: ')[1], '+')[0]

# 1. Define your path
target_dir = Path("build/windows/x64/runner/Release")
output_file = f"build/windows/PicaComic-{version}-windows.zip"

# 2. Create the directory if it doesn't exist
# parents=True creates all missing folders in the path
# exist_ok=True prevents an error if the folder already exists
target_dir.mkdir(parents=True, exist_ok=True)

# 3. Ensure the output directory (build/windows) also exists
Path(output_file).parent.mkdir(parents=True, exist_ok=True)

# 压缩build/windows/x64/runner/Release, 生成app-windows.zip, 使用tar命令
# 4. Run the tar command
# Note: Removed shell=True for better security and reliability
subprocess.run([
    "tar", "-a", "-c", "-f", output_file, 
    "-C", str(target_dir), "."
], check=True)

issContent = ""
file = open('windows/build.iss', 'r')
issContent = file.read()
newContent = issContent
newContent = newContent.replace("{{version}}", version)
newContent = newContent.replace("{{root_path}}", os.getcwd())
file.close()
file = open('windows/build.iss', 'w')
file.write(newContent)
file.close()

subprocess.run(["iscc", "windows/build.iss"], shell=True)

with open('windows/build.iss', 'w') as file:
    file.write(issContent)
