import os
import os.path as path
import numpy as np

"""
Take a folder containing audio files containing the following directory structure:
data:
    source1:
        audio1.wav
        audio2.wav
    source2:
        audio1.wav
        ...

Split it into two folders, train and test, where train will have `p` fraction
of files in each source, while test will have `1-p`. If `p` is 1, then 
train and test will be the same.

Use absolute paths for best results
"""
def split(src_folder, train_folder, test_folder, p):
    if p > 1 or p <= 0:
        raise ValueError("p must be between 0 and 1.")
    sources = os.listdir(src_folder)
    for source in sources:
        # make directories
        src_source = path.join(src_folder, source)
        train_source = path.join(train_folder, source)
        test_source = path.join(test_folder, source)
        os.makedirs(train_source, exist_ok=True)
        os.makedirs(test_source, exist_ok=True)
        audio_files = np.array(os.listdir(src_source)).astype(np.unicode_)
        # split files
        n = len(audio_files)
        indices = np.random.choice(n, size=min(int(np.floor(n * p)), n), replace=False)
        train_idx = np.full(len(audio_files), fill_value=False)
        train_idx[indices] = True
        train_files = audio_files[train_idx]
        if p == 1:
            test_files = train_files
        else:
            test_files = audio_files[~train_idx]
        # Create symlinks
        for filepath in train_files:
            src = path.join(src_source, filepath)
            dst = path.join(train_source, filepath)
            os.symlink(src, dst)
        if p == 1:
            continue
        for filepath in test_files:
            src = path.join(src_source, filepath)
            dst = path.join(test_source, filepath)
            os.symlink(src, dst)


help_text = "Usage: python <src_folder> <train_folder> <test_folder> <p>"

if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) != 5:
        print(help_text)
        exit(2)
    argv[4] = float(argv[4])
    split(*argv[1:])
