# Grammatical Agreement Checking

Detect mismatches between words that must agree grammatically — subject-verb, pronoun-antecedent, tense consistency.

```
"The cats runs"  →  ✗ subject "cats" (plural) doesn't agree with verb "runs" (singular)
"The cat run"    →  ✗ "cat" (singular) doesn't agree with "run" (plural verb form)
"The cat runs"   →  ✓ correct agreement
```

Foundation for grammar checking, translation quality, language education tools.

---

## Core Idea

```
Certain words must MATCH in grammatical features:
   - Subject and verb match in number (singular/plural) and person
   - Pronouns match their antecedents in number and gender
   - Verb tenses align consistently across clauses

Agreement checking detects when this match is broken.
```

---

## Types of Agreement

### Subject-Verb Agreement

```
"She runs"     ✓ third-person singular pronoun + singular verb form
"They run"      ✓ third-person plural + plural verb form
"She run"       ✗ mismatch
"They runs"     ✗ mismatch
```

Verb must agree with subject in **number** and **person**.

### Pronoun-Antecedent Agreement

```
"The boy lost his book"    ✓ "his" agrees with "boy" (masculine, singular)
"The girls lost their books" ✓ "their" agrees with "girls" (plural)
"The boy lost her book"     ✗ gender mismatch
"The boys lost his book"    ✗ number mismatch
```

Pronoun must agree with its **antecedent** (the noun it refers to) in **number** and **gender**.

### Tense Consistency

```
"He was walking when he sees a dog"    ✗ past then sudden present
"He was walking when he saw a dog"     ✓ consistent past tense
"She studied hard and passes the test" ✗ mixed tenses
"She studied hard and passed the test" ✓ consistent past
```

Verb tenses across clauses must be logically consistent.

---

## How Agreement Checking Works

```
1. POS-tag the sentence
   "The cats runs"
   → The/DT cats/NNS runs/VBZ

2. Identify dependency relations
   nsubj(runs, cats)   ← "cats" is the subject of "runs"

3. Check agreement features
   cats: number=plural
   runs: number=singular
   → MISMATCH detected
```

Modern systems use dependency parsers to extract subject-verb pairs and then verify their morphological features.

---

## Agreement in Dependency Structure

Dependency parsing makes agreement checks natural — the dependency arc directly tells you what to compare:

```
"The cats runs"

Dependency arcs:
   The   →   cats   (det)
   cats  →   runs   (nsubj)        ← agreement check here
                                    cats: plural, runs: singular → flag

Result: subject-verb agreement violation
```

---

## Agreement Features to Track

| Feature | Possible Values | Checked Between |
|---------|----------------|-----------------|
| Number | singular, plural | subject & verb, noun & pronoun |
| Person | 1st, 2nd, 3rd | subject & verb |
| Gender | masculine, feminine, neuter | pronoun & antecedent |
| Tense | present, past, future | verbs across clauses |
| Case | nominative, accusative | various (some languages) |
| Definiteness | definite, indefinite | noun & determiner (some languages) |

For English, **number** and **tense** are the most common agreement features to check.

---

## Rule Examples

```
SUBJECT-VERB AGREEMENT RULE:
   if nsubj(verb, noun):
      if number(noun) ≠ number(verb):
         flag agreement error

PRONOUN-ANTECEDENT AGREEMENT RULE:
   if pronoun refers to antecedent_noun:
      if gender(pronoun) ≠ gender(antecedent):
         flag mismatch
      if number(pronoun) ≠ number(antecedent):
         flag mismatch

TENSE CONSISTENCY RULE:
   if two coordinated clauses have verbs:
      if tense(verb_1) ≠ tense(verb_2):
         flag potential inconsistency
```

These rules can be encoded in a grammar checker.

---

## Implementation

### Modern Tools

```python
# Using spaCy for dependency parsing
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp("The cats runs.")

for token in doc:
    if token.dep_ == 'nsubj':
        subject = token
        verb = token.head
        # Check agreement
        if subject.morph.get('Number') != verb.morph.get('Number'):
            print(f"Agreement error: '{subject.text}' ({subject.morph.get('Number')}) "
                  f"doesn't agree with '{verb.text}' ({verb.morph.get('Number')})")
```

### Grammar checkers

```
LanguageTool         → open-source, multilingual grammar checker
Grammarly            → commercial, neural-based
Microsoft Editor     → integrated into Word
```

All combine dependency parsing, agreement rules, and statistical models.

---

## Applications

| Application | Role of agreement checking |
|-------------|---------------------------|
| Grammar checkers | Flag agreement errors for users |
| Machine translation | Maintain agreement when translating |
| Language learning tools | Provide feedback on student writing |
| Automatic essay scoring | Detect grammatical errors |
| Text generation | Ensure generated text is grammatically correct |
| Cross-lingual translation | Different languages have different agreement systems |

---

## Advantages

```
✓ Catches common grammatical errors
✓ Helps non-native speakers and learners
✓ Improves machine translation quality
✓ Easy to interpret and debug — clear rule violations
```

---

## Limitations

```
✗ POS tagging or parsing errors propagate
   if subject is wrongly identified, agreement check fails

✗ Context-dependent agreement
   "The committee has/have decided" — both valid in different dialects

✗ Long-distance dependencies hard to capture
   "The boy who was running in the park near the lake yesterday is/are tired"
   → subject and verb are far apart

✗ Some agreements rely on DISCOURSE, not syntax
   pronoun referring to an antecedent in a previous sentence

✗ Limited to features the parser annotates
```

---

## Cross-Linguistic Variation

Different languages have different agreement systems:

```
English:
   Subject-verb agreement: limited (only third-person singular)
   Adjective-noun: not required ("the big cat" / "the big cats")

Spanish:
   Subject-verb agreement: extensive (all person/number combinations)
   Adjective-noun: in gender and number ("el gato negro" / "la gata negra")

German:
   Case agreement: nominative, accusative, dative, genitive
   Article agreement: gender + case + number

Russian:
   Verb agrees with subject in past tense gender too
```

Agreement checking must be **language-specific** — rules for English don't apply to Russian.

---

## Summary

```
Agreement checking = detect mismatches between
   words that must grammatically match.

Types:
   Subject-verb     → number, person
   Pronoun-antecedent → number, gender
   Tense consistency  → across clauses

How:
   POS tag → parse → check feature compatibility
   Modern tools use dependency parsing.

Used in:
   Grammar checkers, translation, language learning
```

> Agreement checking is one of the most practical applications of syntactic parsing — turning grammatical theory into useful corrections in tools millions of people rely on daily.
