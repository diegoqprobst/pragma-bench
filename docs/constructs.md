# Constructos: definiciones operacionales y criterios de validez

Este documento fija qué cuenta como cada fenómeno. Es la fuente de verdad para anotar ítems (gold labels) y para puntuar respuestas. Cada constructo trae: (a) el anclaje teórico, (b) la definición operacional usada para etiquetar, (c) los rasgos de superficie que **sí** lo indican, (d) los confusores que **no** lo son (base para los distractores).

> Principio transversal: **las viñetas nunca nombran el constructo**. Si el diálogo dice "esto es un doble vínculo" o "estás escalando", el modelo resuelve por léxico, no por pragmática. Las etiquetas viven solo en la anotación, nunca en el estímulo.

---

## 1. Escalada simétrica (symmetrical escalation)

**Anclaje.** Watzlawick, Beavin & Jackson (1967), *Pragmatics of Human Communication*, cap. 3. Las relaciones son **simétricas** (basadas en igualdad / reflejo de la conducta del otro) o **complementarias** (basadas en la diferencia: una posición *up* y otra *down*). La escalada simétrica es un bucle de retroalimentación positiva donde cada participante responde igualando-y-superando la conducta del otro ("tú subes la voz, yo la subo más"), sin mecanismo de de-escalada. Patológica cuando es descontrolada (*runaway*).

