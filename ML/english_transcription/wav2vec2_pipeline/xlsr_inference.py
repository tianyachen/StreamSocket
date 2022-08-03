from pyAudioAnalysis import audioSegmentation as aS
from convert_time_format import convert_time_format
import getopt
import librosa
from split_helper import split_phrases, split_segments
import sys
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer, pipeline
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from urllib.request import urlopen, urlretrieve
import moviepy.editor as mp
import pyroomacoustics.denoise as denoise

def main(argv):
    ### read command line arguments
    try:
        opts, args = getopt.getopt(argv,"hi:o:c:p",["ifile=","ofile=","char_limit=", "periodic_limit="])
    except getopt.GetoptError:
        print('python xlsr_inference.py -i <inputfile> -o <outputfile> -c char_limit -p periodic_limit')
        sys.exit(2)
    input_filepath, output_filepath, char_limit, periodic_limit = '', '', 40, 4
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: python xlsr_inference.py -i <inputfile> -o <outputfile> -c char_limit -p periodic_limit')
            sys.exit()
        ### input audio filepath (wav or flac)
        elif opt in ("-i", "--ifile"):
            input_filepath = arg
        ### output srt filepath
        elif opt in ("-o", "--ofile"):
            output_filepath = arg
        ### character limit per line for captioning
        elif opt in ("-c", "--char_limit"):
            char_limit = arg
        ### time limit per phrase (in seconds) for captioning
        elif opt in ("-p", "--periodic_limit"):
            periodic_limit = arg

    # ### input audio filepath (wav or flac)
    # input_filepath = 'noisy_testset_wav\p257_023.wav'
    # ### output srt filepath
    # output_filepath = 'transcription_output.srt.txt'
    # ### character limit per line for captioning
    # char_limit = 40
    # ### time limit per phrase (in seconds) for captioning
    # periodic_limit = 4

    ### check to make sure input and output files are valid
    if input_filepath == '':
        raise FileNotFoundError('No file provided as input. Please use -i <inputfile> as part of command-line arguments')
    if output_filepath == '':
        raise FileNotFoundError('No file provided as output. Please use -o <outputfile> as part of command-line arguments')

    ### load flac or wav file
    try:
        url = input_filepath
        video_name = "video.mp4"
        filename = "audio.wav"
        urlretrieve(url, video_name)

        audio_detached = mp.VideoFileClip(video_name);
        audio_detached.audio.write_audiofile(filename)

        audio, sr = librosa.load(filename, sr=16000)
            # audio, sr = soundfile.read(input_filepath, samplerate=16000)
    except FileNotFoundError:
        print('Unable to find input file path:', input_filepath)
        sys.exit()


    ### language mapping ###
    MAPPING = {
        "de": 250003,
        "en": 250004, 
        "tr": 250023,
        "fa": 250029,
        "sv": 250042,
        "mn": 250037,
        "zh": 250025,
        "cy": 250007,
        "ca": 250005,
        "sl": 250052,
        "et": 250006,
        "id": 250032,
        "ar": 250001,
        "ta": 250044,
        "lv": 250017,
        "ja": 250012,
    }

    ### load pipeline with model and feature extractor
    asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-xls-r-2b-22-to-16", feature_extractor="facebook/wav2vec2-xls-r-2b-22-to-16")

    # select correct `forced_bos_token_id`
    forced_bos_token_id = MAPPING["en"]

    # https://github.com/tyiannak/pyAudioAnalysis/blob/944f1d777bc96717d2793f257c3b36b1acf1713a/pyAudioAnalysis/audioSegmentation.py#L670
    ### segment limits
    segmentLimits = aS.silence_removal(audio, sr, 0.05, 0.05, 1.0, 0.2)

    ### subdivide segments further based on periodic limit
    periodic_split = []
    for start, end in segmentLimits:
        if end - start < periodic_limit:
            periodic_split.append([start, end])
        else:
            periodic_split += split_segments(start, end, periodic_limit)
    segmentLimits = periodic_split
    # print("segmentLimits:", segmentLimits)

    ### process each segment
    transcriptions = []
    # for start, end in segmentLimits:
    for start, end in segmentLimits:
        split_audio, sr = librosa.load(filename, sr=16000, offset=start, duration=end - start)

        # https://pyroomacoustics.readthedocs.io/en/pypi-release/pyroomacoustics.denoise.spectral_subtraction.html
        ### spectral subtraction
        noise_reduced = denoise.spectral_subtraction.apply_spectral_sub(y, nfft=512, db_reduc=25, lookback=12, beta=30, alpha=1)
        
        ### run model
        t = asr(noise_reduced, forced_bos_token_id=forced_bos_token_id)['text']

        # # https://stackoverflow.com/questions/54587178/python-capitalize-first-character-of-words-in-a-string-except-one-word
        # ### lowercase all letters except for I
        # t = " ".join([word.lower() if word.lower() != 'i' else word for word in t.split()])
        # ### capitalize
        # t = t.capitalize()

        # print("transcription:", t)
        transcriptions.append(t)

    ### write transcriptions into output srt file
    # https://docs.fileformat.com/video/srt/
    try:
        with open(output_filepath, 'w') as f:
            ### one for each segment
            for t in range(len(transcriptions)):
                f.write(str(t+1))
                f.write('\n')
                ### convert segment limits from seconds to hours:minutes:seconds,milliseconds 00:00:00,000 format
                f.write(convert_time_format(segmentLimits[t][0]) + ' --> ' + convert_time_format(segmentLimits[t][1]))
                f.write('\n')
                ### split segments into multiple lines based on character limit per line
                segment = transcriptions[t]
                lines = split_phrases(segment, char_limit)
                for line in lines:
                    f.write(line) 
                    f.write('\n')
                f.write('\n')
    except FileNotFoundError:
        print('Unable to find output file path:', output_filepath)
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
