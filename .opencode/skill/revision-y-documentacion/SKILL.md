---
name: revision-y-documentacion
description: Checklist de revisión de código POO y guía para generar el README y la documentación final del proyecto.
---

# Skill: revisión y documentación

## Checklist de revisión
- [ ] Cada clase de `docs/diseno.md` existe en `src/`.
- [ ] Los atributos están encapsulados.
- [ ] Hay docstrings en clases y métodos públicos.
- [ ] Las entradas se validan.
- [ ] No hay código repetido que deba ser una función o clase base.
- [ ] Todas las pruebas de `tests/` pasan.
- [ ] El programa se ejecuta sin errores.

## Salida de la revisión (`docs/revision.md`)
- Lo que está bien (2-3 puntos).
- Problemas encontrados: archivo, descripción, sugerencia.
- Veredicto: aprobado / requiere cambios.

## README del proyecto
Debe incluir:
1. Qué hace el programa.
2. Cómo ejecutarlo (`python src/main.py`).
3. Cómo correr las pruebas.
4. Estructura de carpetas.
5. Diagrama de clases (copiado de `docs/diseno.md`).
