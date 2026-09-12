# Neural Network Next Lecture Notes

This continues from `Neural_Network_Architecture_Explanation.md`.

The first notes explained the base architecture:

```text
2 input features -> 64 hidden neurons -> 3 output class neurons
Dense -> ReLU -> Dense -> Softmax -> Cross-Entropy Loss
```

This lecture adds:

```text
Regularization -> Dropout -> Adam Optimization -> Training Loop -> Testing/Validation
```

## Updated Architecture

In `Final_Neural_Network_Regularization.ipynb`, the training dataset is:

```text
X, y = spiral_data(samples=1000, classes=3)
```

That means:

```text
1000 samples per class * 3 classes = 3000 total samples
X shape: (3000, 2)
y shape: (3000,)
```

The network flow is:

```text
Input X:        (3000, 2)
Dense 1 + L2:  (3000, 2)  @  W1 (2, 64)  + b1 (1, 64)  ->  (3000, 64)
ReLU:          (3000, 64)                                  ->  (3000, 64)
Dropout 0.1:   (3000, 64)  *  mask (3000, 64)              ->  (3000, 64)
Dense 2:       (3000, 64) @  W2 (64, 3)  + b2 (1, 3)      ->  (3000, 3)
Softmax:       (3000, 3)                                   ->  (3000, 3)
Crossentropy:  probabilities (3000, 3), y (3000,)          ->  data loss scalar
Regularization loss: Dense layer penalties                 ->  reg loss scalar
Total loss:     data_loss + regularization_loss             ->  scalar
```

## Updated Layer Table

| Part | Shape | Meaning |
|---|---:|---|
| `X` | `(3000, 2)` | 3000 spiral points, each point has `x1`, `x2` |
| `dense1.weights` | `(2, 64)` | 2 input weights for each hidden neuron |
| `dense1.biases` | `(1, 64)` | 1 bias for each hidden neuron |
| `dense1.output` | `(3000, 64)` | each sample becomes 64 hidden values |
| `activation1.output` | `(3000, 64)` | ReLU output, negative values become 0 |
| `dropout1.binary_mask` | `(3000, 64)` | random keep/drop mask for hidden activations |
| `dropout1.output` | `(3000, 64)` | ReLU output after dropout |
| `dense2.weights` | `(64, 3)` | 64 hidden values feeding 3 class neurons |
| `dense2.biases` | `(1, 3)` | 1 bias per class |
| `dense2.output` | `(3000, 3)` | logits, raw class scores |
| `loss_activation.output` | `(3000, 3)` | softmax probabilities |
| `data_loss` | scalar | average categorical cross-entropy |
| `regularization_loss` | scalar | L1/L2 penalty added to loss |
| `loss` | scalar | `data_loss + regularization_loss` |

Trainable parameters are unchanged from the base network:

```text
Dense 1: (2 * 64) + 64 = 192
Dense 2: (64 * 3) + 3 = 195
Total: 387 trainable parameters
```

Regularization, dropout, and Adam do not add trainable parameters. Adam adds optimizer state arrays, but those are not model parameters.

## Dense Layer With Regularization

The new `Layer_Dense` supports these regularization settings:

```text
weight_regularizer_l1
weight_regularizer_l2
bias_regularizer_l1
bias_regularizer_l2
```

In the notebook, Dense 1 uses L2 regularization:

```python
dense1 = Layer_Dense(
    2,
    64,
    weight_regularizer_l2=5e-4,
    bias_regularizer_l2=5e-4
)
```

Dense 2 does not use regularization:

```python
dense2 = Layer_Dense(64, 3)
```

So the regularization is mainly controlling the first hidden layer.

## Why Regularization Is Added

Without regularization, the model can make weights very large while trying to fit the training data. Large weights can make the model too sensitive to small input changes.

Regularization adds a penalty to the loss:

```text
total_loss = data_loss + regularization_loss
```

So the model is no longer only asking:

```text
How do I classify the training data correctly?
```

It is also asking:

```text
Can I classify the data while keeping weights reasonably small?
```

## L2 Regularization

L2 regularization penalizes squared parameter values.

For weights:

```text
L2 weight loss = lambda * sum(weights * weights)
```

For biases:

```text
L2 bias loss = lambda * sum(biases * biases)
```

In this notebook:

```text
lambda = 5e-4 = 0.0005
```

For Dense 1:

```text
regularization_loss =
    0.0005 * sum(W1 * W1)
  + 0.0005 * sum(b1 * b1)
```

The L2 gradient is added during `dense1.backward(...)`:

```text
dweights += 2 * lambda * weights
dbiases  += 2 * lambda * biases
```

This pushes weights and biases slightly toward 0 during training.

## L1 Regularization

The code also supports L1 regularization, even though the current model does not use it.

L1 regularization is:

```text
L1 weight loss = lambda * sum(abs(weights))
L1 bias loss   = lambda * sum(abs(biases))
```

Its gradient is based on the sign of each value:

