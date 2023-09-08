# Diarization-WhisperAI

# Instructions

You'll need to be signed in to a google account for this to work

## Accept terms and conditions for using Pyannote  <a id="terms_and_conditions"></a>

Pyannote is an AI tool which diarizes the audio and video streams whilst also segmenting the audio in to discrete chunks according to speaker. The code authors have made this software open source, but have some terms and conditions which you need to agree to in order to use the code. It will not be possible to use these scripts without following these processes, so please don't skip these actions

* Create an account at [https://huggingface.co/](https://huggingface.co/)
* Visit [hf.co/pyannote/speaker-diarization](https://hf.co/pyannote/speaker-diarization) and accept the terms and conditions for the diarization code
* Visit [hf.co/pyannote/segmentation](https://huggingface.co/pyannote/segmentation) and accept the terms and conditions for the segmentation code
* Visit [Hugging Face tokens page](https://huggingface.co/settings/tokens)
  * Click `New token`
  * Name the token something like 'pyannote_token_hf'
  * Change `Role` to write
  * Click `Generate a token`
  * Copy the text of your token
    * It will look something like this `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`
  * Keep this safe, you'll need it later 

## Add your audio/video files to google drive

Upload your files to google drive. We recommend you to make a folder with a name like `whisper`

## Open the code in Google Colab

[Click here](https://colab.research.google.com/github/chrissyhroberts/Diarization-WhisperAI/blob/main/Diarized_Whisper_AI.ipynb) to open the code in a Google Colab window. 

### Buy some computation units

Yes, this costs actual real-world money. You can in theory do this without paying, but you'll be limited to very short clips of audio. 
* Go to [this page](https://colab.research.google.com/signup/pricing) and buy some credits.
* Our experience is that you can get about 3 hours of transcript out of 100 compute units, so an estimated £3 per hour.

### Change the runtime to a GPU compute type
* Click `Runtime`
* Check that the runtime type is set to `python 3`
* Change the `Hardware accelerator` to one of the GPU options
 * If you're using the free Colab account, you are limited to using the T4 GPU and don't have much RAM. Not recommended.
 * If you're using computation units you've paid for, then you can use one of the better options `A100 GPU` or `V100 GPU`. We haven't tested which of the latter two is best.
 * Press `Save`
 * You should now be ready to go

## About the code `notebook`

The code is a python `notebook` format. It should looks like this

![](/img/notebook.png)

Note that you can expand or collapse sections of code using the arrow buttons. 
You run code either by pressing the play button (when multiple code chunks are collapsed in to a section, see the `Setup` chunk in the image above) or by hovering over and then clicking on the [ ] marks at the start of individual code chunks (see the grey box in the image above)

## Getting ready <a id="getting_ready"></a>

### Run the setup chunks
Run all the chunks of code in the setup section. This takes 4-5 minutes as the script prepares the system for the analysis by installing all of the software libraries and packages needed for the run. 

## Specify details of run  <a id="run_details"></a>

This section needs to be edited by you. On the right you can see text boxes where you enter information about the run. 
The notebook will automatically make the appropriate changes to the code based on what you enter here. 
When you have modified this section, collapse the `Specify details of run` section and run the code by pressing the play button

### video_path
Enter the full path to the source audio or video file

The google drive path must start `/content/drive/MyDrive/`
If your file is called `audio_001.mp3` and is in a folder on your google drive called whisper, then you'd use `/content/drive/MyDrive/whisper/audio_001.mp3` as the video_path variable.

### output_path
This is where you want to save all your outputs. The system creates a lot of files, so you don't want to just dump everything in to the whisper folder. 

The google drive path must start `/content/drive/MyDrive/`
A sensible approach would be to use a subfolder named after the input file. For instance, `/content/drive/MyDrive/whisper/audio_001`
If the subfolder doesn't exist, the system will automatically create it. 

![](/img/run_parameters.png)

### audio_title
This is simply the name of the document. This will be shown at the top of the html output.
You could use a descriptive title, such as `Audio_001 : Interview with Dr Ranj from Ugandan MoH 2023-08-01`

### access_token
Paste your huggingface access token here. See [here](#terms_and_conditions)

### language
Whisper can transcribe and translate (only to English) a large number of languages. Select the language of your audio/video file here. 

### whisper_task
This should be set to either transcribe or translate the audio stream. 

### model_size
For English audio, you can usually get away with using the `small` model. For other languages, you should usually opt for the `large` model

## Specify speakers  <a id="speakers"></a>
This section is modifiable, but usually you should leave it alone. 
You can name speakers directly, and change the colours used in the html output. 

## Prepare data and folders  <a id="prep_data_and_folders"></a>
This section creates all the necessary folders and files to do the run
This code should be left alone. Collapse it and run it by pressing play.

## Diarization using Pyannote  <a id="diarization"></a>
This section diarizes the audio stream, figuring out how many speakers there are, and when they are speaking
This code should be left alone. Collapse it and run it by pressing play.

## Prepare data and folders  <a id="prep_data_and_folders"></a>
This section should be left alone. Collapse it and run it by pressing play.

# Outputs
The scripts will put all of the outputs on to your Google Drive in a subfolder named according to how you defined the `output_path` variable.

The most important files you will get are 

00_[filename]_transcript.txt
00_[filename]_transcript.html


