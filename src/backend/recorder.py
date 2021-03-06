import os
import shutil
import time

import speech_recognition as sr

import src.other.constants as const
import src.other.garcon as gc

MAX_REC_LENGTH = const.MAX_REC_LENGTH

DEF_TXT_PROMPT = ''

DEF_POST_PROMPT = 'Done recording'

DEF_PRE_PROMPT = 'Say something...'

DEF_COUNT_DOWN = 3

RECORDING_DIR = os.path.join('..', '..', 'recordings')
EMOTIONS_DIR = os.path.join('..', '..', 'data', 'emotions2')
WAVE_FN_EXT = '.wav'

class Recorder():

	@staticmethod
	def check_is_dir(dir_path):
		print(os.path.isdir(dir_path))

	def __init__(self):
		self._r = None
		self._record_idx = 0
		self._init_emotion_dirs()
		gc.enter_func()
		self._r = sr.Recognizer()

	def _init_emotion_dirs(self):
		self._emotion_dirs = {}
		self._emotion_dirs[0] = os.path.join(EMOTIONS_DIR, '0_happy')
		self._emotion_dirs[1] = os.path.join(EMOTIONS_DIR, '2_sad')
		self._emotion_dirs[2] = os.path.join(EMOTIONS_DIR, '3_angry')

	def record(self, pre_prompt=DEF_PRE_PROMPT, post_prompt=DEF_POST_PROMPT,
			   shell_verbose=True):
		gc.enter_func()
		fn = self._get_fn()
		audio_source = self._record_mic(pre_prompt, post_prompt, shell_verbose)
		self._save_wav(audio_source, fn)
		time.sleep(1)
		return fn

	def labelize_rec(self, rec_fn, label):
		dest_base = os.path.basename(rec_fn)
		splitted = os.path.splitext(dest_base)
		label_txt = '_' + const.LABEL_DIR_DICT[label]
		dest_base = splitted[0] + label_txt + splitted[1]
		dest = os.path.join(self._emotion_dirs[label], 'mine', dest_base)
		shutil.move(rec_fn, dest)

	def _get_fn(self):
		dtime = time.localtime()
		base = ['rec']
		for i in range(1, 6):
			base.append(str(dtime[i]))
		base = '_'.join(base)
		fn = os.path.join(RECORDING_DIR, base + WAVE_FN_EXT)
		return os.path.abspath(fn)

	def _record_mic(self, pre_prompt, post_prompt, shell_verbose):
		'''
		Records mic and returns an audio
		file of that recording.
		:returns: AudioFile recorded
		'''
		pre_prompt = pre_prompt if pre_prompt else DEF_PRE_PROMPT
		post_prompt = post_prompt if post_prompt else DEF_POST_PROMPT
		with sr.Microphone() as source:
			if shell_verbose:
				print()
				time.sleep(2)
				print(pre_prompt)
				time.sleep(1)
				self._countdown()
			# audio_source = self._r.listen(source, timeout=1,
			# 							  phrase_time_limit=MAX_REC_LENGTH)
			audio_source = self._r.listen(source,
										  phrase_time_limit=MAX_REC_LENGTH)
			if shell_verbose:
				print(post_prompt)
		return audio_source

	def _countdown(self, count_down=DEF_COUNT_DOWN):
		'''
		Counts down from the given count_down value.
		'''
		for i in range(count_down, 0, -1):
			print(i)
			time.sleep(1)
		print('GO')

	def _save_wav(self, audio_source, fn):
		'''
		Saves an audio source as a .wav file.
		:param audio_source:	type=AudioSource
		:param record_name: 	name of recording
		'''
		wav_data = audio_source.get_wav_data()
		wf_name = os.path.join(fn)
		with open(wf_name, 'wb') as wf:
			wf.write(wav_data)
