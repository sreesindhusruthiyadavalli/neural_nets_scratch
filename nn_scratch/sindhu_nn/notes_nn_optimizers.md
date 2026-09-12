# Neural Network Optimizers Notes

Source reference: https://nnfs.io/pog/

The NNFS page shows a learning rate that is too small. Even after many optimization steps, the model moves only a little. This is useful for explaining why the learning rate matters so much.

## What Is An Optimizer?

An optimizer decides how to update the weights and biases after backpropagation calculates gradients.

Basic update:

```python
parameter -= learning_rate * gradient
```

The gradient tells us the direction in which loss increases fastest. To reduce loss, we move in the opposite direction.

The optimizer controls how that movement happens.

## Learning Rate

The learning rate is the step size.

If the learning rate is too small:

- The model moves in the correct direction.
- Each update is tiny.
- Training becomes very slow.
- Loss may decrease, but only after many steps.

If the learning rate is too large:

- The model may jump over the minimum.
- Loss may bounce around.
- Training becomes unstable.

If the learning rate is way too large:

- Updates can explode.
- Loss may increase instead of decrease.
- The model may fail to train.

Good explanation:

> The learning rate decides how big a step we take while moving downhill. Too small means slow learning. Too big means unstable learning.

## Good Learning Rate

A good learning rate is large enough to make progress, but small enough to avoid overshooting the minimum.

Good explanation:

> We want steps that are confident at the beginning, but controlled near the end.

## Learning Rate Decay

Learning rate decay means reducing the learning rate over time.

At the beginning of training:

- The model is far from the best solution.
- Bigger steps are useful.
- We want faster movement.

Later in training:

- The model is closer to a good solution.
- Smaller steps are safer.
- We want fine-tuning.

Good explanation:

> Learning rate decay lets the model start with bigger steps and finish with smaller, more careful steps.

## SGD Optimizer

SGD stands for Stochastic Gradient Descent.

Basic SGD update:

```python
weights -= learning_rate * dweights
biases -= learning_rate * dbiases
```

SGD uses the current gradient to update the parameters.

Good explanation:

> SGD looks at the slope right now and takes a step downhill.

Limitations of SGD:

- It can move slowly.
- It can zig-zag.
- It can struggle in flat or curved regions.
- It depends heavily on choosing a good learning rate.

## SGD With Momentum

Momentum adds memory to SGD.

Instead of only using the current gradient, it also remembers the previous direction of movement.

Basic idea:

```python
velocity = momentum * velocity - learning_rate * gradient
parameter += velocity
```

Momentum helps when gradients keep pointing in a similar direction.

Good explanation:

> SGD is like walking downhill step by step. Momentum is like rolling a ball downhill.

Why momentum helps:

- It speeds up movement in consistent directions.
- It reduces zig-zag movement.
- It smooths noisy updates.
- It can move through small flat regions better than plain SGD.

## AdaGrad

AdaGrad adapts the learning rate separately for each parameter.

Basic idea:

```python
cache += gradient ** 2
parameter -= learning_rate * gradient / (sqrt(cache) + epsilon)
```

Parameters with large historical gradients get smaller updates. Parameters with small or rare gradients can still get larger updates.

Good explanation:

> AdaGrad gives each parameter its own learning rate based on how much it has already changed.

Main benefit:

- Useful when some parameters need frequent updates and others need rare updates.

Main problem:

- The cache keeps growing.
- The effective learning rate can become very small.
- Training may slow down too much.

Good explanation:

> AdaGrad remembers everything, so over time it may become too cautious.

## RMSProp

RMSProp improves on AdaGrad by using a moving average instead of storing the full history.

Basic idea:

```python
cache = rho * cache + (1 - rho) * gradient ** 2
parameter -= learning_rate * gradient / (sqrt(cache) + epsilon)
```

RMSProp looks more at recent gradients than very old gradients.

Good explanation:

> AdaGrad remembers everything. RMSProp mostly remembers the recent past.

Why RMSProp helps:

- It keeps adaptive learning rates.
- It avoids shrinking the learning rate forever.
- It works better for long training runs.

## Adam Optimizer

Adam combines ideas from momentum and RMSProp.

Adam tracks two things:

- A moving average of gradients.
- A moving average of squared gradients.

Simple idea:

```python
m = beta1 * m + (1 - beta1) * gradient
v = beta2 * v + (1 - beta2) * gradient ** 2
parameter -= learning_rate * m / (sqrt(v) + epsilon)
```

The first moving average gives direction memory, like momentum.

The second moving average adjusts the step size, like RMSProp.

Good explanation:

> Adam is momentum plus adaptive learning rates.

Why Adam is popular:

- It usually trains quickly.
- It handles noisy gradients well.
- It needs less manual tuning than plain SGD.
- It adapts updates separately for each parameter.

## Teaching Order

Use this order when explaining optimizers:

1. Start with gradient descent.
2. Explain that gradients tell us which direction increases loss.
3. Explain that we move opposite the gradient to reduce loss.
4. Introduce learning rate as step size.
5. Show what happens when learning rate is too small.
6. Show what happens when learning rate is too large.
7. Explain learning rate decay.
8. Explain SGD as the simplest optimizer.
9. Add momentum as direction memory.
10. Explain AdaGrad as per-parameter learning rates.
11. Explain RMSProp as AdaGrad with recent memory.
12. Explain Adam as momentum plus RMSProp-style scaling.

## Short Summary

Optimizers are strategies for turning gradients into parameter updates.

- Learning rate controls step size.
- Momentum remembers direction.
- AdaGrad adapts learning rates per parameter.
- RMSProp adapts using recent gradient history.
- Adam combines momentum and adaptive learning rates.

Best one-line explanation:

> An optimizer decides how far and in what way each parameter should move so the neural network can reduce its loss.
