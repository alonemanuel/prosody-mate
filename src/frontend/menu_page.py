import tkinter as tk

class MenuPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self._init_header()

	def _init_header(self):
		self._header = tk.Frame(self)
		self._header.pack(side='top', anchor='w')
		label = tk.Label(self._header, text="emotio.",
						 font=self.controller.title_font)
		label.pack(side="top", fill="x", padx=10, pady=10)

	# self.configure(background='white')

	def init_navigation(self):
		self._nav_buttons = tk.Frame(self)
		self._nav_buttons.pack(side='bottom')
		for page_name in self.controller._frames.keys():
			if page_name == MenuPage.__name__:
				continue
			button = tk.Button(self._nav_buttons, text=f'Enter {page_name}',
							   command=lambda name=page_name:
							   self.controller._show_frame(
									   name))
			button.pack(side='left', padx=10, pady=50)
