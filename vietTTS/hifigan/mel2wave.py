import json
import os
import pickle

import haiku as hk
import jax
import jax.numpy as jnp
import numpy as np

from .config import FLAGS
from .model import Generator


class AttrDict(dict):
  def __init__(self, *args, **kwargs):
    super(AttrDict, self).__init__(*args, **kwargs)
    self.__dict__ = self


def mel2wave(mel, ckpt_dir):
  config_file = 'assets/hifigan/config.json'
  MAX_WAV_VALUE = 32768.0
  with open(config_file) as f:
    data = f.read()
  json_config = json.loads(data)
  h = AttrDict(json_config)

  @hk.transform_with_state
  def forward(x):
    net = Generator(h)
    return net(x)

  rng = next(hk.PRNGSequence(42))

  with open(ckpt_dir / 'hk_hifi.pickle', 'rb') as f:
    print("hifigan checkpoint path: ", str(ckpt_dir))
    print("===========================================================")
    params = pickle.load(f)
  aux = {}
  wav, aux = forward.apply(params, aux, rng, mel)
  wav = jnp.squeeze(wav)
  audio = jax.device_get(wav)
  return audio
