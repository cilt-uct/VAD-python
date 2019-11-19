from vad import VoiceActivityDetector
from flac_to_wav import flac_to_wav
from descriptions import *
import argparse
import os
from config.logging_setup import logger


def save_to_file(empty, filename):
    f = open(filename, 'w')
    f.write('empty_venue={}\n'.format("true" if empty else "false"))
    f.close()


def get_speech_duration(speech):
    duration = 0
    for segment in speech:
        duration = duration + (segment["speech_end"]-segment["speech_begin"])
    return duration


def get_media_file(media_id):
    media_location = "/data/opencast/archive/mh_default_org/{}".format(media_id)

    most_up_to_date_media_folder = ""
    flac_name = ""
    file_list = []

    for dirName, subdirList, fileList in os.walk(media_location):
        most_up_to_date_media_folder = dirName
        file_list = fileList

    for file_name in file_list:
        if ".flac" in file_name:
            flac_name = file_name

    return most_up_to_date_media_folder, flac_name


def check_or_create_tmp_folder():
    directory = "temp"
    if not os.path.exists(directory):
        os.makedirs(directory)


def detect_speech(media_id, output_file):
    try:
        check_or_create_tmp_folder()

        most_up_to_date_media_folder, flac_name = get_media_file(media_id)
        logger.info("Fetching flac file from: {}, name of file is: {}".format(most_up_to_date_media_folder, flac_name))
        input_file = flac_to_wav(most_up_to_date_media_folder + "/" + flac_name)
        logger.info("Converted media file is located at: {}".format(input_file))

        v = VoiceActivityDetector(input_file)
        raw_detection = v.detect_speech()
        logger.info("Speech detection complete")

        speech_labels = v.convert_windows_to_readible_labels(raw_detection)
        speech = get_speech_duration(speech_labels)
        logger.info("File: {}, Duration: {}".format(input_file, speech))
        empty_venue = (speech / v.duration) < 0.11
        save_to_file(empty_venue, output_file)
        logger.info("File: {}, Empty: {}".format(input_file, empty_venue))

        os.remove(input_file)
        logger.info("Converted media {} has been deleted".format(input_file))
    except Exception as e:
        logger.error("Something went wrong while trying to detect speech: {}".format(e))


if __name__ == "__main__":
    logger.info("New empty venue detection kicked off")
    parser = argparse.ArgumentParser(description=ARG_DESCRIPTION)
    parser.add_argument('-i', '--input', dest='inputfile', metavar='(wav)', help=INPUT_DESCRIPTION)
    parser.add_argument('-o', '--output', dest='outputfile', metavar='(txt)', help=OUTPUT_DESCRIPTION)
    args = parser.parse_args()

    logger.info("Input file name: {}, output file name: {}".format(args.inputfile, args.outputfile))

    detect_speech(args.inputfile, args.outputfile)
