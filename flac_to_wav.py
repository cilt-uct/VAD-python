from os.path import splitext, split
from pydub import AudioSegment


def flac_to_wav(flac_path):
    path, file_name = split(flac_path)
    wav_path = "temp/{}".format(file_name)
    song = AudioSegment.from_file(flac_path)
    song.export(wav_path, format="wav")
    return wav_path
