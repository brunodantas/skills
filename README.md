# brunodantas/skills

A small companion collection of [Agent Skills](https://agentskills.io) that extends
[mattpocock/skills](https://github.com/mattpocock/skills). It is a peer dependency, not a
fork: install it alongside upstream and the two sets interlock.

```bash
npx skills@latest add brunodantas/skills
```

## Skills

| Skill | What it does |
|---|---|
| [`ilities`](skills/ilities/SKILL.md) | Elicit, rank, and document a project's architectural characteristics into `docs/architecture.md`. |

More to land before `0.1.0`: `to-tests` (frozen-oracle test writing), `build-pr` (tiered PR
descriptions), and `setup-brunodantas-skills` (the one-time config skill).

## Non-duplication policy

No skill here shadows the name of a promoted upstream skill. If upstream absorbs an idea from
this collection, the local skill is deprecated with a pointer rather than maintained in
parallel.

## Status

Pre-release. The README's peer-dependency detail (upstream skills referenced, upstream version
tested against) is filled in at `0.1.0`.

## License

MIT. See [LICENSE](LICENSE).
