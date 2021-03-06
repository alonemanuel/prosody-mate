import tkinter as tk
from winsound import *

import src.other.constants as const
import src.other.garcon as gc

class DeployPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self._controller = controller
		self._init_title()
		self._init_labels()
		self._init_widgets()

	def _init_widgets(self):
		self._init_learning_buttons()
		self._init_navigation_buttons()
		self._init_predict_button()
		self._init_debugging_buttons()
		self._init_sample_buttons()

	def _init_sample_buttons(self):
		self._label_buttons = tk.Frame(self)
		self._label_buttons.pack()

		for label, name in self._label_code_names.items():
			print(label, name)
			button = tk.Button(self._label_buttons, text=name,
							   command=lambda label=label:
							   self._assign_label(label))
			button.pack(side='left', padx=10)
		self._disable_labels()

	def _init_labels(self):
		self._label_code_names = {0: 'Happy', 1: 'Sad', 2: 'Angry'}
		self._labels_name_code = {'Happy': 0, 'Sad': 1, 'Angry': 2}

	def _disable_labels(self):
		for child in self._label_buttons.winfo_children():
			child.config(state=tk.DISABLED)

	def _enable_labels(self):
		for child in self._label_buttons.winfo_children():
			child.config(state=tk.NORMAL)

	def _assign_label(self, label):
		'''
		Assigns a label = moved recording to appropriate dir.
		'''
		print(f'label: {label}')
		self._controller.recorder.labelize_rec(self._last_record_fn,
											   label)
		self._disable_labels()

	def _init_predict_button(self):
		gc.enter_func()
		self._predict_button = tk.Button(self, text="Predict",
										 command=self._predict)
		self._prediction_lbl = tk.Label(self)
		self._prediction_lbl.pack()
		self._predict_button.pack()

	def _predict(self):
		gc.enter_func()
		gc.log(f'predicting {self._last_record_fn}')
		prediction = self._controller.logic.predict(self._last_record_fn)
		prediction_str = const.LABEL_DIR_DICT[prediction[0]]
		gc.log(f'prediction: {prediction}')
		self._prediction_lbl.config(text=prediction_str)

	def _init_learning_buttons(self):
		gc.enter_func()
		self._learning_frame = tk.Frame(self)
		self._learning_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
		self._learn_button = tk.Button(self._learning_frame, text='Learn',
									   command=self._controller.logic.learn)
		self._test_button = tk.Button(self._learning_frame, text='Test',
									  command=self._controller.logic.test)
		self._learn_button.pack(side=tk.LEFT, pady=10, padx=10)
		self._test_button.pack(side=tk.LEFT, pady=10, padx=10)

	def _init_debugging_buttons(self):
		gc.enter_func()
		self._record_btn = tk.Button(self, text='Record something',
									 command=self._record)
		self._record_btn.pack()
		self._init_play_button()

	def _record(self):
		self._last_record_fn = self._controller.recorder.record(
				shell_verbose=False)
		self._play_button.config(state=tk.NORMAL)
		self._enable_labels()

	def _init_play_button(self):
		play = lambda: PlaySound(self._last_record_fn, flags=SND_FILENAME)
		self._play_button = tk.Button(self, text='Play last recording',
									  command=play)
		self._play_button.config(state=tk.DISABLED)
		self._play_button.pack(pady=10)

	def _init_title(self):
		label = tk.Label(self, text='This is Deploy page',
						 font=self._controller.title_font)
		label.pack(side="top", fill="x", pady=10)

	def _init_navigation_buttons(self):
		button = tk.Button(self, text="Go to the Menu page",
						   command=lambda: self._controller._show_frame(
								   const.MENU_PAGE))
		button.pack(side='bottom', pady=10)
