import re
import unicodedata
from argparse import ArgumentParser
from pathlib import Path
import soundfile as sf
from .hifigan.config import FLAGS as FLAGSHIFIGAN

from .nat.config import FLAGS as FLAGSNAT

from .hifigan.mel2wave import mel2wave
print("!!!!!!!!!!!!!!!!!!!!!!!!")

from .nat.config import FLAGS
print("!!!!!!!!!!!!!!!!!!!!!!!!")

from .nat.text2mel import text2mel
print("!!!!!!!!!!!!!!!!!!!!!!!!")
parser = ArgumentParser()
parser.add_argument('--text', type=str)
parser.add_argument('--output', default='clip.wav', type=Path)
parser.add_argument('--sample-rate', default=16000, type=int)
parser.add_argument('--silence-duration', default=-1, type=float)
# parser.add_argument('--lexicon-file', default=None)
parser.add_argument('--voice-id', default=1, type=int)
args = parser.parse_args()


def nat_normalize_text(text):
  print("no bug")
  text = unicodedata.normalize('NFKC', text)
  text = text.lower().strip()
  sp = FLAGS.special_phonemes[FLAGS.sp_index]
  text = re.sub(r'[\n.,:]+', f' {sp} ', text)
  text = text.replace('"', " ")
  text = re.sub(r'\s+', ' ', text)
  text = re.sub(r'[.,:;?!]+', f' {sp} ', text)
  text = re.sub('[ ]+', ' ', text)
  text = re.sub(f'( {sp}+)+ ', f' {sp} ', text)
  return text.strip()

def chosen_voice(id_voice:int)->Path:
  print("choose--------")
  model_path={
    '1': FLAGSNAT.ckpt_dir_thao,
    '2': FLAGSNAT.ckpt_dir_kien,
    '3': FLAGSNAT.ckpt_dir_ltrang,
    '4': FLAGSNAT.ckpt_dir_panh,
  }
  return model_path.get(str(id_voice))
      
#take voice
voice_dir = args.voice_id
voice_dir = chosen_voice(int(voice_dir))
lexicon_file = voice_dir / 'lexicon.txt'
print(lexicon_file)

text = nat_normalize_text(args.text)
print('Normalized text input:', text)
mel = text2mel(text, lexicon_file , args.silence_duration, voice_dir)

wave = mel2wave(mel, voice_dir)
print('writing output to file', args.output)
sf.write(str(args.output), wave, samplerate=args.sample_rate)
