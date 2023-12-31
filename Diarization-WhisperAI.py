# -*- coding: utf-8 -*-
"""Diarized_Whisper_AI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-7SlmLLlqEzGA_RfTUW7reUzr0XJDJGr

# Diarised transcriptions and translations using Pyannote & Whisper AI.

## Setup

### Install required libraries
"""

!pip install pydub
!pip install light-the-torch
!ltt install torch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1
!pip install  git+https://github.com/hmmlearn/hmmlearn.git
!pip install  git+https://github.com/pyannote/pyannote-audio.git@develop
!pip install git+https://github.com/openai/whisper.git

"""### Import all libraries


"""

from datetime import timedelta
from google.colab import drive
import json
import locale
locale.getpreferredencoding = lambda: "UTF-8"
from pathlib import Path
from pyannote.audio import Pipeline
from pydub import AudioSegment
import re
import torch
import whisper
import os

"""### Mount Google Drive"""

drive_mount_path = Path("/content/drive")
drive.mount(str(drive_mount_path))
drive_mount_path /= "MyDrive"

"""*italicised text*# Preparing the audio file

## Specify details of run

This script assumes that you have the source file (audio/video) saved on your google drive.

* Enter the full path to the source file on the `video_path` variable.
 * The google drive path must start /content/drive/MyDrive/...
* The `output_path` variable should be the full path to a folder where the files should be saved
 * This will also start /content/drive/MyDrive/...
 * If it doesn't exist, the script will create it
* The `access_token` is a requirement of the usage conditions for the diarisation software.
 * **Important:** To load the pyannote speaker diarization pipeline,
you must first accept the user conditions on both [hf.co/pyannote/speaker-diarization](https://hf.co/pyannote/speaker-diarization) and [hf.co/pyannote/segmentation](https://huggingface.co/pyannote/segmentation).
 * You'll need to create a huggingface account, then create an access token.
 * Then paste your access_token or login using `notebook_login` in the access_token variable below
 * Copy a token from your [Hugging Face tokens page](https://huggingface.co/settings/tokens) and paste it in the `access_token` box.

* The `audio_title` variable is simply the name of the document. This will be shown at the top of the html output.
"""

Source = 'File (Google Drive)'
#store_audio = True #@param {type:"boolean"}
#@markdown #### **Google Drive video or audio path (mp4, wav, mp3)**
video_path = "/content/drive/MyDrive/Colab_Notebooks/Whisper/KII_08_Teacher_Mwakilyambiti_17-08-23.MP3" #@param {type:"string"}
output_path = "/content/drive/MyDrive/Colab_Notebooks/Whisper/content/KII_08_Teacher_Mwakilyambiti_17-08-23" #@param {type:"string"}
output_path = str(Path(output_path))
audio_title = "KII_08 Teacher Mwakilyambiti 17-08-23" #@param {type:"string"}
access_token = "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" #@param {type:"string"}
language_source = 'Swahili' #@param ['any','Afrikaans','Arabic','Armenian','Azerbaijani','Belarusian','Bosnian','Bulgarian','Catalan','Chinese','Croatian','Czech','Danish','Dutch','English','Estonian','Finnish','French','Galician','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Kannada','Kazakh','Korean','Latvian','Lithuanian','Macedonian','Malay','Marathi','Maori','Nepali','Norwegian','Persian','Polish','Portuguese','Romanian','Russian','Serbian','Slovak','Slovenian','Spanish','Swahili','Swedish','Tagalog','Tamil','Thai','Turkish','Ukrainian','Urdu','Vietnamese','Welsh']
whisper_task = 'transcribe' #@param ['transcribe','translate']
model_size = 'large' #@param ['tiny', 'base', 'small', 'medium', 'large']
#append output path with task type
output_path = os.path.join(output_path, whisper_task)

print(output_path)

"""### Define Speakers

Change or add to the speaker names and collors bellow as you wish `(speaker, textbox color, speaker color)`.
"""

speakers = {
    'SPEAKER_00':('Speaker 01', '#e1ffc7', 'darkgreen'),
    'SPEAKER_01':('Speaker 02', 'white', 'darkorange'),
    'SPEAKER_02':('Speaker 03', 'yellow','darkblue'),
    'SPEAKER_03':('Speaker 04', 'green','black'),
    'SPEAKER_04':('Speaker 05', 'orange','darkblue')
    }
