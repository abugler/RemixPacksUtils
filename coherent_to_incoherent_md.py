import os
import os.path as path


def abs_listdir(p):
    return [path.join(p, f) for f in os.listdir(p)]
"""
This is a one-use script for moving musdb metadata around
"""
def to_incoherent(src, dst):
    songpaths = abs_listdir(src)
    for songpath in songpaths:
        sources = os.listdir(songpath)
        for source in sources:
            source_path = path.join(songpath, source)

            npy_path = path.join(source_path, source + ".wav.npy")
            songname = songpath[len(src)+1:]
            link_dst = path.join(dst, source, songname + ".wav.npy")
            os.makedirs(path.join(dst, source), exist_ok=True)
            print(f"{npy_path} -> {link_dst}")
            os.symlink(npy_path, link_dst)


help_text = "python coherent_to_incoherent_md.py <src> <dst>"

if __name__ == "__main__":
    from sys import argv
    if len(argv) != 3:
        print(help_text)
        sys.exit()
    to_incoherent(*argv[1:])
