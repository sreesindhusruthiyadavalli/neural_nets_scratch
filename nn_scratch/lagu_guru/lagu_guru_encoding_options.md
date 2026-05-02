# Encoding Options for Telugu Laghu/Guru Prediction

## Use Case

The final goal is Telugu poem-type identification.

A poem has 4 lines. Each line has words. Each word maps to a laghu/guru pattern made of `I` and `U`.

The complete pipeline looks like this:

```text
poem
  -> 4 lines
  -> words in each line
  -> I/U pattern for each word
  -> combined I/U pattern for each line
  -> compare all 4 line patterns
  -> poem type
```

Example high-level flow:

```text
line 1 -> word patterns -> line pattern
line 2 -> word patterns -> line pattern
line 3 -> word patterns -> line pattern
line 4 -> word patterns -> line pattern
```

If all 4 lines follow a required shared pattern, the poem can be mapped to one type, such as `aataveledi`.

If the 4 lines follow different expected patterns, the poem can be mapped to another type, such as `tetageeti`.

## Current First Step

As the first step, we are not classifying the whole poem yet. We are working on the smaller problem:

```text
Telugu word -> laghu/guru pattern
```

Once word-level prediction works, the next steps are:

```text
word-level I/U patterns -> line-level I/U pattern
line-level I/U patterns -> poem-level type
```

So the current dataset has Telugu words and their laghu/guru pattern:

```text
అంతరంగమందు UIUIUI
అపరాధములు IIUIIII
జేసి UI
మంచివాని UIUI
```

The machine learning task is:

```text
Telugu word -> laghu/guru pattern
```

Example:

```text
మంచివాని -> UIUI
```

A neural network cannot directly process Telugu text. The word must first be converted into numbers. That conversion step is called encoding.

## 1. Character One-Hot Encoding

Each Telugu character is represented as a vector with one `1` and the rest `0`.

Example idea:

```text
వ -> [0, 0, 1, 0, 0, ...]
ే -> [0, 1, 0, 0, 0, ...]
మ -> [1, 0, 0, 0, 0, ...]
```

For a fixed maximum word length:

```text
word length = 16
vocabulary size = 40
input size = 16 * 40 = 640
```

### Why Use It

- Simple to implement from scratch.
- Works with only NumPy.
- Good for learning neural network basics.
- Avoids fake numeric ordering between Telugu characters.

### Limitations

- Sparse and large input vectors.
- Does not understand syllables or pronunciation.
- Does not know Telugu prosody rules.
- Needs more data to generalize well.

## 2. Integer Encoding

Each character is assigned an integer ID.

Example:

```text
వ -> 12
ే -> 25
మ -> 9
```

Then a word becomes a sequence of integers:

```text
వేమ -> [12, 25, 9]
```

### Why Use It

- Compact representation.
- Easy to store and pass into models.
- Useful before an embedding layer.

### Limitation

Integer IDs alone are usually not enough. A model may incorrectly treat nearby numbers as similar:

```text
character 2 is close to character 3
```

That numeric closeness may not mean anything linguistically.

## 3. Character Embeddings

Character embeddings start with integer encoding, then learn a dense vector for each character.

Example:

```text
వ -> [0.12, -0.34, 0.88, ...]
మ -> [-0.51, 0.09, 0.27, ...]
```

Flow:

```text
Telugu character -> integer ID -> embedding vector -> neural network
```

### Why Use It

- More compact than one-hot encoding.
- Learns useful relationships between characters.
- Better for larger datasets.
- Works well with sequence models like RNNs, CNNs, or Transformers.

### Limitation

- Needs more data than one-hot encoding.
- Slightly more complex to implement from scratch.

## 4. Akshara or Syllable-Level Encoding

For Telugu chandassu, aksharas are often more meaningful than raw Unicode characters.

Instead of encoding:

```text
వ ే మ
```

encode pronunciation-like units:

```text
వే | మ
```

Then the task becomes closer to:

```text
akshara sequence -> laghu/guru sequence
```

Example:

```text
మంచివాని -> మం | చి | వా | ని -> UIUI
```

### Why Use It

- More aligned with chandassu.
- Better fit for laghu/guru classification.
- Reduces mismatch between Unicode characters and spoken units.

### Limitation

- Requires a Telugu akshara splitter.
- Must carefully handle vowel signs, conjuncts, anusvara, and visarga.

## 5. Handcrafted Prosody Features

Instead of only encoding symbols, extract features based on Telugu prosody rules.

Possible features:

- vowel length
- short vowel vs long vowel
- syllable ending type
- consonant cluster after vowel
- anusvara
- visarga
- word-final position
- akshara length

Example:

```text
akshara = వా
features = [long_vowel=1, has_consonant_cluster=0, has_anusvara=0]
```

### Why Use It

- Very useful for small datasets.
- Encodes domain knowledge directly.
- Better than expecting the model to learn rules from only a few examples.

### Limitation

- Requires linguistic rule implementation.
- Mistakes in preprocessing affect the model.

## 6. Character N-Gram Encoding

N-grams represent small chunks of nearby characters.

Example character bigrams:

```text
మంచివాని -> మం, ంచ, చి, ివ, వా, ాన, ని
```

The model receives information about local character patterns instead of isolated characters.

### Why Use It

- Captures local context.
- Useful for traditional ML models.
- Can improve over simple character one-hot encoding.

### Limitation

- Creates many possible features.
- Still may not align perfectly with Telugu aksharas.

## 7. Sequence Model Encoding

Instead of flattening a word into one large vector, preserve it as a sequence:

```text
వ -> ే -> మ
```

or:

```text
వే -> మ
```

Then use a model designed for sequences:

- RNN
- LSTM
- GRU
- 1D CNN
- Transformer

Flow:

```text
character or akshara sequence -> sequence model -> I/U pattern
```

### Why Use It

- Preserves order naturally.
- Better for variable-length words.
- Can predict one output symbol per input unit.

### Limitation

- More complex than a simple dense neural network.
- Usually needs more training data.

## 8. Rule-Based Plus Neural Hybrid

For chandassu, a hybrid approach may be the strongest practical option.

Flow:

```text
Telugu word
    -> akshara splitter
    -> rule-based laghu/guru features
    -> neural model or correction model
    -> final I/U pattern
```

### Why Use It

- Rules handle obvious cases.
- Neural model handles ambiguous or exceptional cases.
- More practical when data is small.

### Limitation

- Requires both rule implementation and model training.
- More moving parts to test.

## Target Encoding Options

The output pattern also needs encoding.

### Whole-Pattern Classification

Treat each unique pattern as a class:

```text
UI -> class 0
III -> class 1
UIUI -> class 2
```

Good for quick experiments, but it cannot easily predict a new pattern that was not seen during training.

### Sequence Output Encoding

Encode each output position separately:

```text
PAD = 0
I = 1
U = 2
```

Example:

```text
UI -> [2, 1, 0, 0, 0, ...]
III -> [1, 1, 1, 0, 0, ...]
```

This is better if the model should learn pattern structure instead of memorizing whole pattern labels.

## Recommended Path for This Project

For learning neural networks from scratch:

```text
character one-hot encoding -> dense neural network -> sequence output
```

For a better Telugu chandassu analyzer:

```text
akshara-level encoding + handcrafted prosody features -> sequence model or rule-based hybrid
```

The current dataset is small, so a pure neural network will mostly memorize. More examples and better akshara-level preprocessing will matter more than model complexity.
