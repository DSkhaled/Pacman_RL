import numpy as np
import random

class experience_buffer():
	def __init__(self, buffer_size=50000):
		self.buffer = []
		self.buffer_size = buffer_size

	def add(self, experience):
		if len(self.buffer) + len(experience) >= self.buffer_size:
			self.buffer[0:(len(experience) + len(self.buffer)) - self.buffer_size] = []
		self.buffer.extend(experience)

	def sample(self, size):
		return np.reshape(np.array(random.sample(self.buffer, size)), [size, 5])