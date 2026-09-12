# Neural Network Architecture Explanation

In `Neural_Network_Full_Code.ipynb`, the neural net architecture is:

```text
Input X:        (300, 2)
Dense 1:       (300, 2)  @  W1 (2, 64)  + b1 (1, 64)  ->  (300, 64)
ReLU:          (300, 64)                                 ->  (300, 64)
Dense 2:       (300, 64) @  W2 (64, 3)  + b2 (1, 3)   ->  (300, 3)
Softmax:       (300, 3)                                  ->  (300, 3)
Crossentropy:  probabilities (300, 3), y (300,)          ->  scalar loss
```

## Architecture

| Part | Shape | Meaning |
|---|---:|---|
| `X` | `(300, 2)` | 300 spiral points, each point has 2 features: `x1`, `x2` |
| `dense1.weights` | `(2, 64)` | 2 input weights for each of 64 hidden neurons |
| `dense1.biases` | `(1, 64)` | 1 bias for each hidden neuron |
| `dense1.output` | `(300, 64)` | each sample becomes 64 hidden values |
| `ReLU output` | `(300, 64)` | same shape, negative values become 0 |
| `dense2.weights` | `(64, 3)` | 64 hidden inputs feeding 3 output neurons/classes |
| `dense2.biases` | `(1, 3)` | 1 bias per class |
| `dense2.output` | `(300, 3)` | raw class scores/logits |
| `softmax output` | `(300, 3)` | probabilities for classes 0, 1, 2 |
| `loss` | scalar | average categorical cross-entropy over 300 samples |

Trainable parameters:

```text
Dense 1: (2 * 64) + 64 = 192
Dense 2: (64 * 3) + 3 = 195
Total: 387 trainable parameters
```

## Dense Layer

A dense layer means every input connects to every neuron.

For one sample:

```text
sample = [x1, x2]
```

One hidden neuron does:

```text
z = x1*w1 + x2*w2 + b
```

Since Dense 1 has 64 neurons, it does this 64 times:

```text
[x1, x2] -> [z1, z2, z3, ..., z64]
```

For the full batch:

```text
X (300, 2) @ W1 (2, 64) + b1 (1, 64) = output (300, 64)
```

## ReLU

ReLU is:

```text
ReLU(x) = max(0, x)
```

Example:

```text
Dense output: [-1.2, 0.5, 3.0, -0.7]
ReLU output:  [ 0.0, 0.5, 3.0,  0.0]
```

It keeps positive neuron signals and turns negative signals off. Shape does not change:

```text
(300, 64) -> (300, 64)
```

## Output Dense Layer

Dense 2 maps the 64 hidden features into 3 class scores.

For one output neuron/class:

```text
class_0_score = h1*w1 + h2*w2 + ... + h64*w64 + b
```

Because there are 3 classes:

```text
hidden values (64) -> [score_class_0, score_class_1, score_class_2]
```

For the full batch:

```text
(300, 64) @ (64, 3) + (1, 3) = (300, 3)
```

These 3 values are called logits, not probabilities yet.

## Softmax

Softmax turns the 3 logits into probabilities that sum to 1.

Example:

```text
logits:      [2.0, 1.0, 0.1]
softmax:     [0.659, 0.242, 0.099]
prediction:  class 0
```

For the full network:

```text
logits (300, 3) -> probabilities (300, 3)
```

Each row is one sample:

```text
sample 1 -> [P(class 0), P(class 1), P(class 2)]
```

## Categorical Cross-Entropy

Cross-entropy checks how much probability the model gave to the correct class.

Example:

```text
prediction = [0.7, 0.2, 0.1]
true class = 0
loss = -log(0.7) = 0.357
```

Better confidence gives smaller loss:

```text
-log(0.9) = 0.105   good
-log(0.3) = 1.204   bad
-log(0.01) = 4.605  very bad
```

So the model is rewarded when the correct class probability is high.

## One-Sample Story

For one spiral point:

```text
Input:
[x1, x2]

Dense 1:
64 neurons each calculate a weighted sum.

ReLU:
negative hidden values become 0.

Dense 2:
3 neurons calculate class scores.

Softmax:
scores become probabilities, like [0.1, 0.8, 0.1].

Crossentropy:
if true class is 1, loss = -log(0.8).
```

The clean explanation is:

```text
2 input features -> 64 hidden neurons -> 3 output class neurons
Dense -> ReLU -> Dense -> Softmax -> Cross-Entropy Loss
```


For backward :

- Minimize the loss function.
- how to update the weights w[0], w[1], w[2], b such that loss is minimized.
- For this we have to move in negative gradient direction.
- dl/dw0, dl/dw1, dl/dw2, dl/db
- for one epoch to update w0 = wo - n*dl/dw0

Loss function for one single neuron:



- Loss = (Relu(sum(mul(xo,wo), mul(x1,w1), mul(x2,w2), b)))^2
- dloss/dw0 = dloss/dRelu * dRelu/dsum * dsum/dmul(x0, w0) * dmul(x0,w0)/dw0