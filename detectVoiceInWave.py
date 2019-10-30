from vad import VoiceActivityDetector
from descriptions import *
import argparse
from config.logging_setup import logger


def get_speech_duration(speech):
    duration = 0
    for segment in speech:
        duration = duration + (segment["speech_end"]-segment["speech_begin"])
    return duration


def detect_speech(input_file):
    v = VoiceActivityDetector(input_file)
    raw_detection = v.detect_speech()
    speech_labels = v.convert_windows_to_readible_labels(raw_detection)
    speech = get_speech_duration(speech_labels)
    logger.info("File: {}, Duration: {}".format(input_file, speech))
    empty_venue = (v.duration / speech if speech > 0 else 1) > 0.95
    logger.info("File: {}, Empty: {}".format(input_file, empty_venue))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=ARG_DESCRIPTION)
    parser.add_argument('-i', '--input', dest='inputfile', metavar='(wac)', help=INPUT_DESCRIPTION)
    parser.add_argument('-o', '--output', dest='outputfile', metavar='(txt)', help=OUTPUT_DESCRIPTION)
    args = parser.parse_args()

    detect_speech(args.inputfile)
