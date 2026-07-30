# Contradiction Preflight Transplant Kit

This kit adds a deterministic, read-only contradiction check to an agentic
coding repository. It compares normalized request assertions with explicitly
supplied controlling facts before an agent asks a consequential question or
acts on a potentially superseding assumption.

The kernel does not search repository prose, choose which source governs,
write files, open a database, grant authority, or correct durable state.

## Install

1. Copy this directory into the destination repository.
2. Add `PyYAML>=6.0` to the destination runtime.
3. Edit `host_policy.py`:
   - declare the destination consequence vocabulary;
   - declare allowed and controlling authority roles;
   - replace or extend the example privacy scanner.
4. Wire `contradiction_check.py` into the destination CLI or invoke it
   directly.
5. Add the bounded workflow in `AGENT_CONTRACT.md` to the destination agent
   contract and Elicitation instructions.
6. Run:

   ```text
   python -m unittest discover -s tests
   python contradiction_check.py --packet contradiction-packet.example.yaml --format json
   ```

## Host boundary

The destination repository—not the kernel—must decide which facts and sources
qualify as controlling. The caller must normalize the smallest relevant
assertion set and supply source references. Do not turn the checker into a
semantic repository scanner.

The default host policy preserves the source protocol vocabulary. It is an
example, not authority for another repository.

## Generated provenance

`contradiction_kernel/` is generated from the canonical Anyang kernel.
`MANIFEST.json` records source identity and hashes. Do not edit the generated
kernel copy directly; update the canonical source and rebuild the kit.

In Anyang Intelligence:

```text
python tools/build_contradiction_preflight_kit.py
python tools/build_contradiction_preflight_kit.py --verify
```