def_boxclr = 'white'
def_spkrclr = 'orange'

"""## Prepare data and folders

### Make an output folder based on `output_path`
"""

# Commented out IPython magic to ensure Python compatibility.
Path(output_path).mkdir(parents=True, exist_ok=True)
# %cd {output_path}
video_title = ""
video_id = ""

"""### Re-encode audio stream for input to pipeline"""

!ffmpeg -i {repr(video_path)} -vn -acodec pcm_s16le -ar 16000 -ac 1 -y input.wav

"""### Prepending a spacer

`pyannote.audio` seems to miss the first 0.5 seconds of the audio, and, therefore, we prepend a spcacer.
"""

spacermilli = 2000
spacer = AudioSegment.silent(duration=spacermilli)


audio = AudioSegment.from_wav("input.wav")

audio = spacer.append(audio, crossfade=0)

audio.export('input_prep.wav', format='wav')

"""## Diarization using Pyannote

[`pyannote.audio`](https://github.com/pyannote/pyannote-audio) is an open-source toolkit written in Python for **speaker diarization**.

Based on [`PyTorch`](https://pytorch.org) machine learning framework, it provides a set of trainable end-to-end neural building blocks that can be combined and jointly optimized to build speaker diarization pipelines.

`pyannote.audio` also comes with pretrained [models](https://huggingface.co/models?other=pyannote-audio-model) and [pipelines](https://huggingface.co/models?other=pyannote-audio-pipeline) covering a wide range of domains for voice activity detection, speaker segmentation, overlapped speech detection, speaker embedding reaching state-of-the-art performance for most of them.

### Define Pyannote pipeline
"""

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token= (access_token) or True )

"""### Define whether GPU or CPU is going to be used.
Almost not worth bothering with CPUs.
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipeline.to(device)

"""### Run pyannote.audio to generate the diarizations."""

DEMO_FILE = {'uri': 'blabla', 'audio': 'input_prep.wav'}
dz = pipeline(DEMO_FILE)

with open("diarization.txt", "w") as text_file:
    text_file.write(str(dz))

print(*list(dz.itertracks(yield_label = True))[:10], sep="\n")

"""### Prepare trimmed audio files according to the diarization"""

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s

"""### Group the diarization segments according to the speaker."""

dzs = open('diarization.txt').read().splitlines()

groups = []
g = []
lastend = 0

for d in dzs:
  if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
    groups.append(g)
    g = []

  g.append(d)

  end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
  end = millisec(end)
  if (lastend > end):       #segment engulfed by a previous segment
    groups.append(g)
    g = []
  else:
    lastend = end
if g:
  groups.append(g)
print(*groups, sep='\n')

"""### Save the audio part corresponding to each diarization group."""

audio = AudioSegment.from_wav("input_prep.wav")
gidx = -1
for g in groups:
  start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
  end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
  start = millisec(start) #- spacermilli
  end = millisec(end)  #- spacermilli
  gidx += 1
  #audio[start:end].export(str(gidx) + '.wav', format='wav')
  #print(f"group {gidx}: {start}--{end}")
  audio[start:end].export(str(gidx) + '.mp3', format='mp3')
  print(f"group {gidx}: {start}--{end}")

"""### Free up some memory by removing some variables"""

del   DEMO_FILE, pipeline, spacer,  audio, dz

"""# Transcription & Translation using Whisper AI

### Load model
"""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = whisper.load_model(model_size, device = device)

"""### Run whisper on all audio files. Whisper generates the transcription and writes it to a file.
This can take a long time, depending on your input file
"""

for i in range(len(groups)):
    audiof = str(i) + '.mp3'

    if whisper_task == 'transcribe':
        # Perform transcription
        result = model.transcribe(audio=audiof, language=language_source, word_timestamps=True)
    elif whisper_task == 'translate':
        # Perform translation
        result = model.transcribe(audio=audiof, language=language_source, word_timestamps=True, task = "translate")
    else:
        raise ValueError("Invalid whisper_task value. Use 'transcribe' or 'translate'.")

    # Save the result to a JSON file
    with open(str(i) + '.json', "w") as outfile:
        json.dump(result, outfile, indent=4)

"""### Generate the HTML and/or txt file from the Transcriptions and the Diarization

In the generated HTML,  the transcriptions for each diarization group are written in a box, with the speaker name on the top. By clicking a transcription, the embedded video jumps to the right time .
"""

