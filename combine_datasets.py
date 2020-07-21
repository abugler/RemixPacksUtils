import os

src = "/home/ubuntu/musdb/train_16k"
dst = "/home/ubuntu/DBVO"

for root, _, files in os.walk(src):
    relative_path = root[len(src):]
    while relative_path and relative_path[0] == "/":
        relative_path = relative_path[1:]
    for file in files:
        src_path = os.path.join(root, file)
        dst_path = os.path.join(dst, relative_path, file)
        dst_dir = os.path.dirname(dst_path)
        os.makedirs(dst_dir, exist_ok=True)
        try:
            os.symlink(src_path, dst_path)
            print(f"{dst_path} successfully created for {src_path}")
        except FileExistsError:
            print(f"{dst_path} exists")
        
            