**Definición operacional (para etiquetar como `symmetrical_escalation`):**
1. Los participantes ocupan la **misma posición** relacional (ninguno cede el rol *up*/*down*; compiten por la misma).
2. Cada turno **refleja y amplifica** el turno previo del otro (más volumen, más acusación, más amenaza, "ojo por ojo" creciente).
3. Hay **tendencia monotónica al alza**: el intercambio se intensifica turno a turno; no aparece reparación ni de-escalada.

**Rasgos de superficie que lo indican:** tit-for-tat ("ah, ¿yo?, pues tú..."), simetría especular de actos de habla (reproche↔reproche, amenaza↔amenaza), "uno-más" competitivo, ausencia de meta-comunicación reparadora.

**Confusores (NO son escalada simétrica → sirven de distractores):**
- **Rigidez complementaria**: uno persigue / otro se retira, posiciones *desiguales* y estables (no se reflejan; ver §3). Etiqueta `complementary_rigidity`.
- **Desacuerdo simple**: dos turnos en oposición pero **sin amplificación** ni curva ascendente. Etiqueta `none`.
- **Escalada que de-escala**: empieza a subir pero un participante repara/cede → no es *runaway*. Etiqueta según resultado (a menudo `none`).

---

## 2. Doble vínculo (double bind)

**Anclaje.** Bateson, Jackson, Haley & Weakland (1956), "Toward a Theory of Schizophrenia", *Behavioral Science* 1(4), 251–264. Los **ingredientes** del doble vínculo:
1. Dos o más personas en una **relación intensa** de alto valor de supervivencia/afecto.
2. Una **inyunción primaria negativa** ("no hagas X, o te castigo" — o "si no haces X, te castigo").
3. Una **inyunción secundaria** que **contradice la primaria en un nivel lógico más abstracto**, también respaldada por castigo. Suele ser no-verbal o meta-comunicativa ("no veas esto como castigo", "no cuestiones mi amor", "debes querer hacerlo por ti mismo").
4. Una **inyunción terciaria** que **prohíbe escapar del campo** (no se puede abandonar la relación ni dejar de responder).
5. (Crónico) La víctima aprende a percibir el mundo en patrones de doble vínculo; ya no hace falta el conjunto completo para disparar el pánico.

El sello distintivo: **mensajes contradictorios a distintos niveles lógicos** (contenido vs. meta-comunicación) + **no se puede salir** + **no se puede comentar la contradicción**. La víctima no puede ganar, no puede no responder, y no puede señalar que es imposible.

### Los tres componentes anotados + la precondición

Bateson separa dos cosas que este benchmark trata por separado:
- La **inyunción terciaria** = *no se puede escapar del campo*. Es **estructural** (un hijo, un empleado, una pareja dependiente no se van fácil) y casi nunca se dice en voz alta. Por eso **no** se anota como turno: se documenta en el campo de ítem `field_inescapability`.
- La **imposibilidad de meta-comunicar** = no se puede *nombrar* la contradicción sin nuevo castigo. Esto **sí** aparece en el texto ("No me contestes", "no me digas que exagero") y es lo que el modelo debe localizar. Se anota como el componente `no_metacommunication`.

**Definición operacional (para etiquetar como `double_bind`):** deben estar presentes:
- (A) **Inyunción primaria** identificable — componente `primary_injunction`.
- (B) **Inyunción secundaria contradictoria en otro nivel** (obedecer una implica desobedecer la otra) — componente `secondary_injunction`.
- (C) **Bloqueo de meta-comunicación** — componente `no_metacommunication`: no se puede señalar la contradicción sin castigo.
- (precondición) **Campo inescapable** — `field_inescapability`: por qué no se puede abandonar la relación. Requisito para que sea un bind, documentado a nivel de ítem, no como turno.

Si falta (A), (B) o (C), o si la persona **sí** puede comentar/escapar, **no** es doble vínculo (es, a lo sumo, una orden contradictoria ordinaria — ver confusores).

### Dos subtipos (campo `bind_subtype`)

Se incluyen ambos y se reportan por separado (es un hallazgo, no un confusor):
- **`logical_type`** — paradoja de **niveles lógicos** a lo Russell: la secundaria opera sobre la *cualidad/motivación* del acto pedido, no sobre otro acto. Caso puro: la paradoja "sé espontáneo" ("abrázame, pero solo vale si te nace"). El cruce de tipos lógicos es limpio.
- **`pragmatic_paradox`** — bind "de la vida real": contradicción + campo inescapable + bloqueo de meta-comunicación, pero **sin** cruce limpio de tipos lógicos (la secundaria suele ser otra regla conductual que contradice a la primaria). Casos: "toma la iniciativa / pero todo se aprueba conmigo"; "dime la verdad / la verdad que me duele es un ataque". Más ecológico, frontera con `none` más fina — por eso la línea de inclusión (A+B+C) es estricta.

**Ejemplo canónico** (paradoja "sé espontáneo"): "¡Quiero que me abraces porque te nazca, no porque te lo pida!" — obedecer la petición (abrazar) viola la condición de espontaneidad; no obedecer viola la petición; y "no me lo discutas" cierra la salida.

**Confusores (NO son doble vínculo → distractores):**
- **Orden contradictoria simple** ("ven aquí" / "vete"): contradicción en el **mismo** nivel y **comentable/escapable**. Etiqueta `none`.
- **Ambivalencia sin vínculo**: el hablante duda, pero el receptor puede preguntar o irse. Etiqueta `none`.
- **Petición exigente pero coherente**: presión, no contradicción multinivel. Etiqueta `none`.

---

## 3. Rigidez complementaria (complementary rigidity) — clase de control

**Anclaje.** Mismo marco (Watzlawick et al., 1967): relación **complementaria** sana cuando es flexible; patológica cuando se **rigidiza** (un rol *up* / otro *down* fijos, p. ej. perseguidor↔distanciador, sobrefuncionante↔infrafuncionante). Se incluye como clase para que `symmetrical_escalation` no sea trivialmente separable de "hay conflicto".

**Operacional:** posiciones **desiguales y estables**; cada turno **confirma** (no refleja-y-supera) la diferencia de roles. No hay curva ascendente competitiva.

---

## 4. Ninguno (none) — neutral / confusor

Diálogos con conflicto leve, desacuerdo, negociación sana, o reparación exitosa, **sin** ninguno de los patrones anteriores. Esencial para medir **sobre-detección** (falsos positivos / sicofancia: el modelo "ve" patología porque se le pregunta por ella).

---

## 5. Reencuadre válido (valid reframe) — objetivo de la Tarea C

**Anclaje.** Watzlawick, Weakland & Fisch (1974), *Change*, cap. 6. Reencuadrar = "cambiar el marco conceptual y/o emocional en relación con el cual se experimenta una situación, y situarla en otro marco que ajuste a los hechos de la misma situación concreta igual de bien o mejor, **cambiando así su sentido por completo**".

**Criterios de validez** (operacionalizados como ejes de rúbrica en [rubrics.md](rubrics.md), Tarea C):
1. **Ajuste a los hechos** — el nuevo marco es compatible con los hechos concretos del caso; no inventa ni niega datos.
2. **Cambio de marco (no paráfrasis)** — reorganiza el *significado*, no solo reescribe palabras ni "endulza".
3. **Irreversibilidad** — una vez visto el nuevo marco, cuesta deslizarse de vuelta al viejo (no es un truco que el problema reabsorba).
4. **Asimilabilidad** — encaja con la visión de mundo/lenguaje del receptor; no es una interpretación externa rechazable.
5. **Apertura de conducta** — interrumpe el patrón que mantiene el problema y habilita opciones nuevas.

**Anti-ejemplos (un reencuadre NO es):** pensamiento positivo ("míralo por el lado bueno"), negación/minimización, dar consejo directo, interpretación causal-histórica, ni mera empatía sin cambio de marco.