```text
if weight > 0: gradient contribution is +lambda
if weight < 0: gradient contribution is -lambda
```

L1 tends to push some weights exactly toward 0, which can make a model more sparse. L2 tends to shrink weights smoothly.

## Dropout Layer

Dropout randomly turns off some neuron outputs during training.

The notebook creates:

```python
dropout1 = Layer_Dropout(0.1)
```

This means:

```text
dropout rate = 0.1
drop 10% of hidden activations
keep 90% of hidden activations
```

The dropout class stores:

```python
self.rate = 1 - rate
```

So for `Layer_Dropout(0.1)`:

```text
self.rate = 0.9
```

## Dropout Forward Pass

The dropout mask has the same shape as the hidden layer:

```text
activation1.output shape:      (3000, 64)
dropout1.binary_mask shape:    (3000, 64)
dropout1.output shape:         (3000, 64)
```

The mask is created with:

```python
self.binary_mask = np.random.binomial(1, self.rate, size=inputs.shape) / self.rate
```

For keep rate `0.9`, each mask value is usually one of:

```text
0              means neuron output is dropped
1 / 0.9 = 1.111... means neuron output is kept and scaled up
```

Example:

```text
ReLU output:       [2.0, 0.5, 0.0, 3.0]
dropout mask:      [1.111, 0.0, 1.111, 1.111]
dropout output:    [2.222, 0.0, 0.0, 3.333]
```

This is called inverted dropout. Scaling during training keeps the expected activation size roughly the same, so testing can use the normal network without dropout.

## Dropout Backward Pass

Backward pass uses the same mask:

```python
self.dinputs = dvalues * self.binary_mask
```

If a neuron was dropped during forward pass, its gradient is also dropped during backward pass.

Shape stays the same:

```text
dense2.dinputs:      (3000, 64)
dropout1.dinputs:    (3000, 64)
```

## Adam Optimizer

The notebook uses Adam:

```python
optimizer = Optimizer_Adam(learning_rate=0.05, decay=5e-5)
```

Adam improves on plain gradient descent by keeping two running values for every parameter:

```text
momentum: running average of gradients
cache:    running average of squared gradients
```

For every Dense layer, Adam creates:

```text
weight_momentums: same shape as weights
weight_cache:     same shape as weights
bias_momentums:   same shape as biases
bias_cache:       same shape as biases
```

For Dense 1:

```text
weight_momentums: (2, 64)
weight_cache:     (2, 64)
bias_momentums:   (1, 64)
bias_cache:       (1, 64)
```

For Dense 2:

```text
weight_momentums: (64, 3)
weight_cache:     (64, 3)
bias_momentums:   (1, 3)
bias_cache:       (1, 3)
```

These help Adam choose better update sizes for each individual weight and bias.

## Learning Rate Decay

The starting learning rate is:

```text
learning_rate = 0.05
```

The decay is:

```text
decay = 5e-5
```

Before each update, the current learning rate is:

```text
current_learning_rate = learning_rate * (1 / (1 + decay * iterations))
```

At iteration 0:

```text
current_learning_rate = 0.05
```

As training continues, the learning rate slowly becomes smaller.

This helps the model take larger steps early and smaller, more careful steps later.

## Adam Update Logic

For each layer, Adam does:

```text
momentum = beta_1 * old_momentum + (1 - beta_1) * gradient
cache    = beta_2 * old_cache    + (1 - beta_2) * gradient^2
```

The notebook defaults are:

```text
beta_1 = 0.9
beta_2 = 0.999
epsilon = 1e-7
```

Then Adam corrects early bias:

```text
momentum_corrected = momentum / (1 - beta_1 ^ (iterations + 1))
cache_corrected    = cache    / (1 - beta_2 ^ (iterations + 1))
```

Then parameters are updated:

```text
parameter += -current_learning_rate * momentum_corrected / (sqrt(cache_corrected) + epsilon)
```

In simple words:

```text
Momentum remembers gradient direction.
Cache controls step size.
Decay reduces learning rate over time.
```

## Training Forward Pass

Each epoch runs this forward flow:

```text
1. dense1.forward(X)
   (3000, 2) -> (3000, 64)

2. activation1.forward(dense1.output)
   (3000, 64) -> (3000, 64)

3. dropout1.forward(activation1.output)
   (3000, 64) -> (3000, 64)

4. dense2.forward(dropout1.output)
   (3000, 64) -> (3000, 3)

5. loss_activation.forward(dense2.output, y)
   logits (3000, 3) -> probabilities (3000, 3) -> data_loss scalar

6. regularization_loss =
      regularization_loss(dense1)
    + regularization_loss(dense2)

7. loss = data_loss + regularization_loss
```

Since Dense 2 has no regularizers, its regularization loss is 0.

## Accuracy During Training

Softmax returns probabilities:

```text
loss_activation.output shape: (3000, 3)
```

The prediction is the class with the largest probability:

```python
predictions = np.argmax(loss_activation.output, axis=1)
```

