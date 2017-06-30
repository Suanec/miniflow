# Copyright 2017 The Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import client
import ops

# Compatible for TensorFlow APIs
placeholder = ops.PlaceholderOp
constant = ops.ConstantOp
add = ops.AddOp
float32 = float
float64 = float
Session = client.Session


def main():
  # y = 3 * x**3 + 2 * x**2 + x + 10
  # y' = 9 * x**2 + 4 * x + 1
  print("Formula: {}".format("y = 3 * x**3 + 2 * x**2 + x + 10"))
  print("Formula gradient: {}".format("y' = 9 * x**2 + 4 * x + 1"))

  x = 1
  first_item = ops.MultipleOp(3, ops.CubicOp(x))
  second_item = ops.MultipleOp(2, ops.SquareOp(x))
  third_item = ops.VariableOp(x)
  forth_item = ops.ConstantOp(10)
  y = ops.AddNOp(ops.AddOp(first_item, second_item), third_item, forth_item)

  # Should be "X: 1, forward: 16.0, grad: 14.0"
  print("X: {}, forward: {}, grad: {}".format(x, y.forward(), y.grad()))

  # Build the graph
  name_op_map = {}
  coefficient1 = ops.ConstantOp(3)
  cubic1 = ops.CubicOp(x)
  coefficient2 = ops.ConstantOp(2)
  square1 = ops.SquareOp(x)
  multiple1 = ops.MultipleOp(coefficient1, cubic1)
  multiple2 = ops.MultipleOp(coefficient2, square1)
  variable1 = ops.VariableOp(x)
  constant1 = ops.ConstantOp(10)
  add1 = ops.AddNOp(multiple1, multiple2, variable1, constant1)
  add2 = ops.AddNOp(multiple1, multiple2)

  name_op_map["coefficient1"] = coefficient1
  name_op_map["cubic1"] = cubic1
  name_op_map["coefficient2"] = coefficient2
  name_op_map["square1"] = square1
  name_op_map["multiple1"] = multiple1
  name_op_map["multiple2"] = multiple2
  name_op_map["variable1"] = variable1
  name_op_map["constant1"] = constant1
  name_op_map["add1"] = add1
  name_op_map["add2"] = add2

  print("add1 forward: {}, backward: {}".format(name_op_map["add1"].forward(),
                                                name_op_map["add1"].grad()))
  print("add2 forward: {}, backward: {}".format(name_op_map["add2"].forward(),
                                                name_op_map["add2"].grad()))

  # Automatically update weights with gradient
  learning_rate = 0.01
  epoch_number = 10
  label = 10
  weights_value = 3

  # y = weights * x**3 + 2 * x**2 + x + 10
  x = ops.PlaceholderOp()
  weights = ops.VariableOp(weights_value)
  cubic1 = ops.CubicOp(x)
  coefficient2 = ops.ConstantOp(2)
  square1 = ops.SquareOp(x)
  multiple1 = ops.MultipleOp(weights, cubic1)
  multiple2 = ops.MultipleOp(coefficient2, square1)
  constant1 = ops.ConstantOp(10)
  add1 = ops.AddNOp(multiple1, multiple2, x, constant1)

  for epoch_index in range(epoch_number):

    x.set_value(1)
    #import ipdb;ipdb.set_trace()

    grad = add1.grad()
    weights_value -= learning_rate * grad
    weights.set_value(weights_value)

    predict = add1.forward()
    loss = predict - label
    print("Epoch: {}, loss: {}, grad: {}, weights: {}, predict: {}".format(
        epoch_index, loss, grad, weights_value, predict))

  # Run with session
  ''' TensorFlow example
  hello = tf.constant('Hello, TensorFlow!')
  sess = tf.Session()
  print(sess.run(hello))
  a = tf.constant(10)
  b = tf.constant(32)
  c = tf.add(a, b)
  print(sess.run(c))
  '''

  hello = ops.ConstantOp("Hello, TensorFlow! -- by MinialFlow")
  sess = client.Session()
  print(sess.run(hello))
  a = ops.ConstantOp(10)
  b = ops.ConstantOp(32)
  c = ops.AddOp(a, b)
  print(sess.run(c))

  # Run with session and feed_dict
  '''
  
  a = tf.placeholder(tf.float32)
  b = tf.constant(32.0)
  c = tf.add(a, b)
  sess = tf.Session()
  print(sess.run(c, feed_dict={a: 10}))
  print(sess.run(c, feed_dict={a.name: 10}))
  '''

  a = ops.PlaceholderOp()
  b = ops.ConstantOp(32)
  c = ops.AddOp(a, b)
  sess = Session()
  print(sess.run(c, feed_dict={a: 10}))
  print(sess.run(c, feed_dict={a.name: 10}))


if __name__ == "__main__":
  main()