preS = '\n<!DOCTYPE html>\n<html lang="en">\n\n<head>\n\t<meta charset="UTF-8">\n\t<meta name="viewport" content="whtmlidth=device-width, initial-scale=1.0">\n\t<meta http-equiv="X-UA-Compatible" content="ie=edge">\n\t<title>' + \
    audio_title+ \
    '</title>\n\t<style>\n\t\tbody {\n\t\t\tfont-family: sans-serif;\n\t\t\tfont-size: 14px;\n\t\t\tcolor: #111;\n\t\t\tpadding: 0 0 1em 0;\n\t\t\tbackground-color: #efe7dd;\n\t\t}\n\n\t\ttable {\n\t\t\tborder-spacing: 10px;\n\t\t}\n\n\t\tth {\n\t\t\ttext-align: left;\n\t\t}\n\n\t\t.lt {\n\t\t\tcolor: inherit;\n\t\t\ttext-decoration: inherit;\n\t\t}\n\n\t\t.l {\n\t\t\tcolor: #050;\n\t\t}\n\n\t\t.s {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t.c {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t.e {\n\t\t\t/*background-color: white; Changing background color */\n\t\t\tborder-radius: 10px;\n\t\t\t/* Making border radius */\n\t\t\twidth: 50%;\n\t\t\t/* Making auto-sizable width */\n\t\t\tpadding: 0 0 0 0;\n\t\t\t/* Making space around letters */\n\t\t\tfont-size: 14px;\n\t\t\t/* Changing font size */\n\t\t\tmargin-bottom: 0;\n\t\t}\n\n\t\t.t {\n\t\t\tdisplay: inline-block;\n\t\t}\n\n\t\t#player-div {\n\t\t\tposition: sticky;\n\t\t\ttop: 20px;\n\t\t\tfloat: right;\n\t\t\twidth: 40%\n\t\t}\n\n\t\t#player {\n\t\t\taspect-ratio: 16 / 9;\n\t\t\twidth: 100%;\n\t\t\theight: auto;\n\t\t}\n\n\t\ta {\n\t\t\tdisplay: inline;\n\t\t}\n\t</style>';
preS += '\n\t<script>\n\twindow.onload = function () {\n\t\t\tvar player = document.getElementById("audio_player");\n\t\t\tvar player;\n\t\t\tvar lastword = null;\n\n\t\t\t// So we can compare against new updates.\n\t\t\tvar lastTimeUpdate = "-1";\n\n\t\t\tsetInterval(function () {\n\t\t\t\t// currentTime is checked very frequently (1 millisecond),\n\t\t\t\t// but we only care about whole second changes.\n\t\t\t\tvar ts = (player.currentTime).toFixed(1).toString();\n\t\t\t\tts = (Math.round((player.currentTime) * 5) / 5).toFixed(1);\n\t\t\t\tts = ts.toString();\n\t\t\t\tconsole.log(ts);\n\t\t\t\tif (ts !== lastTimeUpdate) {\n\t\t\t\t\tlastTimeUpdate = ts;\n\n\t\t\t\t\t// Its now up to you to format the time.\n\t\t\t\t\tword = document.getElementById(ts)\n\t\t\t\t\tif (word) {\n\t\t\t\t\t\tif (lastword) {\n\t\t\t\t\t\t\tlastword.style.fontWeight = "normal";\n\t\t\t\t\t\t}\n\t\t\t\t\t\tlastword = word;\n\t\t\t\t\t\t//word.style.textDecoration = "underline";\n\t\t\t\t\t\tword.style.fontWeight = "bold";\n\n\t\t\t\t\t\tlet toggle = document.getElementById("autoscroll");\n\t\t\t\t\t\tif (toggle.checked) {\n\t\t\t\t\t\t\tlet position = word.offsetTop - 20;\n\t\t\t\t\t\t\twindow.scrollTo({\n\t\t\t\t\t\t\t\ttop: position,\n\t\t\t\t\t\t\t\tbehavior: "smooth"\n\t\t\t\t\t\t\t});\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}, 0.1);\n\t\t}\n\n\t\tfunction jumptoTime(timepoint, id) {\n\t\t\tvar player = document.getElementById("audio_player");\n\t\t\thistory.pushState(null, null, "#" + id);\n\t\t\tplayer.pause();\n\t\t\tplayer.currentTime = timepoint;\n\t\t\tplayer.play();\n\t\t}\n\t\t</script>\n\t</head>';
preS += '\n\n<body>\n\t<h2>' + audio_title + '</h2>\n\t<i>Click on a part of the transcription, to jump to its portion of audio, and get an anchor to it in the address\n\t\tbar<br><br></i>\n\t<div id="player-div">\n\t\t<div id="player">\n\t\t\t<audio controls="controls" id="audio_player">\n\t\t\t\t<source src="input.wav" />\n\t\t\t</audio>\n\t\t</div>\n\t\t<div><label for="autoscroll">auto-scroll: </label>\n\t\t\t<input type="checkbox" id="autoscroll" checked>\n\t\t</div>\n\t</div>\n';

