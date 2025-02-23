import tensorflow as tf
import tensorflow.contrib.slim as slim



class Qnetwork():
	def __init__(self, h_size, n_actions):
		self.scalarInput = tf.placeholder(shape=[None, 84 * 84 * 4], dtype=tf.float32)
		self.imageIn = tf.reshape(self.scalarInput, shape=[-1, 84, 84, 4])

		self.conv1 = slim.conv2d(inputs=self.imageIn, num_outputs=32, kernel_size=[8,8], stride=[4,4], padding='VALID', biases_initializer=None, activation_fn=tf.nn.relu)
		self.conv2 = slim.conv2d(inputs=self.conv1, num_outputs=64, kernel_size=[4,4], stride=[2,2], padding='VALID', biases_initializer=None, activation_fn=tf.nn.relu)
		self.conv3 = slim.conv2d(inputs=self.conv2, num_outputs=64, kernel_size=[3,3], stride=[1,1], padding='VALID', biases_initializer=None, activation_fn=tf.nn.relu)
		self.conv4 = slim.conv2d(inputs=self.conv3, num_outputs=h_size, kernel_size=[7,7], stride=[1,1], padding='VALID', biases_initializer=None, activation_fn=tf.nn.relu)
		
		self.streamAC, self.streamVC = tf.split(self.conv4, 2, 3)
		self.streamA = slim.flatten(self.streamAC)
		self.streamV = slim.flatten(self.streamVC)
		xavier_init = tf.contrib.layers.xavier_initializer()
		self.AW = tf.Variable(xavier_init([h_size//2, n_actions]))
		self.VW = tf.Variable(xavier_init([h_size//2, 1]))
		self.Advantage = tf.matmul(self.streamA, self.AW)
		self.Value = tf.matmul(self.streamV, self.VW)

		self.Qout = self.Value + tf.subtract(self.Advantage, tf.reduce_mean(self.Advantage, axis=1, keep_dims=True))
		self.predict = tf.argmax(self.Qout, 1)

		self.targetQ = tf.placeholder(shape=[None], dtype=tf.float32)
		self.actions = tf.placeholder(shape=[None], dtype=tf.int32)
		self.actions_onehot = tf.one_hot(self.actions, n_actions, dtype=tf.float32)

		self.Q = tf.reduce_sum(tf.multiply(self.Qout, self.actions_onehot), axis=1)

		self.td_error = tf.square(self.targetQ - self.Q)
		self.loss = tf.reduce_mean(self.td_error)
		self.trainer = tf.train.AdamOptimizer(learning_rate=0.00025)
		self.updateModel = self.trainer.minimize(self.loss)

	