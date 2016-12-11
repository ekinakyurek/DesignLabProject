import os
import datetime
from asrclient.voiceproxy_pb2 import AddDataResponse as AsrResponse

"""
use it like
./asrclient-cli.py -k <your-key> --callback-module advanced_callback_example --silent <path-to-your-sound.wav>
"""

session_id = "not-set"
start_timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

utterance_count = 0

def advanced_callback(asr_response, correction = 0):
    print "Got response:"
    print "end-of-utterance = {}".format(asr_response.endOfUtt)
    r_count = 0
    for r in asr_response.recognition:
        print "recognition[{}] = {}; confidence = {}".format(r_count, r.normalized.encode("utf-8"), r.confidence)
        print "utterance timings: from {} to {}".format(r.align_info.start_time+correction,r.align_info.end_time+correction)
        w_count = 0
        for w in r.words:
            print "word[{}] = {}; confidence = {}".format(w_count, w.value.encode("utf-8"), w.confidence)
            print "word timings: from {} to {}".format(w.align_info.start_time+correction,w.align_info.end_time+correction)
            w_count += 1
        r_count += 1


def advanced_utterance_callback(asr_response, data_chunks):    
    global utterance_count

    dirname = "./{0}_{1}/".format(start_timestamp, session_id)
    if not os.path.isdir(dirname):
        mkdir_p(dirname)
    print "Got complete utterance, for {0} data_chunks, session_id = {1}".format(len(data_chunks), session_id)

    with open("{0}/{1}_{2}.sound".format(dirname, session_id, utterance_count), "wb") as sound_file:
        for chunk in data_chunks:
            if chunk is not None:
                sound_file.write(chunk)

    with open("{0}/{1}_{2}.txt".format(dirname, session_id, utterance_count), "w") as txt_file:
        text = asr_response.recognition[0].normalized.encode("utf-8")
        if text is not None:
            txt_file.write(text)

    utterance_count += 1
