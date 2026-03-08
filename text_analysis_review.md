# Text Analyzer Evaluation Report

## 1. Exact Prompt Used

    Write a Python module with a function called analyze_text(text: str, **options) that accepts any text and keyword arguments for options (count_words=True, count_sentences=True, find_longest_word=True, sentiment_simple=True). Each option enables a different analysis. Use *args and **kwargs, add type hints and Google-style docstrings. Return a dict with all requested analyses.

------------------------------------------------------------------------

# 2. AI Generated Code

``` python
from typing import Dict, Any
import re

def analyze_text(text: str, *args, **options) -> Dict[str, Any]:
    """
    Analyze a text string with configurable analysis options.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    result: Dict[str, Any] = {}

    count_words = options.get("count_words", True)
    count_sentences = options.get("count_sentences", True)
    find_longest_word = options.get("find_longest_word", True)
    sentiment_simple = options.get("sentiment_simple", True)

    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"[.!?]+", text.strip())
    sentences = [s for s in sentences if s.strip()]

    if count_words:
        result["word_count"] = len(words)

    if count_sentences:
        result["sentence_count"] = len(sentences)

    if find_longest_word:
        result["longest_word"] = max(words, key=len) if words else None

    if sentiment_simple:
        positive_words = {"good", "great", "excellent", "love", "amazing", "happy"}
        negative_words = {"bad", "terrible", "hate", "awful", "sad", "poor"}

        pos = sum(1 for w in words if w.lower() in positive_words)
        neg = sum(1 for w in words if w.lower() in negative_words)

        if pos > neg:
            sentiment = "positive"
        elif neg > pos:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        result["sentiment"] = sentiment

    return result
```

------------------------------------------------------------------------

# 3. Critical Evaluation

## 3.1 Does it properly use \*\*kwargs?

Yes.

The function retrieves configuration options using:

``` python
options.get("count_words", True)
```

This allows flexible configuration without changing the function
signature.

However: - It does not validate unknown options. - Incorrect option
names will silently be ignored.

Better approach:

    validate allowed options

or raise an error if unsupported options are passed.

------------------------------------------------------------------------

## 3.2 Are type hints correct?

Mostly correct.

    (text: str) -> Dict[str, Any]

However:

-   The dictionary keys are known (`word_count`, `sentence_count`, etc.)
-   Using `Dict[str, Any]` is overly generic.

Better type hint:

    dict[str, int | str | None]

or using TypedDict for strict typing.

------------------------------------------------------------------------

## 3.3 Edge Case Handling

Handled cases:

✔ Non-string input raises `TypeError`\
✔ Empty word list handled with `if words else None`

Missing edge cases:

-   Empty string `" "` still processed unnecessarily
-   Unknown options not validated
-   Sentiment lexicon extremely small

------------------------------------------------------------------------

## 3.4 Docstring Quality

The docstring exists but is minimal.

Problems:

-   Does not document return structure clearly
-   Does not explain sentiment algorithm
-   Does not describe supported options in detail

A better docstring should include:

-   parameter descriptions
-   return schema
-   example usage

------------------------------------------------------------------------

## 3.5 Single Responsibility Principle (SRP)

The function violates SRP.

It performs multiple responsibilities:

1.  Word tokenization
2.  Sentence splitting
3.  Longest word computation
4.  Sentiment analysis
5.  Configuration parsing

This makes the function:

-   harder to test
-   harder to maintain
-   harder to extend

Better design: split into smaller functions.

------------------------------------------------------------------------

# 4. Improved Implementation

The improved version separates responsibilities into dedicated
functions.

``` python
import re
from typing import Dict, Any, List


def tokenize_words(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text)


def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"[.!?]+", text.strip())
    return [s for s in sentences if s.strip()]


def get_longest_word(words: List[str]) -> str | None:
    return max(words, key=len) if words else None


def simple_sentiment(words: List[str]) -> Dict[str, int | str]:

    positive_words = {"good", "great", "excellent", "love", "amazing", "happy"}
    negative_words = {"bad", "terrible", "hate", "awful", "sad", "poor"}

    pos = sum(1 for w in words if w.lower() in positive_words)
    neg = sum(1 for w in words if w.lower() in negative_words)

    if pos > neg:
        sentiment = "positive"
    elif neg > pos:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "positive_matches": pos,
        "negative_matches": neg
    }


def analyze_text(text: str, **options) -> Dict[str, Any]:
    """
    Analyze text with configurable options.

    Args:
        text (str): Input text.
        **options: Analysis options.

            count_words (bool)
            count_sentences (bool)
            find_longest_word (bool)
            sentiment_simple (bool)

    Returns:
        dict: Dictionary containing requested analyses.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    words = tokenize_words(text)
    sentences = split_sentences(text)

    results: Dict[str, Any] = {}

    if options.get("count_words", True):
        results["word_count"] = len(words)

    if options.get("count_sentences", True):
        results["sentence_count"] = len(sentences)

    if options.get("find_longest_word", True):
        results["longest_word"] = get_longest_word(words)

    if options.get("sentiment_simple", True):
        results.update(simple_sentiment(words))

    return results
```

------------------------------------------------------------------------

# 5. Improvements Achieved

✔ Smaller functions (better testing)\
✔ Clear responsibilities\
✔ Cleaner main API\
✔ Easier to extend\
✔ More maintainable architecture

------------------------------------------------------------------------

# 6. Key Software Engineering Takeaway

Good code should prioritize:

-   **Modularity**
-   **Testability**
-   **Separation of concerns**
-   **Clear documentation**

Breaking large functions into smaller reusable components significantly
improves maintainability.
