# Taxonomy

Physical-RSI uses a deliberately small taxonomy. A paper can carry several tags, but each entry
has one home category so that the index remains easy to browse.

## Reasoning

Reasoning covers goals, language grounding, planning, task decomposition, and the use of tools or
programs. It asks what the system should do and how it chooses the next step.

## Sensing

Sensing covers visual perception, geometry, state estimation, scene representations, and the
uncertainty that comes with incomplete observations. It asks what the system can know about the
world at decision time.

## Interaction

Interaction covers action generation, control, manipulation, navigation, and feedback. It asks how
a decision changes the world and how the system responds when the result differs from the plan.

## Cross-cutting categories

- **Foundations** follows models that connect multiple modalities or embodiments.
- **Learning policies and control** follows the algorithms that produce executable behavior.
- **Language, planning, and tool use** follows high-level grounding and closed-loop planning.
- **Perception and world models** follows representations used to estimate or predict the world.
- **Simulation and environments** follows repeatable physical testbeds.
- **Datasets and benchmarks** follows shared data and evaluation protocols.
- **Safety, evaluation, and deployment** follows constraints, robustness, and real-world evidence.

The categories are not a claim that a paper belongs to only one part of the loop. They are an
editorial choice that makes the relationships visible without flattening them into one score.
