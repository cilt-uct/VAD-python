import multiprocessing as mp
from detectVoiceInWave import detect_speech


if __name__ == "__main__":
    # Add relative paths of files to be analysed
    files = ["test_files/wav-sample.wav"]

    # Files to be run in parallel
    pool = mp.Pool(mp.cpu_count())
    pool.map(detect_speech, [record for record in files])
    pool.close()
