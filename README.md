# Sistema agéntico en OpenCode para programación orientada a objetos

Sistema de agentes de IA hecho con **OpenCode** que ayuda a **diseñar** un programa en Python, **escribir el código fuente** y **realizar pruebas**.

## Agentes (`.opencode/agent/`)
| Agente | Rol |
|---|---|
| `arquitecto` | Diseña las clases y el diagrama (`docs/diseno.md`) |
| `desarrollador` | Escribe el código en `src/` a partir del diseño |
| `tester` | Crea y ejecuta pruebas en `tests/` y reporta (`docs/reporte-pruebas.md`) |
| `revisor` | Revisa todo y documenta (`docs/revision.md`) |

## Skills (`.opencode/skill/`)
| Skill | Usada por | Para qué |
|---|---|---|
| `diseno-clases-poo` | arquitecto | Identificar clases, relaciones y diagramas Mermaid |
| `escritura-codigo-python` | desarrollador | Convenciones y plantilla de clases en Python |
| `pruebas-unitarias-python` | tester | Casos normales, límite y de error con pytest |
| `revision-y-documentacion` | revisor | Checklist de revisión y README |

## Flujo de trabajo
1. El usuario describe el programa que quiere.
2. **Arquitecto** → `docs/diseno.md`
3. **Desarrollador** → `src/`
4. **Tester** → `tests/` + `docs/reporte-pruebas.md`
5. **Revisor** → `docs/revision.md`

## Cómo usarlo
1. Instala OpenCode y abre esta carpeta: `opencode`
2. Elige el agente con la tecla `Tab` (o menciónalo con `@arquitecto`, `@tester`, etc.).
3. Pide, por ejemplo: *"Diseña un sistema de biblioteca con libros, socios y préstamos"*.
4. Pasa al desarrollador, luego al tester y al revisor.

## Estructura
```
.
├── .opencode/
│   ├── agent/
│   └── skill/
├── docs/
├── src/
├── tests/
└── README.md
```
