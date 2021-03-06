from vad import VoiceActivityDetector
from descriptions import *
import argparse
from config.logging_setup import logger


def save_to_file(empty, filename, result):
    f = open(filename, 'w')
    f.write('empty_venue={}\n'.format("true" if empty else "false"))
    f.write('empty_venue_result={}\n'.format("true" if result else "false"))
    f.close()


def get_speech_duration(speech):
    duration = 0
    for segment in speech:
        duration = duration + (segment["speech_end"]-segment["speech_begin"])
    return duration


def detect_speech(input_file, output_file="results.txt"):
    try:
        v = VoiceActivityDetector(input_file)
        raw_detection = v.detect_speech()
        logger.info("Speech detection complete")
        speech_labels = v.convert_windows_to_readible_labels(raw_detection)
        speech = get_speech_duration(speech_labels)
        logger.info("File: {}, Duration of video: {}, Duration of speech: {}".format(input_file, v.duration, speech))
        empty_venue = (speech / v.duration) < 0.05
        save_to_file(empty_venue, output_file, True)
        logger.info("File: {}, Empty: {}".format(input_file, empty_venue))
    except Exception as e:
        save_to_file(False, output_file, False)
        logger.error("Something went wrong while trying to detect speech: {}".format(e))


if __name__ == "__main__":
    logger.info("New empty venue detection kicked off")
    parser = argparse.ArgumentParser(description=ARG_DESCRIPTION)
    parser.add_argument('-i', '--input', dest='inputfile', metavar='(wav)', help=INPUT_DESCRIPTION)
    parser.add_argument('-o', '--output', dest='outputfile', metavar='(txt)', help=OUTPUT_DESCRIPTION)
    args = parser.parse_args()

    logger.info("Input file name: {}, output file name: {}".format(args.inputfile, args.outputfile))

    detect_speech(args.inputfile, args.outputfile)
