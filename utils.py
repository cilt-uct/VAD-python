import os


def check_or_create_tmp_folder():
    directory = "temp"
    if not os.path.exists(directory):
        os.makedirs(directory)


def clean_up_if_required(temp_audio):
    head, tail = os.path.split(temp_audio)
    if head == "temp" and os.path.isfile(temp_audio):
        os.remove(temp_audio)
