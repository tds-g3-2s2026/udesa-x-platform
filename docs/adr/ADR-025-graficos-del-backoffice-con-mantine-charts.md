# ADR-025: `@mantine/charts` para los gráficos del backoffice

**Fecha:** 2026-11-15 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`E5-H3 CA.2` pide un gráfico de barras o líneas con los registros de la última semana en el
dashboard del backoffice (`udesa-x-backoffice#39`). El backoffice no tiene ninguna librería de
gráficos, y la regla de simplicidad de su `AGENTS.md` pide un ADR aprobado antes de sumar una. El
issue recomendaba `@mantine/charts`, de la misma familia que el resto de la interfaz.

## Decisión

**`@mantine/charts` en `backoffice`**, fijado en la versión exacta de `@mantine/core` (hoy
`9.5.2`), porque cada versión pide exactamente su par de `@mantine/core`. Dibuja con `recharts`,
que entra como dependencia directa porque `@mantine/charts` lo declara como peer. Sus estilos se
importan una vez en `main.tsx`, junto a los de `@mantine/core`.

El costo es el tamaño del bundle. El backoffice se arma en un solo chunk, y con `vite build`:

| | JS | JS gzip |
|---|---:|---:|
| `main` | 756,65 kB | 236,30 kB |
| Con el gráfico de registros | 1.169,43 kB | 354,82 kB |

Son 118 kB más comprimidos, un 50% más. Se acepta porque el backoffice lo usan pocos
administradores, desde una computadora, y el gráfico queda con los colores, la tipografía y el
modo oscuro del tema sin escribir nada.

## Alternativas descartadas

- **Barras dibujadas a mano con componentes de Mantine.** No suma dependencias ni peso, pero los
  ejes, la escala, los tooltips y la accesibilidad quedan a cargo del equipo, con sus tests, y se
  repiten en cada gráfico nuevo.
- **Cargar el gráfico con `React.lazy`.** Sacaría `recharts` del chunk inicial, pero el dashboard
  es la ruta `/`, la primera pantalla después del login, así que el chunk se baja igual enseguida.
  Suma código sin una ganancia que se note.
- **Otra librería de gráficos.** Ninguna comparte el sistema de estilos de Mantine: habría que
  adaptar colores y modo oscuro a mano.

## Consecuencias

- El bundle del backoffice crece unos 118 kB gzip.
- Actualizar `@mantine/core` obliga a actualizar `@mantine/charts` a la misma versión en el mismo
  PR.
- Los próximos gráficos del dashboard usan esta misma librería.
- Si el peso llega a importar, el primer paso es partir el bundle por ruta, no cambiar de
  librería.
