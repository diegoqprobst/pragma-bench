# Palo Alto Bench: Can Frontier LLMs Detect Symmetrical Escalation and Double Binds, and Produce Valid Reframes?

**A Bilingual (Spanish/English) Benchmark for Relational Pragmatics**

Diego Quinde
diegoaquinde@gmail.com

> **Estado del manuscrito:** borrador pre-resultados. Las secciones 1–6, 8.2, 9–11 están completas; los bloques marcados `[RESULTS]` se llenan tras la corrida confirmatoria preregistrada. Citas del related work **verificadas 2026-07-07** contra fuente primaria (ver [docs/citas-verificadas.md](../docs/citas-verificadas.md)); queda un único `[VERIFY-CITE]` opcional en §1.

---

## Abstract

Large language models are increasingly used in emotionally loaded conversations — as companions, coaches, and informal counselors. These uses assume a capability that has never been directly measured: understanding the *relational pragmatics* of a conversation, i.e., what an exchange is doing between two people, over and above what either of them is saying. We introduce **Palo Alto Bench**, a bilingual (Spanish/English) benchmark grounded in the interactional theory of the Palo Alto school (Bateson, Watzlawick), which evaluates three capabilities over short expert-authored dialogues: (1) **detecting** symmetrical escalation and double binds, (2) **localizing** their internal structure (primary injunction, contradictory secondary injunction, metacommunication block), and (3) **producing valid reframes**, scored against the five validity criteria of Watzlawick, Weakland and Fisch. Items never name the constructs; adversarial distractors (commentable contradictions, repaired conflicts, flexible complementarity) measure over-detection. All items exist as culturally-native Spanish/English parallel pairs, isolating the cross-lingual gap. Against [N] frontier models under a preregistered protocol (OSF: [DOI]), we find [RESULTS: headline finding 1], [RESULTS: headline finding 2], and [RESULTS: headline finding 3]. Dataset, prompts, code, raw outputs, and both human and LLM judge scores are released openly.

**Keywords:** benchmark evaluation, pragmatics, systemic therapy, double bind, reframing, cross-lingual evaluation, LLM-as-judge

---

## 1. Introduction

A person tells a chatbot: *"My mother asks me to hug her, then stiffens and says a real hug should come on its own — and when I point this out, she says a good son doesn't argue."* Whether the model recognizes what is happening here — not sadness, not conflict, but a specific interactional trap with a specific structure — determines whether its response helps, soothes generically, or reinforces the trap.

Current evaluations of LLMs in psychologically sensitive settings measure symptom and risk classification (the CLPsych shared-task series, 2014–present), empathy expression (Sharma et al., 2020), counseling-response quality (Liu et al., 2021), or fidelity of simulated patients for training (Wang et al., 2024). All of these treat the *individual* as the unit of analysis and the *content* of utterances as the signal. But a founding insight of the systemic tradition in psychotherapy is that much psychological suffering lives not in individuals but in **interaction patterns**: self-reinforcing loops with an internal structure that is invisible at the level of any single message (Watzlawick, Beavin & Jackson, 1967). A model that reads content but not pattern will misread precisely the conversations where stakes are highest.

We ask a direct question: **can frontier LLMs see interaction patterns?** We operationalize it through three constructs from the Palo Alto school, chosen because they are (a) precisely defined in the source literature, (b) structurally diagnosable from short dialogue excerpts, and (c) consequential — each has a known clinical intervention whose misapplication causes harm:

1. **Symmetrical escalation** — a positive feedback loop in which each turn matches and outbids the other (Watzlawick et al., 1967);
2. **Double bind** — contradictory injunctions across logical levels, plus a block on escaping or commenting (Bateson, Jackson, Haley & Weakland, 1956);
3. **Reframing** — the therapeutic response to both: changing the conceptual frame of a situation so that the same facts acquire a workable meaning (Watzlawick, Weakland & Fisch, 1974).

The first two test *recognition* at increasing depth (label → structure); the third tests *production* of an intervention, scored against explicit validity criteria rather than judge taste.

