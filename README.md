# Diarization-WhisperAI

# Instructions

## Accept terms and conditions for using Pyannote

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

## Open the code in Google Colab

You'll need to be signed in to a google account for this to work

[Click here](https://colab.research.google.com/github/chrissyhroberts/Diarization-WhisperAI/blob/main/Diarized_Whisper_AI.ipynb) to open the code in a Google Colab window. 

* Click `Runtime`
* Check that the runtime type is set to `python 3`
* Change the `Hardware accelerator` to one of the GPU options
 * If you're using the free Colab account, you are limited to using the T4 GPU.
 * If you're using the pro account (paid for) then you can use one of the better options `A100 GPU` or `V100 GPU`. We haven't tested which of the latter two is best.
 * Save 




