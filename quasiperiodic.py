import requests
import numpy as np
import tensorflow as tf

from esn_cell import ESNCell


def run(data_str, tr_size=12000, washout_size=50, units=40, connectivity=0.2, scale=0.7, elements=16000):
  data = map(float, data_str.splitlines()[:elements])
  print data
  data_t = tf.reshape(tf.constant(data), [1, elements, 1])
  esn = ESNCell(units, connectivity, scale)

  print("Building graph...")
  outputs, final_state = tf.nn.dynamic_rnn(esn, data_t, dtype=tf.float32)
  washed = tf.squeeze(tf.slice(outputs, [0, washout_size, 0], [-1, -1, -1]))

  with tf.Session() as S:
    S.run(tf.global_variables_initializer())

    print("Computing embeddings...")
    res = S.run(washed)

    print("Computing direct solution...")
    state = np.array(res)
    tr_state = np.mat(state[:tr_size])
    ts_state = np.mat(state[tr_size:])
    wout = np.transpose(np.mat(data[washout_size+1:tr_size+washout_size+1]) * np.transpose(np.linalg.pinv(tr_state)))

    print("Testing performance...")
    ts_out = np.mat((np.transpose(ts_state * wout).tolist())[0][:-1])
    ts_y = np.mat(data[washout_size+tr_size+1:])
    print ts_y - ts_out

    ts_mse = np.mean(np.square(ts_y - ts_out))

  print("Test MSE: " + str(ts_mse))

if __name__ == "__main__":
  data_str = open("EXPTQP3.DAT", "r").read()
  run(data_str)