**Why bilingual.** Clinical NLP evaluation is overwhelmingly monolingual English — the anchor datasets above are all English-language [VERIFY-CITE: multilingual-gap survey, optional reinforcement]. Yet the deployment reality of emotionally loaded LLM use is massively multilingual, and Spanish is among the largest deployment languages with the least evaluation coverage. Every Palo Alto Bench item is authored as a **parallel pair**: same phenomenon, same turn structure, culturally native wording in each language. This makes the cross-lingual gap a measured quantity rather than an anecdote.

**Why these failure modes matter.** Our design targets two specific risks. *Over-detection*: a model that finds pathology wherever it looks — measured with adversarial `none` items (a demanding but commentable request; a conflict that repairs; a one-off helpful asymmetry) and a neutral-vs-guided prompt manipulation. *Invalid reframes*: responses that sound therapeutic while being positivity, advice, or minimization — measured with a five-axis rubric derived directly from Watzlawick's validity criteria, with disqualification flags for each failure mode.

**Contributions.**
1. The first benchmark (to our knowledge) operationalizing systemic-interactional constructs — symmetrical escalation, double bind (with its component structure), complementary rigidity, and valid reframing — for LLM evaluation.
2. A bilingual parallel-pair design with expert-authored items that never name their constructs, plus adversarial distractors calibrated to each construct's nearest confusable neighbor.
3. A preregistered evaluation of [N] frontier models (OSF: [DOI]) with a human-expert-calibrated LLM judge for the generative task.
4. Full open release: items, gold annotations, frozen prompts, runner, raw model outputs, and judge scores.

## 2. Theoretical Background

### 2.1 Interaction, not individuals

The Palo Alto school reframed psychopathology as communication: the unit of analysis is the ongoing exchange, whose regularities ("rules of the game") persist independently of the participants' intentions (Watzlawick et al., 1967). Two properties of communication drive our constructs. First, every message carries **content** and a **relationship claim** (how the sender defines the relation); pathology often lives in the second channel. Second, relations are **symmetrical** (based on equality — partners mirror each other) or **complementary** (based on difference — one-up/one-down); both are healthy when flexible and pathological when rigid or runaway.

### 2.2 Symmetrical escalation

When both parties claim the same relational position, each turn that asserts it invites a matching-and-exceeding counter-assertion: a positive feedback loop with no internal brake (Watzlawick et al., 1967, ch. 3). Operationally we require: (i) same claimed position, (ii) mirror-and-outbid turn structure, (iii) monotone intensification without repair. The nearest confusables — which our distractors instantiate — are *complementary rigidity* (stable unequal roles: pursuer/withdrawer, over-/under-functioning), *simple disagreement* (opposition without amplification), and *repaired conflict* (escalation that de-escalates).

### 2.3 Double bind

Bateson et al. (1956) specify ingredients: an intense relationship; a primary negative injunction; a secondary injunction contradicting the first **at a more abstract logical level**; a tertiary injunction prohibiting escape from the field; and (once the pattern is learned) the inability to comment on the contradiction. The victim cannot win, cannot not respond, and cannot say so.

We annotate three **textually localizable components** per item: `primary_injunction`, `secondary_injunction`, `no_metacommunication`. Field inescapability — Bateson's tertiary injunction — is structural (a son, an employee, a dependent partner cannot simply leave) and rarely verbalized; forcing it into dialogue would make items artificial. We therefore document it as an item-level precondition (`field_inescapability`) rather than a turn to localize.

We further distinguish two subtypes, reported separately: **`logical_type`** binds, where the secondary injunction targets the *quality or motivation* of the demanded act itself (the canonical "be spontaneous" paradox: *hug me — but only if it comes on its own*); and **`pragmatic_paradox`** binds, where the contradiction, inescapability, and comment-block are all present but the level-crossing is not clean in Russellian terms (*take initiative — but everything is approved through me first*). The subtype contrast turns a definitional dispute into an empirical result: models may detect the laboratory-pure bind and miss the ecological one, or vice versa.

### 2.4 Valid reframing