postS = '\t</body>\n</html>'

def timeStr(t):
  return '{0:02d}:{1:02d}:{2:06.2f}'.format(round(t // 3600),
                                                round(t % 3600 // 60),
                                                t % 60)

html = list(preS)
txt = list("")
gidx = -1
for g in groups:
  shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
  shift = millisec(shift) - spacermilli #the start time in the original video
  shift=max(shift, 0)

  gidx += 1

  captions = json.load(open(str(gidx) + '.json'))['segments']

  if captions:
    speaker = g[0].split()[-1]
    boxclr = def_boxclr
    spkrclr = def_spkrclr
    if speaker in speakers:
      speaker, boxclr, spkrclr = speakers[speaker]

    html.append(f'<div class="e" style="background-color: {boxclr}">\n');
    html.append('<p  style="margin:0;padding: 5px 10px 10px 10px;word-wrap:normal;white-space:normal;">\n')
    html.append(f'<span style="color:{spkrclr};font-weight: bold;">{speaker}</span><br>\n\t\t\t\t')

    for c in captions:
      start = shift + c['start'] * 1000.0
      start = start / 1000.0   #time resolution ot youtube is Second.
      end = (shift + c['end'] * 1000.0) / 1000.0
      txt.append(f'[{timeStr(start)} --> {timeStr(end)}] [{speaker}] {c["text"]}\n')

      for i, w in enumerate(c['words']):
        if w == "":
           continue
        start = (shift + w['start']*1000.0) / 1000.0
        #end = (shift + w['end']) / 1000.0   #time resolution ot youtube is Second.
        html.append(f'<a href="#{timeStr(start)}" id="{"{:.1f}".format(round(start*5)/5)}" class="lt" onclick="jumptoTime({int(start)}, this.id)">{w["word"]}</a><!--\n\t\t\t\t-->')
    #html.append('\n')
    html.append('</p>\n')
    html.append(f'</div>\n')

html.append(postS)


with open(f"capspeaker.txt", "w", encoding='utf-8') as file:
  s = "".join(txt)
  file.write(s)
  print('captions saved to capspeaker.txt:')
  print(s+'\n')

with open(f"capspeaker.html", "w", encoding='utf-8') as file:    #TODO: proper html embed tag when video/audio from file
  s = "".join(html)
  file.write(s)
  print('captions saved to capspeaker.html:')
  print(s+'\n')

"""### Add a full transcript to the outputs, fully diarized in .txt format."""

# Function to convert time in HH:MM:SS.sss format to milliseconds
def millisec(time_str):
    h, m, s = map(float, time_str.split(':'))
    return int((h * 3600 + m * 60 + s) * 1000)

# Function to format time in HH:MM:SS.sss format
def timeStr(t):
    return '{0:02d}:{1:02d}:{2:06.2f}'.format(round(t // 3600),
                                               round(t % 3600 // 60),
                                               t % 60)

# Initialize variables
transcript = []
current_speaker = None
current_speaker_text = ""
gidx = -1

# Replace with your data or variables
#groups = [...]  # Replace with your groups data
#preS = [...]    # Replace with your preS data
#def_boxclr = '...'  # Replace with your default box color
#def_spkrclr = '...' # Replace with your default speaker color
#spacermilli = 0    # Replace with your spacermilli value
#speakers = {}       # Replace with your speaker data
#postS = [...]       # Replace with your postS data

for group in groups:
    shift = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=group[0])[0]
    shift = millisec(shift) - spacermilli  # Start time in the original video
    shift = max(shift, 0)

    gidx += 1
    captions = json.load(open(str(gidx) + '.json'))['segments']

    if captions:
        speaker = group[0].split()[-1]
        for caption in captions:
            start_time = shift + caption['start'] * 1000.0
            start_time = start_time / 1000.0  # Time resolution of YouTube is second
            end_time = (shift + caption['end'] * 1000.0) / 1000.0
            text = caption['text']

            if speaker != current_speaker:
                # New speaker, add their previous text to the transcript
                if current_speaker is not None:
                    transcript.append(f"{current_speaker}:\n{current_speaker_text}\n")
                    current_speaker_text = ""
                current_speaker = speaker

            current_speaker_text += f"{text} "

# Add the final speaker's text to the transcript
if current_speaker is not None:
    transcript.append(f"{current_speaker}:\n{current_speaker_text}\n")

# Combine the transcript lines into a single string
transcript_str = "\n".join(transcript)

# Save the transcript to a file
with open("transcript.txt", "w", encoding="utf-8") as file:
    file.write(transcript_str)

print("Transcript saved to transcript.txt")

"""[![notebook shield](https://img.shields.io/static/v1?label=&message=Notebook&color=blue&style=for-the-badge&logo=googlecolab&link=https://colab.research.google.com/github/ArthurFDLR/whisper-youtube/blob/main/whisper_youtube.ipynb)](https://colab.research.google.com/github/Majdoddin/nlp/blob/main/Pyannote_plays_and_Whisper_rhymes_v_2_0.ipynb)
[![repository shield](https://img.shields.io/static/v1?label=&message=Repository&color=blue&style=for-the-badge&logo=github&link=https://github.com/openai/whisper)](https://github.com/majdoddin/nlp)

# Whisper's transcription plus Pyannote's Diarization

**Update** - [@johnwyles](https://github.com/johnwyles) added HTML output for audio/video files from Google Drive, along with some fixes.

Using the new word-level timestamping of Whisper, the transcription words are highlighted as the video plays, with optional autoscroll. And the display on small displays is improved.

Moreover, the model is loaded just once, thus the whole thing runs much faster now. You can also hardcode your Huggingface token.

---
Andrej Karpathy [suggested](https://twitter.com/karpathy/status/1574476200801538048?s=20&t=s5IMMXOYjBI6-91dib6w8g) training a classifier on top of  OpenAI [Whisper](https://openai.com/blog/whisper/) model features to identify the speaker, so we can visualize the speaker in the transcript. But, as [pointed out](https://twitter.com/tarantulae/status/1574493613362388992?s=20&t=s5IMMXOYjBI6-91dib6w8g) by Christian Perone, it seems that features from whisper wouldn't be that great for speaker recognition as its main objective is basically to ignore speaker differences.

In the following, I use [**`pyannote-audio`**](https://github.com/pyannote/pyannote-audio), a speaker diarization toolkit by Hervé Bredin, to identify the speakers, and then match it with the transcriptions of Whispr, linked to the video. The input can be YouTube or an video/audio file (also on Google Drive). I try it on a [Customer Support Call](https://youtu.be/hpZFJctBUHQ). Check the result [**here**](https://majdoddin.github.io/dyson.html).

To make it easier to match the transcriptions to diarizations by speaker change, Sarah Kaiser [suggested](https://github.com/openai/whisper/discussions/264#discussioncomment-3825375) runnnig the pyannote.audio first and  then just running whisper on the split-by-speaker chunks.
For sake of performance (and transcription quality?), we attach the audio segments into a single audio file with a silent spacer as a separator, and run whisper on it. Enjoy it!

(For sake of performance , I also tried attaching the audio segments into a single audio file with a silent -or beep- spacer as a separator, and run whisper on it see it on [colab](https://colab.research.google.com/drive/1HuvcY4tkTHPDzcwyVH77LCh_m8tP-Qet?usp=sharing). It [works](https://majdoddin.github.io/lexicap.html) on some audio, and fails on some (Dyson's Interview). The problem is, whisper does not reliably make a timestap on a spacer. See the discussions [#139](https://github.com/openai/whisper/discussions/139) and [#29](https://github.com/openai/whisper/discussions/29))

The Markdown form used below is from [@ArthurFDLR](https://github.com/ArthurFDLR/whisper-youtube/).   
"""
