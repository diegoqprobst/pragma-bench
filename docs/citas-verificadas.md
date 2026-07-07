# Citas verificadas — Palo Alto Bench

> Política: **ninguna cita entra al paper sin verificar contra fuente primaria.**
> Verificación: 2026-07-07 (búsqueda web + arXiv/ACL Anthology). Cada entrada: cita completa, ancla verificada y para qué sección del paper sirve.

## Clásicos fuente (verificados desde el inicio)

1. **Bateson, G., Jackson, D. D., Haley, J., & Weakland, J. (1956).** Toward a theory of schizophrenia. *Behavioral Science*, 1(4), 251–264. — §2.3 (doble vínculo).
2. **Watzlawick, P., Beavin, J. H., & Jackson, D. D. (1967).** *Pragmatics of Human Communication*. W. W. Norton. — §2.1–2.2.
3. **Watzlawick, P., Weakland, J. H., & Fisch, R. (1974).** *Change: Principles of Problem Formation and Problem Resolution*. W. W. Norton. — §2.4 (reencuadre).

## Related work — verificadas 2026-07-07

### Mental-health / counseling NLP (§1, §3)

4. **Sharma, A., Miner, A. S., Atkins, D. C., & Althoff, T. (2020).** A Computational Approach to Understanding Empathy Expressed in Text-Based Mental Health Support. *EMNLP 2020*, 5263–5276. arXiv:2009.08441. ✓ [ACL Anthology 2020.emnlp-main.425](https://aclanthology.org/2020.emnlp-main.425/) — ancla de "empathy detection"; marco EPITOME, RoBERTa bi-encoder.
5. **Liu, S., Zheng, C., Demasi, O., Sabour, S., Li, Y., Yu, Z., Jiang, Y., & Huang, M. (2021).** Towards Emotional Support Dialog Systems. *ACL 2021*. DOI 10.18653/v1/2021.acl-long.269. arXiv:2106.01144. ✓ [ACL Anthology](https://aclanthology.org/2021.acl-long.269/) — ESConv; ancla de "counseling-response quality"; estrategias de Helping Skills Theory.
6. **Wang, R., Milani, S., Chiu, J. C., et al. (2024).** PATIENT-Ψ: Using Large Language Models to Simulate Patients for Training Mental Health Professionals. *EMNLP 2024* (main). arXiv:2405.19660. ✓ [ACL Anthology 2024.emnlp-main.711](https://aclanthology.org/2024.emnlp-main.711/) — pacientes simulados sobre modelos cognitivos CBT; el individuo como unidad.
7. **CLPsych — Workshop on Computational Linguistics and Clinical Psychology** (ACL, anual desde 2014; shared tasks de riesgo suicida 2019, cambios de ánimo 2022, etc.). ✓ [ACL Anthology venue](https://aclanthology.org/venues/clpsych/) — ancla de la línea clasificación-de-riesgo/síntoma sobre texto del individuo.

### Evaluación de pragmática en LLMs (§3)

8. **Hu, J., Floyd, S., Jouravlev, O., Fedorenko, E., & Gibson, E. (2023).** A fine-grained comparison of pragmatic language understanding in humans and language models. *ACL 2023*, 4194–4213. DOI 10.18653/v1/2023.acl-long.230. arXiv:2212.06801. ✓ [ACL Anthology](https://aclanthology.org/2023.acl-long.230/) — 7 fenómenos pragmáticos, enunciado único; contraste perfecto con nuestro objeto diádico multi-turno.
9. **Ruis, L., Khan, A., Biderman, S., Hooker, S., Rocktäschel, T., & Grefenstette, E. (2022).** Large language models are not zero-shot communicators. arXiv:2210.14986. ✓ [arXiv](https://arxiv.org/abs/2210.14986) — implicaturas conversacionales; presentado en NeurIPS. ⚠ Nota: la versión NeurIPS 2023 pudo publicarse retitulada; **citar la versión arXiv verificada** salvo confirmación del título de actas.

### Sicofancia (§3, H3)

10. **Sharma, M., Tong, M., Korbak, T., Duvenaud, D., Askell, A., Bowman, S. R., et al. (2023).** Towards Understanding Sycophancy in Language Models. *ICLR 2024*. arXiv:2310.13548. ✓ [arXiv](https://arxiv.org/abs/2310.13548) — 5 asistentes SOTA muestran sicofancia consistente; base de nuestra "sicofancia clínica" (H3).

### LLM-as-judge (§3, §4.4)

11. **Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023).** Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *NeurIPS 36* (Datasets and Benchmarks). arXiv:2306.05685. ✓ [arXiv](https://arxiv.org/abs/2306.05685) — verificación de acuerdo juez-LLM↔humano; sesgos de posición/verbosidad/auto-preferencia → justifica nuestra calibración κ y la restricción anti-autopreferencia.

## Pendientes (si el texto final las necesita)

- Survey que soporte "clinical NLP evaluation is overwhelmingly monolingual English" — el claim es defendible por inspección de los datasets ancla (todos EN o ZH), pero un survey multilingüe de NLP clínico lo blindaría. Marcador `[VERIFY-CITE: survey]` se mantiene en §1 hasta encontrarlo.
- Theory-of-mind eval (opcional para §3): se retiró la mención para no citar sin verificar; re-añadir solo con ancla verificada.
