# Maintenance guide

The source of truth for the index is [`data/reading-list.json`](../data/reading-list.json). The
README section between the generated-section markers is a rendered view of that file.

## Add an entry

1. Pick the category where a reader would look first. Add tags for the other parts of the physical
   loop that the work genuinely uses.
2. Use the canonical paper or project title, the earliest public publication year, and one stable
   URL. An arXiv abstract URL is preferable to a tracking link.
3. Write the note for a reader who has not seen the work. State the contribution and its relevance
   to physical systems in one sentence; avoid adjectives that are not supported by the paper.
4. Keep entries sorted by descending year and then by title (alphabetically within a year). The validator enforces this order.
5. Run `make check`, then open a pull request with the reason for the addition or correction.

## Review checklist

- Is the work about an agent that observes, reasons about, or acts in a physical or embodied
  environment?
- Is the link public and stable?
- Does the note describe the work rather than advertise it?
- Is the category and tag choice understandable to someone reading the neighboring entries?
- Does the addition duplicate an existing work, dataset, or version?

## Scope

The index is selective. We prioritize primary papers, public datasets, simulators, and reusable
software with enough documentation for independent readers. We do not maintain a leaderboard, make
claims about commercial products, or include a paper only because it mentions robots in passing.
When a work is corrected or superseded, keep the older entry when it provides useful historical
context and explain the relationship in the note or a pull request.
