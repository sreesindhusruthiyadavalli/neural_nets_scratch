# Neural Network Regularization Notes

Video reference: https://youtu.be/tZA5nVMITeM

Video title: Lecture 30 - L1/L2 Regularization to avoid neural network overfitting

## How To Explain Regularization

Regularization is a technique used to reduce **overfitting**.

Overfitting means:

> The model performs very well on training data, but poorly on new/unseen data.

In simple words:

> The model memorized the training examples instead of learning the general pattern.

Regularization helps the model stay simpler, so it generalizes better.

## Main Idea

Normally, neural networks minimize only the data loss:

```text
total loss = data loss
```

With regularization, we add a penalty for complex weights:

```text
total loss = data loss + regularization penalty
```

So the model is no longer rewarded only for fitting the training data. It is also encouraged to keep weights smaller or simpler.

## Why Penalize Weights?

Large weights can make the model too sensitive.

Small input changes may cause large output changes. That often means the model is fitting small noise in the training data.

Good explanation:

> Regularization tells the model: "Fit the data, but do not use unnecessarily large weights."

## L2 Regularization

L2 regularization adds a penalty based on the square of the weights.

```text
L2 penalty = lambda * sum(weights^2)
```

So the total loss becomes:

```text
total loss = data loss + lambda * sum(weights^2)
```

L2 pushes weights toward small values, but usually does not make them exactly zero.

Good explanation:

> L2 regularization discourages large weights. It keeps the model smoother and less sensitive.

Effect of L2:

- Reduces overfitting.
- Keeps weights small.
- Makes the model smoother.
- Usually keeps all features involved, but with smaller influence.

## L1 Regularization

L1 regularization adds a penalty based on the absolute value of the weights.

```text
L1 penalty = lambda * sum(abs(weights))
```

So the total loss becomes:

```text
total loss = data loss + lambda * sum(abs(weights))
```

L1 can push some weights exactly to zero.

Good explanation:

> L1 regularization can make the model ignore less useful features by shrinking their weights to zero.

Effect of L1:

- Reduces overfitting.
- Encourages sparsity.
- Some weights may become exactly zero.
- Useful for feature selection.

## Lambda

`lambda` controls the strength of regularization.

If lambda is too small:

> Regularization has almost no effect.

If lambda is too large:

> The model becomes too restricted and may underfit.

Good explanation:

> Lambda controls how strict we are about keeping weights small.

## Overfitting vs Underfitting

No regularization or too little regularization:

```text
training accuracy high
testing accuracy low
```

This is overfitting.

Too much regularization:

```text
training accuracy low
testing accuracy also low
```

This is underfitting.

Good regularization:

```text
training accuracy good
testing accuracy good
```

This means better generalization.

## Simple Teaching Analogy

Without regularization:

> The model is allowed to write a very complicated rule that matches every training point.

With regularization:

> The model is asked to find a simpler rule that still explains the data well.

## Best Short Explanation

> Regularization reduces overfitting by adding a penalty to the loss function. This penalty discourages overly large or unnecessary weights, helping the model learn simpler patterns that work better on unseen data.
