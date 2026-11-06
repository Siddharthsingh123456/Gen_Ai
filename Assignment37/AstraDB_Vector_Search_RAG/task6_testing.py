"""TASK 6 - Testing & validation.
1. Ask 5 questions from the PDF  2. Verify answers come from the document  3. Out-of-context questions.
Run:  python task6_testing.py      (after task4_store_embeddings.py has indexed data/sample.pdf)"""
from rag_core import NOT_FOUND, answer_question, get_embeddings, get_llm, get_vector_store

# (question, keyword that must appear in a correct answer, found in the PDF)
IN_DOC = [
    ("By roughly how much have solar panel prices fallen since 2010?", ["90", "ninety"]),
    ("Which country's feed-in tariff created a large stable market for renewables?", ["germany"]),
    ("Why does building new high-voltage transmission lines take so long?", ["permit", "land", "oppos"]),
    ("Which technology lets midday solar electricity be used in the evening?", ["batter"]),
    ("Name critical minerals needed for batteries.", ["lithium", "cobalt", "nickel"]),
]
OUT_OF_DOC = [
    "Who won the FIFA World Cup in 2018?",
    "What is the recipe for pasta carbonara?",
]

vstore, llm = get_vector_store(get_embeddings()), get_llm()
passed = 0

print("=== Part 1 & 2: questions from the PDF (answer + source check) ===")
for q, keywords in IN_DOC:
    r = answer_question(vstore, llm, q)
    has_keyword = any(k in r["answer"].lower() for k in keywords)
    # grounded = the retrieved chunks really contain the keyword, i.e. the answer comes from the document
    grounded = bool(r["sources"]) and any(k in s["text"].lower() for s in r["sources"] for k in keywords)
    ok = has_keyword and grounded
    passed += ok
    pages = sorted({s["page"] for s in r["sources"]})
    print(f"\n[{'PASS' if ok else 'CHECK'}] {q}\n  Answer : {r['answer']}\n  Sources: pages {pages}")

print("\n=== Part 3: out-of-context questions (should be declined gracefully) ===")
for q in OUT_OF_DOC:
    r = answer_question(vstore, llm, q)
    declined = "couldn't find" in r["answer"].lower()
    passed += declined
    print(f"\n[{'PASS' if declined else 'CHECK'}] {q}\n  Answer : {r['answer']}")

total = len(IN_DOC) + len(OUT_OF_DOC)
print(f"\nResult: {passed}/{total} checks passed. Graceful fallback message: \"{NOT_FOUND}\"")