Example:

```text
probabilities: [0.10, 0.80, 0.10]
prediction:    class 1
```

Accuracy is:

```python
accuracy = np.mean(predictions == y)
```

So if 2100 out of 3000 predictions are correct:

```text
accuracy = 2100 / 3000 = 0.700
```

## Training Backward Pass

Backward pass flows in reverse:

```text
1. loss_activation.backward(loss_activation.output, y)
   probabilities (3000, 3) -> dinputs (3000, 3)

2. dense2.backward(loss_activation.dinputs)
   dvalues (3000, 3)
   dweights (64, 3)
   dbiases  (1, 3)
   dinputs  (3000, 64)

3. dropout1.backward(dense2.dinputs)
   dvalues (3000, 64) -> dinputs (3000, 64)

4. activation1.backward(dropout1.dinputs)
   dvalues (3000, 64) -> dinputs (3000, 64)

5. dense1.backward(activation1.dinputs)
   dvalues (3000, 64)
   dweights (2, 64)
   dbiases  (1, 64)
   dinputs  (3000, 2)
```

Dense 1 also adds L2 gradients:

```text
dense1.dweights += 2 * 0.0005 * dense1.weights
dense1.dbiases  += 2 * 0.0005 * dense1.biases
```

## Parameter Update

After backward pass, Adam updates both Dense layers:

```python
optimizer.pre_update_params()
optimizer.update_params(dense1)
optimizer.update_params(dense2)
optimizer.post_update_params()
```

Only Dense layers are updated because only Dense layers have trainable parameters.

ReLU has no weights.

Dropout has no weights.

Softmax and cross-entropy have no trainable weights.

## Training Log

The notebook prints every 100 epochs:

```text
epoch: 100,
acc: 0.569,
loss: 0.923 (data_loss: 0.899, reg_loss: 0.024),
lr: 0.04975371909050202
```

How to read it:

| Value | Meaning |
|---|---|
| `epoch` | current training step |
| `acc` | training accuracy |
| `loss` | total loss |
| `data_loss` | cross-entropy loss |
| `reg_loss` | regularization penalty |
| `lr` | current learning rate after decay |

Important point:

```text
loss = data_loss + reg_loss
```

So if:

```text
data_loss = 0.899
reg_loss = 0.024
```

Then:

```text
loss = 0.923
```

## Testing / Validation Pass

After training, the notebook creates a separate test dataset:

```python
X_test, y_test = spiral_data(samples=100, classes=3)
```

That means:

```text
X_test shape: (300, 2)
y_test shape: (300,)
```

Testing forward pass:

```text
1. dense1.forward(X_test)
   (300, 2) -> (300, 64)

2. activation1.forward(dense1.output)
   (300, 64) -> (300, 64)

3. dense2.forward(activation1.output)
   (300, 64) -> (300, 3)

4. loss_activation.forward(dense2.output, y_test)
   logits (300, 3) -> probabilities (300, 3) -> validation loss
```

Notice that dropout is skipped during testing:

```text
Training: Dense 1 -> ReLU -> Dropout -> Dense 2 -> Softmax
Testing:  Dense 1 -> ReLU -----------> Dense 2 -> Softmax
```

This is correct because dropout is only a training technique. During testing, the full network is used.

Also notice that the printed validation loss in the notebook is only the data loss from cross-entropy. The code does not add `regularization_loss` to the validation loss.

## Why Training And Testing Are Separate

Training accuracy answers:

```text
How well does the model fit the data it trained on?
```

Testing/validation accuracy answers:

```text
How well does the model perform on new data?
```

If training accuracy is high but test accuracy is low, the model is overfitting.

Regularization and dropout are used to reduce overfitting.

## Full One-Epoch Story

One training epoch looks like this:

```text
Input:
3000 points, each with 2 features.

Dense 1:
Each point is transformed into 64 hidden neuron values.

ReLU:
Negative hidden values are turned into 0.

Dropout:
Random hidden values are turned off during training.

Dense 2:
The remaining hidden values are converted into 3 class scores.

Softmax:
The 3 scores become probabilities.

Cross-entropy:
The model is penalized if the correct class probability is low.

Regularization:
The model is also penalized if weights/biases are too large.

Backward pass:
Gradients flow backward through softmax/loss, Dense 2, dropout, ReLU, and Dense 1.

Adam:
Weights and biases are updated using gradients, momentum, cache, and learning rate decay.
```

## Clean Summary

The regularized training architecture is:

```text
Input -> Dense 1 with L2 -> ReLU -> Dropout -> Dense 2 -> Softmax -> Cross-Entropy
```

The training objective is:

```text
Minimize total_loss = cross_entropy_loss + regularization_loss
```

The testing architecture is:

```text
Input -> Dense 1 -> ReLU -> Dense 2 -> Softmax -> Cross-Entropy
```

Dropout is used during training, skipped during testing, and Adam updates only the Dense layer weights and biases.
