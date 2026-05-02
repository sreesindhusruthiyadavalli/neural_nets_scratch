# Telugu Poem Generation with Laghu/Guru Constraints

## Goal

Generate a meaningful 4-line Telugu poem that follows a required laghu/guru pattern.

The system should not depend on the LLM blindly following the meter. Instead, the LLM should generate poem candidates, and our laghu/guru system should verify whether the generated poem follows the required pattern.

## Important Design Decision

We do not need to build our own full LLM from scratch for this project.

Building a custom LLM would require:

- a very large Telugu text corpus
- tokenizer training
- byte pair encoding or another subword tokenizer
- transformer pretraining
- GPUs
- fine-tuning data
- evaluation and alignment

The current laghu/guru dataset is useful for learning and for building a word-level predictor, but it is not enough to train a language model that can generate meaningful Telugu poetry.

So the practical architecture is:

```text
existing Telugu-capable LLM
        +
our laghu/guru mapper
        +
our poem verifier
        +
repair loop
```

## Two Separate Problems

There are two different tasks in this project.

### 1. Meter Task

```text
Telugu word -> laghu/guru pattern
```

Example:

```text
మంచివాని -> UIUI
తత్వంబు -> UUI
మోక్షంబు -> UUI
```

This is where our neural network is useful.

The NN can learn:

```text
Telugu word or akshara sequence -> I/U sequence
```

For a stronger system, this should eventually become a hybrid:

```text
Telugu word
  -> akshara splitter
  -> rule-based prosody features
  -> neural correction/fallback
  -> laghu/guru pattern
```

### 2. Poem Generation Task

```text
theme + meaning + meter constraints -> 4-line Telugu poem
```

This is where an existing LLM should be used.

The LLM should only do the language generation job:

```text
Generate meaningful Telugu poem lines using the given theme,
word bank, meanings, and laghu/guru hints.
```

It should not be trusted as the final judge of meter.

## Why BPE Is Not Enough

Byte pair encoding is useful for language modeling, especially in English-like LLM pipelines.

But BPE does not understand Telugu chandassu by itself.

BPE splits text based on statistical frequency. Laghu/guru depends on Telugu sound units, especially aksharas, vowel length, consonant clusters, anusvara, visarga, and related prosody rules.

So this project needs a separate chandassu tokenizer:

```text
Telugu word -> aksharas -> laghu/guru pattern
```

This is different from the LLM tokenizer:

```text
text -> BPE/subword tokens -> transformer
```

## Recommended Architecture

```text
Input:
  theme
  target poem type or target I/U pattern

Step 1:
  Select useful Telugu words from the word bank.

Step 2:
  For each word, attach:
    - meaning
    - laghu/guru pattern
    - optional theme tags

Step 3:
  Ask the LLM to generate exactly 4 Telugu lines.

Step 4:
  Split generated poem into lines and words.

Step 5:
  Use our laghu/guru mapper to compute each line pattern.

Step 6:
  Compare generated patterns with required patterns.

Step 7:
  If a line fails, ask the LLM to rewrite only that line.

Output:
  final 4-line poem
  laghu/guru pattern for each line
  pass/fail validation
```

## Word Bank Format

A useful word record should look like this:

```json
{
  "word": "మంచివాని",
  "meaning": "good person",
  "laghu_guru": "UIUI",
  "part_of_speech": "noun/adjective",
  "theme_tags": ["morality", "wisdom", "person"]
}
```

The LLM can then use words based on both meaning and meter.

## LLM Prompt Shape

The LLM should receive a narrow instruction:

```text
You are only a Telugu poem generator.

Theme:
  wisdom and self-knowledge

Required output:
  exactly 4 Telugu lines

Meter constraint:
  line 1 must follow: ...
  line 2 must follow: ...
  line 3 must follow: ...
  line 4 must follow: ...

Useful words:
  మంచివాని -> UIUI -> good person
  ఎరుక -> III -> awareness
  తత్వంబు -> UUI -> truth/principle
  మోక్షంబు -> UUI -> liberation

Do not explain.
Output only the poem.
```

## Verification Loop

After generation:

```text
generated poem
  -> split into 4 lines
  -> split each line into words
  -> compute word-level I/U patterns
  -> combine into line-level I/U patterns
  -> compare with target patterns
```

If a line does not match:

```text
Line 2 failed.
Required pattern: UIUIII
Generated pattern: UIUUII

Rewrite only line 2.
Preserve the meaning.
Use these replacement words if possible:
...
```

The system repeats this until all lines pass or a maximum retry count is reached.

## MVP Plan

### Phase 1: Laghu/Guru Data Cleanup

- Clean the existing word-pattern dataset.
- Remove trailing spaces.
- Check duplicate words.
- Confirm whether duplicate words always have the same pattern.

### Phase 2: Akshara Splitter

- Build a Telugu akshara splitter.
- Handle vowel signs, anusvara, visarga, and conjuncts.
- Use aksharas instead of raw Unicode characters wherever possible.

### Phase 3: Laghu/Guru Mapper

- Start with rules where possible.
- Train the current NN as a learning model and fallback.
- Evaluate word-level prediction accuracy.

### Phase 4: Word Bank with Meanings

- Add semantic meanings to words.
- Add theme tags.
- Add part-of-speech where useful.

### Phase 5: LLM Poem Generator

- Use an existing Telugu-capable LLM.
- Give it a strict prompt.
- Provide useful words with meanings and laghu/guru patterns.

### Phase 6: Meter Verifier

- Verify every generated line.
- Reject poems that do not match.
- Return mismatch details.

### Phase 7: Repair Loop

- Ask the LLM to rewrite failed lines only.
- Preserve the theme and meaning.
- Repeat verification.

### Phase 8: Named Poem Types

- Map poem types to expected line patterns.
- Support meters such as `aataveladi` or `tetageeti` after the verifier is reliable.

## What To Build From Scratch

Build these from scratch:

- Telugu akshara splitter
- laghu/guru mapper
- small NN for word-to-pattern prediction
- word bank
- poem verifier
- repair loop

Do not build these from scratch for the MVP:

- full LLM
- full transformer pretraining pipeline
- BPE tokenizer for a Telugu LLM

Those are useful only if the separate goal is to learn how LLMs are built internally.

## Final Direction

The best first version is:

```text
existing LLM writes the poem
our system checks the meter
our NN helps map words to laghu/guru
the verifier decides whether the poem is valid
```

This keeps the LLM focused on semantic Telugu poem generation and keeps the chandassu correctness inside our own system.
