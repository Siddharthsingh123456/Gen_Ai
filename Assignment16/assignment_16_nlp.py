
import re
import pandas as pd
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

print("=" * 72)
print("ASSIGNMENT 16 - NLP TEXT PREPROCESSING PIPELINE")
print("=" * 72)

# Dataset: 30 text samples selected from the supplied IMDb-style movie-review CSV.
df = pd.read_csv("data/text_dataset_30.csv")
text_col = "text"
df[text_col] = df[text_col].fillna("").astype(str)

print("\nDATASET INFORMATION")
print("Shape:", df.shape)
print("Columns:", list(df.columns))

# ----------------------------------------------------------------------
# TASK 1 - UNDERSTANDING RAW TEXT DATA
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 1 - UNDERSTANDING RAW TEXT DATA")
print("=" * 72)

print("\nFirst 5 text samples:")
for i, text in enumerate(df[text_col].head(5), 1):
    print(f"\nSample {i}: {text[:500]}")

print("\nLength of each text:")
df["text_length"] = df[text_col].str.len()
print(df[["text_length"]].head(10).to_string())

sample_raw = "I LOVED this Movie!!! It was GREAT!!! 123    <b>Wow</b>"
print("\nCommon raw-text issues found:")
print("- Uppercase/lowercase differences")
print("- Punctuation such as !, ?, commas and full stops")
print("- Numbers")
print("- Extra/repeated spaces")
print("- HTML tags, URLs and special symbols may occur in raw text")
print("\nExample raw text:", sample_raw)

# ----------------------------------------------------------------------
# TASK 2 - BASIC TEXT CLEANING
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 2 - BASIC TEXT CLEANING")
print("=" * 72)

def basic_clean(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)       # punctuation
    text = re.sub(r"\d+", " ", text)           # numbers
    text = re.sub(r"\s+", " ", text).strip()   # extra spaces
    return text

df["clean_text_basic"] = df[text_col].apply(basic_clean)
print(df[[text_col, "clean_text_basic"]].head(3).to_string(index=False))

# ----------------------------------------------------------------------
# TASK 3 - ADVANCED NOISE REMOVAL
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 3 - REMOVING NOISE")
print("=" * 72)

def advanced_clean(text):
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

noise_demo = "Visit https://example.com or mail me@test.com <b>Hello!</b> 😊"
print("Noise-removal demo:")
print("Before:", noise_demo)
print("After :", advanced_clean(noise_demo))

df["clean_text_advanced"] = df[text_col].apply(advanced_clean)
print("\nAdvanced cleaned samples:")
print(df[["clean_text_advanced"]].head(3).to_string(index=False))

# ----------------------------------------------------------------------
# TASK 4 - HANDLING STOPWORDS
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 4 - HANDLING STOPWORDS")
print("=" * 72)

# NLTK is the required NLP library. If the local NLTK corpus is unavailable,
# use a small standard-English fallback so the assignment can still run.
try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
    stopword_source = "NLTK English stopwords corpus"
except LookupError:
    stop_words = {
        "a","an","and","are","as","at","be","by","for","from","has","he","in",
        "is","it","its","of","on","that","the","this","to","was","were","will",
        "with","i","you","your","they","them","we","our","but","or","not"
    }
    stopword_source = "NLTK-compatible fallback set because the NLTK corpus was unavailable"

def remove_stopwords(text):
    words = text.split()
    return " ".join(word for word in words if word not in stop_words)

df["text_no_stopwords"] = df["clean_text_advanced"].apply(remove_stopwords)
print("Stopword source:", stopword_source)
print(df[["clean_text_advanced", "text_no_stopwords"]].head(3).to_string(index=False))

# ----------------------------------------------------------------------
# TASK 5 - REPEATED CHARACTERS AND SLANG
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 5 - REPEATED CHARACTERS AND SLANG")
print("=" * 72)

def normalize_repeated_chars(text):
    return re.sub(r"(.)\1{2,}", r"\1\1", text)

slang_dict = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "gr8": "great",
    "btw": "by the way",
    "omg": "oh my god",
    "idk": "i do not know"
}

def replace_slang(text):
    words = text.split()
    return " ".join(slang_dict.get(word, word) for word in words)

repeat_demo = "This movie was soooo goooood!!!"
slang_demo = "u r gr8 btw"
print("Repeated-character demo:")
print("Before:", repeat_demo)
print("After :", normalize_repeated_chars(repeat_demo))
print("\nSlang dictionary:", slang_dict)
print("Slang demo:", slang_demo)
print("After:", replace_slang(slang_demo))

