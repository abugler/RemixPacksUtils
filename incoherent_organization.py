import json
import os

'''
Taking the files from original_files, querying the labels from raw JSON labels,
and creating symlinks
'''

input_path = "/home/data/RemixPacks/original_files/"

labels_path = "/home/data/RemixPacks/raw_json_labels/"

json_files = os.listdir("raw_json_labels")
all_specific_instruments = []
count = 0
for j in json_files:
    read_file = labels_path + j
    #obj = json.loads(read_file)
    with open(read_file, "r") as read:
        raw_file = json.load(read)
        if raw_file["completions"][0]["result"][0]["from_name"] != "category":
            continue

        simple_label = raw_file["completions"][0]["result"][0]["value"]["choices"]
        if "Garbage" in simple_label or "Silence" in simple_label:
            continue

        if raw_file["completions"][0]["result"][1]["from_name"] != "fine":
            complex_label = []
        else:
            complex_label = raw_file["completions"][0]["result"][1]["value"]["choices"]

        for label in complex_label:
            if label not in all_specific_instruments:
                all_specific_instruments.append(label)

        old_path = raw_file["task_path"]
        #cleaning to match original_files file
        new_path = old_path.replace("/remixpacks600/train_mp3", "/RemixPacks/original_files")
        new_path = new_path.replace("/bass/", "/")
        new_path = new_path.replace("/drums/", "/")
        new_path = new_path.replace("/vocals/", "/")
        new_path = new_path.replace("/other/", "/")
        new_file = new_path[:-4] #without the end tag

        for extension in [".wav", ".ogg", ".flac", ".mp3"]:
            if os.path.exists(new_file + extension):
                new_file = new_file + extension
                default_ext = extension
                break
        else:
            continue

        name = new_file[37:-4]
        if default_ext == ".flac":
            name = name[:-1]
        name = name.replace("/", " ")


        '''
        #simple labelling
        if len(simple_label) == 1:
            os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/simple/" + simple_label[0] + "/" + name + "(symlink)" + default_ext)
        elif len(simple_label) > 1:
            if "Bass" not in simple_label:
                os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/simple/Mix/No_Bass/" + name + "(symlink)" + default_ext)
            if "Drums" not in simple_label[0]:
                os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/simple/Mix/No_Drums/" + name + "(symlink)" + default_ext)
            if "Vocals" not in simple_label:
                os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/simple/Mix/No_Vocals/" + name + "(symlink)" + default_ext)
            if "Other" not in simple_label:
                os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/simple/Mix/No_Other/" + name + "(symlink)" + default_ext)

        #fine labelling: Note, there are very few "pure" instrument labelling, but I think it'll be ok
        if len(complex_label) == 1:
            pass
            #inst = complex_label[0].replace(" ", "_")
            #os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/fine/Pure/" + inst + "/" + name + "(symlink)" + default_ext)
        else:
            for label in complex_label:
                inst = label.replace(" ", "_")
                os.symlink(new_file, "/home/data/RemixPacks/symlinks_to_files/fine/Mixed/" + inst + "/" + name + "(symlink)" + default_ext)

        '''
