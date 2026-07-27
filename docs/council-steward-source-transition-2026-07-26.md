# Council Steward Source Transition — 2026-07-26

**Transition ID:** `EC-STEWARD-SOURCE-TRANSITION-2026-07-26-06`

**State:** `approved — sealing and verification authorized; runtime
notification and release held`

**Decision authority:** System Engineer

**Decision source:** System Engineer selection `A. Approve exact v6
implementation through sealed-and-verified, but require a later decision before
runtime notification`, 2026-07-26

**Named executor:** Chief Executive

## Purpose

Seal a current, bounded source packet for the active Council Steward pilot
without notifying the runtime, releasing the packet, expanding the pilot term,
or granting new action authority.

This transition reconciles the five-position Council state, the current Grace
Gems routing card, and three explicitly classified project artifacts. It does
not adopt a Steward finding or authorize a project correction.

## Predecessor state

- Predecessor manifest:
  `docs/council-steward-source-manifest-2026-07-24-v5.json`;
- predecessor ID: `EC-STEWARD-SOURCE-2026-07-24-05`;
- predecessor file count: `476`;
- predecessor aggregate SHA-256:
  `63B2793D292EB0B7DFF2A0AAE7D5021C595D8E0E9200AA49E31B8D322E27F82A`;
- predecessor state: `sealed and verified — unreleased`;
- latest released source-manifest identity: `Missing` from repository evidence.

Do not infer release from sealing, pilot activation, runtime existence, prior
discussion, or elapsed time.

## Successor identity

- Successor manifest:
  `docs/council-steward-source-manifest-2026-07-26-v6.json`;
- successor ID: `EC-STEWARD-SOURCE-2026-07-26-06`;
- authorized repository HEAD:
  `ec615907423df0b5ede0e9c665ca1c657cc21e43`;
- authorized tree:
  `8e7a1424635dbe4d7c268a6f181ab7d56601f0dc`;
- file count and aggregate SHA-256: controlled only by the generated successor
  manifest after successful verification;
- maximum state authorized by this receipt:
  `sealed and verified — unreleased`.

Any HEAD mismatch or unexpected change to an authorized canonical or
`projects/` source returns this transition to `held`.

## Source boundary

The source categories remain:

- the canonical sources named by the manifest builder, including this
  transition receipt;
- Git-tracked and untracked non-ignored regular files under `projects/`;
- no private or external system.

The following current project artifacts are explicitly classified:

| Source | Classification |
| --- | --- |
| `projects/commercial-hypotheses.md` | `included-current — noncontrolling hypothesis` |
| `projects/singularity-science/README.md` | `included-current — derived index` |
| `projects/singularity-science/visual-training-technical-brief.md` | `included-current — provisional research` |

Coverage limits:

- commercial-offer documents under `docs/analysis/` are
  `omitted — source expansion not authorized`;
- the operator-supplied visual-training transcript is
  `unavailable — no repository path or hash`;
- Photon-1 primary technical evidence and independent replication are
  `unavailable`;
- `tmp/`, private systems, external applications, and other sources outside
  the exact canonical and `projects/` surface are excluded.

Inclusion establishes source visibility only. It does not approve a
commercial offer, research claim, model change, deployment, publication,
customer action, or doctrine.

## Unchanged runtime boundary

The active pilot remains governed by
`EC-STEWARD-ACTIVATION-2026-07-24-01` and expires on 2026-08-23 unless earlier
paused or revoked.

This transition does not authorize:

- runtime notification or source release;
- Council Steward content access to v6;
- a new runtime, model, tool, permission, term, or persistence boundary;
- private-system or external access;
- strategy, correction, execution, delegation, communication, spending, or
  publication;
- changes to historical manifests or activation receipts;
- access to omitted or unavailable evidence.

## Sealing and verification

The named executor may:

1. confirm the authorized HEAD, tree, and in-scope status;
2. run the canonical validator and privacy checks;
3. generate the successor manifest at the exact path and ID;
4. verify its path set, file hashes, byte counts, aggregate hash, and file
   count against the unchanged authorized source surface;
5. record the objective result outside the sealed source packet.

After generation, no authorized source may change before verification
completes. Any mismatch, validation failure, unexpected in-scope path,
credential exposure, or privacy concern requires `Hold`.

## Release gate

Successful verification leaves v6 `sealed and verified — unreleased`.

A later System Engineer decision must separately authorize notification to the
named runtime. Release requires an attributable runtime response containing:

- runtime identity;
- this transition ID;
- successor manifest ID and path;
- file count and aggregate SHA-256 copied from the verified manifest;
- pilot expiration;
- `ACCEPT` or `HOLD`;
- effective timestamp.

The runtime must verify these values before reading source content. No response,
unavailable runtime, identity mismatch, value mismatch, or ambiguous state
keeps v6 unreleased.

## Authority header

**Proposed by:** Chief Executive  
**Recommended by:** Chief Executive  
**Approved by:** System Engineer, 2026-07-26  
**Executed by:** Chief Executive for sealing and verification only  
**Authority scope:** exact v6 source sealing and verification; no notification
or release  
**Evidence required:** canonical validation, privacy pass, generated manifest,
successful manifest verification, unchanged in-scope source state, and
objective reconciliation record

> This receipt authorizes a sealed candidate source packet. It does not release
> that packet to the Council Steward runtime.
