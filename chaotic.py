import requests
import numpy as np
import tensorflow as tf

from esn_cell import ESNCell


def run(data_str, file, average, tr_size=12000, washout_size=50, units=40, connectivity=0.2, scale=0.7, elements=12081):
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

    ts_mse = np.mean(np.square(ts_y - ts_out))
    print ts_out.shape
    print np.squeeze(ts_out)
    print np.squeeze(ts_out).shape
    for i in ts_out:
      print i
    print data[washout_size + tr_size + 1]
  if (average):
    print("Test MSE: " + str(ts_mse))
    file.write(str(ts_mse)+"\n")
  else:
    get_last = str(ts_out).split(" ")
    get_last_true = str(ts_y).split(" ")
    print get_last_true
    print get_last
    use_found = 0
    if "]]" in str(get_last[-1]):
      use_found = get_last[-1][0:-2]
    else:
      use_found = get_last[-2]
    print use_found
    print get_last_true[-1][0:-2]
    file.write(str(use_found) + ":" + str(get_last_true[-1][0:-2]) + "\n")

def run_x(data_str, x, average):
  file = open("results"+str(x)+"chaotic.txt", "a")
  run(data_str, file, average, tr_size=12000, washout_size=50, units=40, connectivity=0.2, scale=0.7, elements=12051 + x)
if __name__ == "__main__":
  data_str = open("HENON.DAT", "r").read()
  run_x(data_str, 100, True)