Reframing is "to change the conceptual and/or emotional setting or viewpoint in relation to which a situation is experienced and to place it in another frame which fits the 'facts' of the same concrete situation equally well or even better, thereby changing its entire meaning" (Watzlawick et al., 1974, ch. 8). From the source criteria we derive five scoring axes: (1) **fit to the facts**, (2) **frame change** (not paraphrase), (3) **irreversibility** (the old frame is hard to reinhabit), (4) **assimilability** (fits the recipient's language and worldview), (5) **behavioral opening** (interrupts the problem-maintaining pattern). Crucially, the tradition is explicit about what reframing is *not*: positive thinking, denial, direct advice, causal-historical interpretation. These become disqualification flags.

## 3. Related Work

**Mental-health and counseling NLP.** Existing work targets the individual and the utterance: risk and symptom classification over user text (the CLPsych workshop series and its shared tasks, ACL, 2014–present), empathy expression in support conversations (Sharma, Miner, Atkins & Althoff, 2020), strategy-annotated emotional-support dialogue (ESConv; Liu et al., 2021), and simulated patients for clinician training (PATIENT-Ψ; Wang et al., 2024). Palo Alto Bench differs on the unit of analysis — the interaction pattern, not the individual — and on scoring generation against construct-derived validity criteria rather than preference or strategy labels.

**Pragmatics evaluation for LLMs.** Existing pragmatics benchmarks test single-utterance inference: implicature resolution (Ruis et al., 2022) and a battery of seven pragmatic phenomena compared against human judgments (Hu et al., 2023). Our constructs are irreducibly *dyadic and multi-turn* — the signal is a property of the loop between speakers, not of any utterance, and the double bind specifically requires tracking contradiction across message levels over turns.

**Sycophancy and over-diagnosis.** Sharma et al. (2023) show state-of-the-art assistants consistently bend toward what prompts suggest. Our neutral-vs-guided manipulation measures a clinical variant of this failure: does naming pathologies make the model find them where there are none? (H3).

**LLM-as-judge.** Zheng et al. (2023) establish both the practice of validating LLM judges against human preferences and the biases that make uncalibrated judging unsafe (position, verbosity, self-enhancement). We adopt calibration against a human expert with a preregistered κ threshold, plus an anti-self-preference constraint: the judge never scores outputs of its own generator family without this being reported.

## 4. The Benchmark

### 4.1 Items

Each item is a short dialogue (2–6 turns, with optional nonverbal stage directions carrying the metacommunicative channel), a relational register (couple, family, workplace, clinical, friendship), gold labels, structural annotation, and — where applicable — reframing materials (presenting problem, reference reframes each tagged with a distinct systemic technique, anti-examples). The full JSON schema ships with the dataset.

Three design rules are enforced by validation scripts:

1. **No construct leakage.** Dialogues never contain theory terms in either language. A model that has memorized "double bind" gains nothing; the pattern must be read off the interaction.
2. **Parallel pairs.** Every concept exists as ES and EN versions sharing `pair_id` and turn structure, each written natively (names, idiom, register), never translated literally.
3. **Distractors that bite.** Every `none` item is a near-miss of a specific construct (`distractor_of`), failing exactly one criterion: a double demand that is *commentable and adjusted when named*; a reproach met with *immediate repair*; a *one-off, role-flexible* helping exchange.

### 4.2 Seed set and evaluation set

A frozen seed set of 15 pairs (30 stimuli; 5 escalation / 4 double bind, balanced across subtypes / 3 complementary rigidity / 3 none) anchors the annotation guide and calibrates the judge; it is excluded from confirmatory analysis. The evaluation set (≥120 concepts, ≥240 stimuli; composition preregistered, including ≥15% clinical register and ~25% `none`) is authored after preregistration and before any evaluated model is run.

### 4.3 Tasks

**Task A — Detection.** *Neutral condition:* "Do you observe any problematic communication pattern? YES/NO + explain." *Guided condition:* closed multi-label choice over the four classes, presented with one-line operational glosses, order randomized per item. The pair of conditions separates spontaneous detection from prompted detection and yields the over-detection contrast (H3).

**Task B — Localization.** The model is told, in operational terms (never the theory name), what pattern the dialogue contains, and must return its structure as JSON: the three double-bind components with turn indices and quotes, or the escalation curve's turn indices plus the contested position. Scoring: exact turn = 2, adjacent = 1, absent/hallucinated = 0 (double bind); Jaccard over turn sets (escalation).

**Task C — Reframe production.** Without any label, the model is asked for "a different way of understanding the situation that fits the concrete facts as well or better, changes the meaning of what is going on, and opens new ways out — without giving advice or minimizing." The theoretical term is deliberately absent from the instruction, so the task measures the capability, not retrieval of the recipe's name.

### 4.4 Scoring Task C: calibrated judging

Each generated reframe is scored 1–4 on the five axes by (a) the human expert (clinical training in systemic therapy; blind to model identity, randomized order) on the seed set, and (b) a fixed LLM judge — never the generator under evaluation — using the identical rubric prompt with reference reframes explicitly framed as *non-exhaustive examples of distinct techniques, not templates to match*. The judge scales to the full set only if quadratic-weighted κ against the human is ≥ 0.60 on ≥ 4 of 5 axes (one prompt-iteration permitted, recalibrating on the seed set); otherwise the human scores everything. A reframe is **valid** iff axes 1, 2, 5 ≥ 3 and axes 3, 4 ≥ 2 (threshold frozen 2026-06-30, preregistered).

## 5. Experimental Setup

**Models.** [N] frontier models pinned by exact version at run time (run manifest published): [RESULTS: model table]. Temperature 0 (or provider minimum); n = 3 repetitions for Tasks A/B (majority vote; ties = error), single generation for Task C.

**Prompts.** Frozen pre-registration in `runner/prompts/v1.json`; every raw output stores the SHA-256 of its exact prompt.

**Failure handling (preregistered).** Refusals count as incorrect/invalid and are reported separately; malformed JSON gets one format-reminder retry then counts as incorrect; API errors retry ×3 then the item is excluded and reported (>5% exclusions ⇒ model flagged as partial evaluation).

**Statistics.** 95% CIs via nonparametric bootstrap (B = 10,000) resampling by `pair_id`; H2 via exact McNemar on ES/EN paired accuracy (Task A) and Wilcoxon signed-rank on item-level rubric means (Task C); H3 via McNemar on paired FP outcomes (guided vs. neutral) per `none` item; Holm correction across models within each hypothesis. Full plan: OSF preregistration [DOI].

## 6. Hypotheses

Preregistered, directional (see OSF [DOI] for operationalization):

- **H1.** Double-bind detection F1 < symmetrical-escalation detection F1 (multilevel reasoning is harder than curve-shape recognition).
- **H2.** Spanish performance < English on at least one task, within parallel pairs.
- **H3.** False-positive rate on `none` items is > 0 under guided prompting, and higher guided than neutral (clinical sycophancy).
- **H4.** Valid-reframe rate < detection rate on the same items (production lags recognition).

Exploratory: `logical_type` vs. `pragmatic_paradox` gap; component hallucination rates in Task B; register effects; escalation↔rigidity confusion structure.

## 7. Results

`[RESULTS — se llena tras la corrida confirmatoria; estructura fijada de antemano]`

### 7.1 Detection (Task A)
Table 1: macro-F1 and per-class F1, per model × language × condition. Figure 1: confusion structure. Key cells: `double_bind` vs `symmetrical_escalation` F1 (H1); FP-rate on `none`, neutral vs guided (H3).

### 7.2 Localization (Task B)
Table 2: normalized component scores (double bind, by subtype) and turn-Jaccard (escalation), per model × language. Component hallucination rates.

### 7.3 Reframe production (Task C)
Judge calibration: κ per axis, human vs LLM judge, seed set. Table 3: % valid reframes and per-axis means, per model × language; flag distribution (which failure mode dominates: advice? positivity? minimization?). H4 contrast.

### 7.4 Cross-lingual gap
Paired ES−EN deltas across all three tasks (H2), with McNemar/Wilcoxon results.

## 8. Discussion

### 8.1 `[RESULTS-dependent interpretation]`

*(Ramas pre-escritas según el patrón de resultados, para redactar con honestidad sea cual sea el desenlace:)*
- If H1 holds: recognition of relational pathology degrades exactly where multilevel (content-vs-metacommunication) reasoning is required — the signature capability gap this benchmark was built to expose.
- If H3 holds: naming pathologies to a model makes it find them — a deployment-relevant risk for any "screening" use of LLMs, and a quantified instance of sycophancy in a clinical frame.
- If H4 holds: models can name the trap but not reframe it — supporting a "describe, don't intervene" boundary for unsupervised use.
- If Spanish lags (H2): the languages where LLMs are most used for emotional support are not the languages where they are safest.

### 8.2 What this benchmark cannot say

Palo Alto Bench measures pattern recognition and single-shot intervention quality over synthetic vignettes. It does not measure therapeutic outcome, multi-session skill, or safety in deployment; a high score licenses none of those claims. The constructs themselves carry historical caveats — the double-bind theory of schizophrenia is not an etiological claim we endorse; we use the *communication-structural* definitions, which stand independently of the etiological hypothesis.

## 9. Limitations

(i) Synthetic expert-authored items: strong confound control, reduced ecological realism; a subsample inspired by anonymized real transcripts is future work. (ii) **Single expert annotator** (the author) for gold labels and human judging: no inter-annotator κ is reportable; the full annotation guide is public precisely so others can replicate the labels, and a second clinical annotator is the highest-value extension. (iii) LLM-judge bias: mitigated by calibration, anti-self-preference and anti-template instructions, not eliminated. (iv) Results are version-pinned snapshots.

## 10. Ethics Statement

This is an evaluation instrument, not a clinical tool. Nothing here validates LLMs as therapists; if anything, the benchmark exists to give precise content to claims of *incapacity*. Vignettes are fictional; no patient data is used. Model-generated reframes are published with model attribution so that failure modes are inspectable. We note a dual-use consideration: descriptions of double-bind structure could in principle be misused as a manipulation recipe; the structures described have been public in the clinical literature for seventy years, and the benchmark adds detection capability, not technique.

## 11. Data and Code Availability

Items, gold annotations, frozen prompts, runner and scoring code, raw model outputs, judge scores (human and LLM), and the preregistration are available at github.com/diegoqprobst/pragma-bench (code MIT, data CC BY 4.0) and OSF [DOI].

## References

*(Todas verificadas contra fuente primaria — detalle y enlaces en [docs/citas-verificadas.md](../docs/citas-verificadas.md).)*

- Bateson, G., Jackson, D. D., Haley, J., & Weakland, J. (1956). Toward a theory of schizophrenia. *Behavioral Science*, 1(4), 251–264.
- Hu, J., Floyd, S., Jouravlev, O., Fedorenko, E., & Gibson, E. (2023). A fine-grained comparison of pragmatic language understanding in humans and language models. *Proceedings of ACL 2023*, 4194–4213. arXiv:2212.06801.
- Liu, S., Zheng, C., Demasi, O., Sabour, S., Li, Y., Yu, Z., Jiang, Y., & Huang, M. (2021). Towards emotional support dialog systems. *Proceedings of ACL 2021*. arXiv:2106.01144.
- Ruis, L., Khan, A., Biderman, S., Hooker, S., Rocktäschel, T., & Grefenstette, E. (2022). Large language models are not zero-shot communicators. arXiv:2210.14986.
- Sharma, A., Miner, A. S., Atkins, D. C., & Althoff, T. (2020). A computational approach to understanding empathy expressed in text-based mental health support. *Proceedings of EMNLP 2020*, 5263–5276. arXiv:2009.08441.
- Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., et al. (2023). Towards understanding sycophancy in language models. *ICLR 2024*. arXiv:2310.13548.
- Wang, R., Milani, S., Chiu, J. C., et al. (2024). PATIENT-Ψ: Using large language models to simulate patients for training mental health professionals. *Proceedings of EMNLP 2024*. arXiv:2405.19660.
- Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967). *Pragmatics of Human Communication: A Study of Interactional Patterns, Pathologies, and Paradoxes*. New York: W. W. Norton.
- Watzlawick, P., Weakland, J. H., & Fisch, R. (1974). *Change: Principles of Problem Formation and Problem Resolution*. New York: W. W. Norton.
- Workshop on Computational Linguistics and Clinical Psychology (CLPsych). *Proceedings*, Association for Computational Linguistics, 2014–present. aclanthology.org/venues/clpsych.
- Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems 36* (Datasets and Benchmarks). arXiv:2306.05685.

*(Único marcador restante: [VERIFY-CITE: multilingual-gap survey] en §1 — refuerzo opcional, no bloqueante.)*