df["clean_text_advanced"] = df["clean_text_advanced"].apply(normalize_repeated_chars)
df["clean_text_advanced"] = df["clean_text_advanced"].apply(replace_slang)

# ----------------------------------------------------------------------
# TASK 6 - TOKENIZATION
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 6 - TOKENIZATION")
print("=" * 72)

def word_tokenize_safe(text):
    try:
        return nltk.word_tokenize(text)
    except LookupError:
        return re.findall(r"\b\w+\b", text)

def sentence_tokenize_safe(text):
    try:
        return nltk.sent_tokenize(text)
    except LookupError:
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

for i, text in enumerate(df[text_col].head(3), 1):
    print(f"\nSample {i} word tokens:")
    print(word_tokenize_safe(text)[:30])
    print(f"Sample {i} sentence tokens:")
    print(sentence_tokenize_safe(text)[:5])

df["word_tokens"] = df["clean_text_advanced"].apply(word_tokenize_safe)
df["sentence_tokens"] = df[text_col].apply(sentence_tokenize_safe)

# ----------------------------------------------------------------------
# TASK 7 - STEMMING
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 7 - STEMMING")
print("=" * 72)

stemmer = PorterStemmer()
stem_examples = ["playing", "played", "plays", "studies", "studying", "happily", "movies"]

for word in stem_examples:
    print(f"{word:12} -> {stemmer.stem(word)}")

df["stemmed_text"] = df["text_no_stopwords"].apply(
    lambda x: " ".join(stemmer.stem(w) for w in word_tokenize_safe(x))
)

# ----------------------------------------------------------------------
# TASK 8 - LEMMATIZATION
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 8 - LEMMATIZATION")
print("=" * 72)

lemmatizer = WordNetLemmatizer()

def lemmatize_word(word):
    try:
        return lemmatizer.lemmatize(word)
    except LookupError:
        # Simple fallback for execution when WordNet data is not installed.
        rules = [
            ("ies", "y"), ("ing", ""), ("ed", ""), ("es", ""), ("s", "")
        ]
        for suffix, replacement in rules:
            if len(word) > len(suffix) + 2 and word.endswith(suffix):
                return word[:-len(suffix)] + replacement
        return word

lemma_examples = ["playing", "played", "movies", "studies", "cars", "running"]
print("Original -> Stem -> Lemma")
for word in lemma_examples:
    print(f"{word:10} -> {stemmer.stem(word):10} -> {lemmatize_word(word)}")

df["lemmatized_text"] = df["text_no_stopwords"].apply(
    lambda x: " ".join(lemmatize_word(w) for w in word_tokenize_safe(x))
)

# ----------------------------------------------------------------------
# TASK 9 - FINAL NLP PIPELINE
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 9 - FINAL NLP PIPELINE")
print("=" * 72)

def nlp_preprocess(text):
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = normalize_repeated_chars(text)
    text = re.sub(r"\s+", " ", text).strip()
    text = replace_slang(text)

    tokens = word_tokenize_safe(text)
    tokens = [w for w in tokens if w not in stop_words]
    tokens = [lemmatize_word(w) for w in tokens]
    return " ".join(tokens)

df["final_clean_text"] = df[text_col].apply(nlp_preprocess)
print(df[[text_col, "final_clean_text"]].head(5).to_string(index=False))

# ----------------------------------------------------------------------
# TASK 10 - OBSERVATIONS AND INSIGHTS
# ----------------------------------------------------------------------
print("\n" + "=" * 72)
print("TASK 10 - OBSERVATIONS & INSIGHTS")
print("=" * 72)

observations = [
    "Basic cleaning handles simple formatting issues such as case, punctuation, numbers and extra spaces.",
    "Advanced cleaning goes further by removing URLs, email addresses, HTML tags and special characters, producing more consistent text.",
    "Stopword removal reduces common words that usually add little information for many NLP tasks.",
    "Repeated-character normalization changes informal spellings such as 'soooo' into a shorter standard form, while the slang dictionary maps common chat-style words to clearer forms.",
    "Lemmatization is generally preferred when preserving meaningful dictionary words matters because it aims to return a normalized word form rather than only cutting characters.",
    "Preprocessing is important because inconsistent raw text creates unnecessary vocabulary variation and noise, which can make later NLP models less effective and harder to interpret."
]

for i, item in enumerate(observations, 1):
    print(f"{i}. {item}")

# Save all required outputs.
df.to_csv("assignment_16_nlp_results.csv", index=False)

print("\nFinal columns:")
print(list(df.columns))
print("\nPIPELINE COMPLETED SUCCESSFULLY")
