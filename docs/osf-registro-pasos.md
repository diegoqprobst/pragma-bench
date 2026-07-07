# Registro OSF — pasos exactos (Diego, ~20 min)

> El registro OSF es la compuerta de la producción del set de evaluación (así lo declara el
> working paper publicado). Estos son los pasos exactos, en orden.

## 0. Cuenta (una sola vez)

1. Ir a **osf.io** → *Sign up*.
2. Elegir **"Sign in with ORCID"** (tienes ORCID: `0009-0005-7107-8897`). OSF crea la cuenta
   vinculada — no necesitas afiliación institucional (déjala en blanco; "independent researcher" va bien).
3. Confirmar el correo (diegoaquinde@gmail.com).

## 1. Crear el proyecto

1. *My Projects* → **Create new project**.
2. Título: `Palo Alto Bench`. Descripción: una línea (puedes pegar la del README).
3. En el proyecto: *Settings* → dejarlo **privado por ahora** (el registro se hace público aparte).

## 2. Crear el registro (esto es lo que importa)

1. Dentro del proyecto → pestaña **Registrations** → **New registration**.
2. Plantilla: **"Open-Ended Registration"** (la más simple; nuestro documento ya trae toda la estructura).
3. En el campo de resumen/summary: **pegar el contenido completo de `docs/prereg-osf.md`**
   (desde "## 1. Título" hasta el final; el bloque de cabecera con "> Estado: borrador…" NO se pega).
4. Continuar → en la pantalla final elegir **"Make registration public immediately"**
   (nada de embargo — la gracia es el timestamp público).
5. Registrar. OSF genera **URL y DOI** del registro.

## 3. Después de registrar (me pasas los datos y yo cierro el circuito)

- Pásame: **fecha, URL del registro y DOI**.
- Yo actualizo: `docs/prereg-osf.md` (anotar fecha/URL/hash del commit), `paper/paper.md`
  (los `[DOI]` de OSF), `README.md`, y el registro de Zenodo si aplica (related identifier).
- Y con eso queda **abierta la producción del set de evaluación** (plan en
  [plan-de-tandas.md](plan-de-tandas.md)).

## Notas

- El registro es **inmutable** una vez creado — por eso pegamos el documento ya congelado, sin editar.
- Si OSF pide categoría: *Study Registration / Preregistration*.
- Costo: cero.
