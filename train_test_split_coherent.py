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
    tracks = np.array([path.join(src_folder, f)
                       for f in os.listdir(src_folder)]
    ).astype(str)
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    if p == 1:
        train_tracks = test_tracks = tracks
    else:
        n = len(tracks)
        train_idx = np.random.choice(n, size=int(n * p), replace=False)
        train_mask = np.zeros(n, dtype=bool)
        train_mask[train_idx] = True
        train_tracks = tracks[train_mask]
        test_tracks = tracks[~train_mask]
    for src in train_tracks:
        relative_src = src[len(src_folder)+1:]
        dst = path.join(train_folder, relative_src)
        os.symlink(src, dst)
    for src in test_tracks:
        relative_src = src[len(src_folder)+1:]
        dst = path.join(test_folder, relative_src)
        os.symlink(src, dst)




help_text = "Usage: python train_test_split_coherent.py <src_folder> <train_folder> <test_folder> <p>"

if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) != 5:
        print(help_text)
        exit(2)
    argv[4] = float(argv[4])
    split(*argv[1:])
