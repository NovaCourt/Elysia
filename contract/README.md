# The contract

Every message between the pieces of Elysia -- the app, the local mechanics, the gateway, and the Court's servers -- is
described here, and nowhere else.

## Rules

- **One JSON Schema file per call type**, named `<call_type>.schema.json`.
- **Every schema carries a version.** The version goes up **only on a breaking change**. Adding an optional field is
  not breaking; removing or renaming a field, or changing what a field means, is.
- **Both sides validate at startup** and refuse to run, with a clear error, when their versions do not match.
- **A refusal is a first-class reply**, never an error: when the other side says no, the reply says so, why, and what
  to do instead.
- **The contract is the source of truth.** Code on either side is generated from it or checked against it.

## Call types

None yet. The first ones arrive one per pull request, each with its architecture note.
