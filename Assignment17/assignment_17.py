
import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

print("Assignment 17 - Text Cleaning, Preprocessing & NLP Pipeline")
print("-" * 60)

# ---------------- TASK 1 ----------------
print("\nTASK 1: Understanding Raw Text Data")

data = pd.read_csv("data/text_dataset_30.csv")
data["text"] = data["text"].fillna("").astype(str)

print("Rows and columns:", data.shape)
print("\nFirst 5 samples:")
for i, x in enumerate(data["text"].head(), 1):
    print("\n", i, ":", x[:350])

data["text_length"] = data["text"].apply(len)
print("\nLengths of first 10 texts:")
print(data["text_length"].head(10).tolist())

# A small example makes the problems easier to see.
example = "I LOVE this movie!!! 123   <b>great</b> 😊"
print("\nRaw example:", example)
print("Problems I can see: capitals, punctuation, number, HTML, symbol and extra spaces.")

# ---------------- TASK 2 ----------------
print("\nTASK 2: Basic Text Cleaning")

def basic_clean(x):
    x = x.lower()
    x = re.sub(r"[^\w\s]", " ", x)
    x = re.sub(r"[0-9]", " ", x)
    x = " ".join(x.split())
    return x

data["clean_text_basic"] = data["text"].apply(basic_clean)

print("\nOriginal vs basic cleaned:")
print(data[["text", "clean_text_basic"]].head(5).to_string(index=False))

# ---------------- TASK 3 ----------------
print("\nTASK 3: Removing Noise")

def remove_noise(x):
    x = re.sub(r"https?://\S+|www\.\S+", " ", x)
    x = re.sub(r"\S+@\S+", " ", x)
    x = re.sub(r"<.*?>", " ", x)
    x = re.sub(r"[^A-Za-z\s]", " ", x)
    x = " ".join(x.split())
    return x.lower()

noise_test = "See https://example.com, email me@test.com <b>Hello</b> 😊!!!"
print("Before:", noise_test)
print("After :", remove_noise(noise_test))

data["clean_text_advanced"] = data["text"].apply(remove_noise)

# ---------------- TASK 4 ----------------
print("\nTASK 4: Stopword Removal")

try:
    stop_words = set(nltk.corpus.stopwords.words("english"))
    stop_source = "NLTK stopwords"
except LookupError:
    # The execution environment may not have downloaded the NLTK corpus.
    # Keep a small list so the rest of the assignment can still be run.
    stop_words = {
        "a","an","and","are","as","at","be","by","for","from","has","he","in",
        "is","it","of","on","that","the","this","to","was","were","with","i",
        "you","your","we","they","but","or","not"
    }
    stop_source = "small fallback because NLTK stopwords were unavailable"

def without_stopwords(x):
    words = x.split()
    return " ".join([w for w in words if w not in stop_words])

data["text_no_stopwords"] = data["clean_text_advanced"].apply(without_stopwords)
print("Stopword source:", stop_source)
print(data[["clean_text_advanced", "text_no_stopwords"]].head(5).to_string(index=False))

# ---------------- TASK 5 ----------------
print("\nTASK 5: Repeated Characters and Slang")

def repeat_fix(x):
    # Keep at most two of the same character.
    return re.sub(r"(.)\1\1+", r"\1\1", x)

slang = {
    "u": "you",
    "ur": "your",
    "r": "are",
    "gr8": "great",
    "btw": "by the way"
}

def slang_fix(x):
    words = x.split()
    return " ".join(slang.get(w, w) for w in words)

print("Repeated example:")
print("soooo good ->", repeat_fix("soooo good"))
print("Slang example:")
print("u r gr8 btw ->", slang_fix("u r gr8 btw"))

data["clean_text_advanced"] = data["clean_text_advanced"].apply(repeat_fix)
data["clean_text_advanced"] = data["clean_text_advanced"].apply(slang_fix)

# ---------------- TASK 6 ----------------
print("\nTASK 6: Tokenization")

def words(text):
    try:
        return nltk.word_tokenize(text)
    except LookupError:
        return text.split()

def sentences(text):
    try:
        return nltk.sent_tokenize(text)
    except LookupError:
        return [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

for i in range(3):
    print("\nSample", i + 1)
    print("Word tokens:", words(data.loc[i, "clean_text_advanced"])[:20])
    print("Sentence tokens:", sentences(data.loc[i, "text"])[:3])

data["word_tokens"] = data["clean_text_advanced"].apply(words)
data["sentence_tokens"] = data["text"].apply(sentences)

# ---------------- TASK 7 ----------------
print("\nTASK 7: Stemming")

stemmer = PorterStemmer()
compare_words = ["playing", "played", "plays", "movies", "studies"]

print("Original -> Stem")
for w in compare_words:
    print(w, "->", stemmer.stem(w))

data["stemmed_text"] = data["text_no_stopwords"].apply(
    lambda x: " ".join(stemmer.stem(w) for w in words(x))
)

# ---------------- TASK 8 ----------------
print("\nTASK 8: Lemmatization")

lemmatizer = WordNetLemmatizer()

def lemma(w):
    try:
        return lemmatizer.lemmatize(w)
    except LookupError:
        # Simple fallback for this offline run.
        if w.endswith("ies") and len(w) > 4:
            return w[:-3] + "y"
        if w.endswith("s") and len(w) > 3:
            return w[:-1]
        return w

print("Word | Stem | Lemma")
for w in compare_words:
    print(w, "|", stemmer.stem(w), "|", lemma(w))

data["lemmatized_text"] = data["text_no_stopwords"].apply(
    lambda x: " ".join(lemma(w) for w in words(x))
)

# ---------------- TASK 9 ----------------
print("\nTASK 9: Final NLP Function")

def nlp_preprocess(text):
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[0-9]", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = repeat_fix(text)
    text = slang_fix(text)
    text = " ".join(text.split())

    tokens = words(text)
    tokens = [w for w in tokens if w not in stop_words]
    tokens = [lemma(w) for w in tokens]
    return " ".join(tokens)

data["final_clean_text"] = data["text"].apply(nlp_preprocess)

print("\nFinal original vs final text:")
print(data[["text", "final_clean_text"]].head(5).to_string(index=False))

# ---------------- TASK 10 ----------------
print("\nTASK 10: Observations")

before_avg = data["text_length"].mean()
after_avg = data["final_clean_text"].str.len().mean()

print("1. Basic cleaning mainly changes formatting: case, punctuation, numbers and spaces.")
print("2. Advanced cleaning removes extra sources of noise such as URLs, emails and HTML.")
print("3. In this run, the final text is shorter on average.")
print("   Average original length:", round(before_avg, 2))
print("   Average final length   :", round(after_avg, 2))
print("4. Stemming can create shortened forms that are not normal dictionary words.")
print("5. Lemmatization is preferable when readable word forms and meaning are important.")
print("6. Preprocessing reduces unnecessary variations in the vocabulary before an NLP model is trained.")

data.to_csv("assignment_17_results.csv", index=False)
print("\nSaved: assignment_17_results.csv")
print("\nCompleted all 10 tasks.")
