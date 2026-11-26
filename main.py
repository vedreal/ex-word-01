"""One Word From Your Ex — entry program.

The bounty asks for exactly one word: the word your ex would use to
describe you, and nothing else. A judge model compares entries two at a
time and picks the funniest, most painfully honest word, weighing the
laugh and the sting of recognition together.

This program scores 10 fresh candidate words against the judge's own
brief, in the brief's criterion order, and writes the winner to
/output/entry.txt. The gate requires UTF-8 text of 1 to 24 characters,
not only white space, and exactly one word.
"""

import os

# --- Candidates -----------------------------------------------------------
# Each candidate: (word, rationale). Every word is a real word a person
# would actually say about a partner they once had — no phrases, no
# sentences, nothing off-subject. The rationale records why the word was
# considered, so the ranking below is checkable, not vibes.
CANDIDATES = [
    (
        "Practice",
        "The whole relationship was a rehearsal. 'You were practice' is "
        "the ex's most efficient insult: it says you were never the main "
        "event, only the warm-up for the person who came next. It stings "
        "because the entrant plainly knows it, and it lands as a joke "
        "because of the surprise turn — you thought you were the one, you "
        "were the trial run.",
    ),
    (
        "Almost",
        "He was almost the one, almost committed, almost enough. A single "
        "word that carries an entire failed relationship: the ex does not "
        "even need a sentence. It is elegant and painfully true, though it "
        "winces more than it laughs.",
    ),
    (
        "Placeholder",
        "You were never the one, only the seat kept warm until someone "
        "better arrived. Brutal and specific, but it leans on the sting "
        "more than the laugh, and it is a slightly colder, more formal "
        "word than an ex would say out loud.",
    ),
    (
        "Project",
        "She tried to fix him. 'He was a project' names the whole dynamic "
        "in one word: the renovation that never finished. Funny, true and "
        "deeply relatable — everyone has dated a project, or been one.",
    ),
    (
        "Buffering",
        "Always loading, never ready. The modern ex's word for a partner "
        "who kept promising and never delivered, frozen mid-sentence. "
        "Very funny on first hearing, but the sting is lighter — it is a "
        "tech joke first and a confession second.",
    ),
    (
        "Ghost",
        "He ghosted, or he was a ghost of a boyfriend: present in the "
        "room, absent everywhere it counted. Instantly understood, but "
        "the word is so common now that the surprise is gone.",
    ),
    (
        "Unread",
        "Left on read, as a person. The ex's word for someone whose "
        "messages — and feelings — were never opened. Clever and modern, "
        "but it reads more like a status than a description of a person.",
    ),
    (
        "Draft",
        "Like an unsent draft: never finished, never sent, abandoned in "
        "the folder. A good image, but quieter than its cousins — it "
        "suggests incompleteness without the punch of a verdict.",
    ),
    (
        "Fine",
        "The classic ex verdict: 'he's fine.' Damning with the faintest "
        "praise there is. It lands instantly and everyone has heard it, "
        "but the laugh is small — it is a shrug, not a punchline.",
    ),
    (
        "Roommate",
        "The relationship degraded until the lover became a flatmate who "
        "shared the rent and nothing else. Painfully true and relatable, "
        "but it names a situation rather than a person, and the joke "
        "needs a beat of explanation to land.",
    ),
]

# --- Rubric ---------------------------------------------------------------
# Weights follow the judge's brief, most important first:
#   1. exactly one word an ex would use to describe you   (weight 5)
#   2. makes me laugh out loud (surprise, sharp turn)      (weight 4)
#   3. stings with recognition, painfully true              (weight 3)
#   4. lands instantly, no explanation, irreplaceable       (weight 2)
#   5. relatable, the kind of word people repeat            (weight 1)
# Each criterion is scored 0-5. Maximum weighted total is 75.
WEIGHTS = (5, 4, 3, 2, 1)

# Scores, in the same criterion order as WEIGHTS, one row per candidate.
# Scored before any ranking, from the rationale above:
#   Practice   — ex would say it (5), laugh (5), sting (5), instant (4), relatable (4)
#   Almost     — ex would say it (5), laugh (4), sting (5), instant (5), relatable (5)
#   Placeholder— ex would say it (4), laugh (4), sting (5), instant (4), relatable (3)
#   Project    — ex would say it (5), laugh (4), sting (4), instant (4), relatable (5)
#   Buffering  — ex would say it (4), laugh (5), sting (3), instant (4), relatable (4)
#   Ghost      — ex would say it (5), laugh (3), sting (4), instant (5), relatable (4)
#   Unread     — ex would say it (4), laugh (4), sting (4), instant (4), relatable (4)
#   Draft      — ex would say it (4), laugh (3), sting (4), instant (4), relatable (3)
#   Fine       — ex would say it (5), laugh (3), sting (3), instant (5), relatable (4)
#   Roommate   — ex would say it (5), laugh (4), sting (4), instant (4), relatable (5)
SCORES = {
    "Practice": (5, 5, 5, 4, 4),
    "Almost": (5, 4, 5, 5, 5),
    "Placeholder": (4, 4, 5, 4, 3),
    "Project": (5, 4, 4, 4, 5),
    "Buffering": (4, 5, 3, 4, 4),
    "Ghost": (5, 3, 4, 5, 4),
    "Unread": (4, 4, 4, 4, 4),
    "Draft": (4, 3, 4, 4, 3),
    "Fine": (5, 3, 3, 5, 4),
    "Roommate": (5, 4, 4, 4, 5),
}


def weighted_total(word):
    """Weighted rubric total for one candidate word (max 75)."""
    return sum(w * s for w, s in zip(WEIGHTS, SCORES[word]))


def rank_candidates():
    """Rank all candidates: highest weighted total first.

    Ties go to the shorter word (fewer bytes), mirroring how the
    bounty breaks exact ties on judge win rate.
    """
    ranked = sorted(
        ((word, weighted_total(word)) for word, _ in CANDIDATES),
        key=lambda item: (-item[1], len(item[0].encode("utf-8"))),
    )
    return ranked


def write_entry(out_dir=None):
    """Pick the winner, validate it against the gate, write the entry.

    The gate: /output/entry.txt must be UTF-8 text of 1 to 24
    characters, not only white space, and exactly one word.
    """
    winner, total = rank_candidates()[0]
    text = winner.strip()
    if not (1 <= len(text) <= 24):
        raise ValueError(f"entry {text!r} is {len(text)} chars, gate needs 1-24")
    if not text or text != text.split()[0] or len(text.split()) != 1:
        raise ValueError(f"entry {text!r} is not exactly one word")
    text.encode("utf-8")  # must be valid UTF-8
    out_dir = out_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"Wrote {text!r} ({len(text)} chars) to {path}")
    return text


def main():
    ranked = rank_candidates()
    for word, total in ranked:
        print(f"{total:2d}  {word}")
    winner, winner_total = ranked[0]
    print(f"\nWinner: {winner!r} ({winner_total}/75)")
    write_entry()


if __name__ == "__main__":
    main()
