# Arcanos: Mod del Tarot (Fabric 1.21.11)

## Compilar
JDK 21 + Gradle 9.2+ (o `gradle wrapper`). `gradle build` -> jar en `build/libs/`.
Las 22 cartas son ilustraciones 128x128 estilo Rider-Waite (`gen_cards.py`, `rw_lib.py`, `rw_scenes*.py`; requiere Pillow y numpy). Para regenerar texturas, modelos, modelos, lang, recetas y logros: `python3 gen_assets.py` (solo stdlib).

## Bucle de progresión
1. **Exploración**: Santuarios (ruinas 11x11, cofre oculto bajo una baldosa agrietada, El Vidente) o comerciar con El Vidente -> primeros Sobres. Mesa del Tarot (receta) y Mazo (papel + Polvo Estelar).
2. **Colección**: cada carta nueva = +1 Punto de Destino. 5 cartas: +1 pasiva activa en el Mazo · 10: +2 espacios · 15: energía arcana (Polvo cada 2 min) · 22: +4 espacios y +5 puntos.
3. **Profecías** (Mesa: 3 cartas + amatista o 5 niveles): se cumplen a los 2-5 min. Fortuna (meteorito + cofre con Esquirlas), Peligro (oscuridad, emboscada y mini-jefe), Encuentro (mercader místico 4 min).
4. **Jefes** (Altar Arcano, 3 cartas-llave): Hierofante (Torre+Mago+Sol) · Sombra de la Luna, de noche (Estrella+Loco+Carro) · Juicio Final (Rueda+Estrella+Emperatriz+3 Páginas). 2 fases, ataques telegrafiados, esbirros.
5. **Ascensión** (Mesa, botón Fusionar): 2 cartas iguales + 2 Polvo + Esquirla = Astral · 2 Astrales + 4 Polvo + material de jefe = Cósmica (Fortuna: Lágrima Astral · Peligro: Corona Rota · Encuentro: Corazón del Destino). Las Cósmicas abren los nodos finales del Árbol.

## Árbol del Destino (tecla Z, configurable)
3 ramas x 5 nodos: Vidente (cooldown, sobres, tesoros, mazo), Arcanista (daño, radio, ahorro, efectos), Sobreviviente (resistencia, curación, escudo fatal, almas).
Datos en `<mundo>/tarot_data.json`, sincronizados con `SyncPayload` / `UnlockPayload`.

## Cartas
Clic derecho = activa (cuesta Polvo Estelar, o 3 niveles de XP por Polvo; cooldown visible en el ítem). Pasiva: mano secundaria o primeras N cartas del Mazo.

## Estado
El entorno de generación no tenía acceso a Maven: el código **no fue compilado**. Si `gradle build` marca algo, los puntos más probables son
`KeyBinding.Category.create` (TarotClient), `Entity.velocityModified`, `getAdvancementLoader().get(...)` (DestinyManager.grant) y la firma de `Screen.renderBackground`.

## Sistema de lectura (v0.2)
- Cartas **invertidas** (~25% al abrir sobres): cuestan 1 Polvo menos, enfrían 25% más lento y empujan la profecía hacia el Peligro.
- `card/Meanings.java`: significado derecha/invertida de las 22 cartas (editable; pendiente de revisión por una tarotista). Se ve en tooltip y Grimorio.
- La Mesa imprime una **lectura interpretada** (Pasado/Presente/Futuro). La carta del Futuro vuelve al jugador: si la lleva encima al cumplirse la profecía está **preparado** (Fortuna: más botín · Peligro: menos enemigos y mini-jefe débil · Encuentro: mejores ofertas).
- Pendiente: carta del día, otras tiradas, jefes "legibles" antes de invocarlos.
- Botón **Consejo** en la Mesa (1 carta en Futuro). `card/Readings.java`: narrativa por posición, combinaciones (Torre+Muerte, Sol+Luna...) y veredicto por cartas invertidas.
- **Ruleta del destino** (La Rueda, llevándola encima): ante un golpe mortal, el jugador queda a 1 de vida mientras una ruleta (~4 s) decide VIDA/MUERTE: 40% Normal, 50% Astral, 60% Cósmica. Si vive, 3 min de enfriamiento y empuja a los enemigos; si pierde, muere. No actúa contra `/kill` ni el vacío.
- **Cielo Rojo + Grieta** (`SkyEvent`, `SkyPayload`, `client/SkyOverlay`): se dispara con una tirada que incluya El Diablo, La Torre o La Muerte, con el Augurio de Peligro y al sellar el Pacto del Diablo. Partículas en forma de grieta sobre el jugador + velo rojo en pantalla. Usa `HudElementRegistry` (Fabric API); si no compila, cambiar por `HudRenderCallback`.

## Jefes con modelo 3D propio y animaciones
El Hierofante Corrompido, La Sombra de la Luna y El Juicio Final ya no son mobs vanilla: son entidades propias
(`boss/entity/`) con modelo por cajas, textura pintada y animaciones por keyframes.

- **Animaciones**: `idle` (bucle), caminar, `slam` (golpe), `cast` (bombardeo), `summon` (esbirros), `special` (ataque de fase 2),
  `enrage` (cambio a fase 2) y `death`. `BossManager` las dispara con cada ataque; durante una acción el jefe se detiene y encara al objetivo.
  El golpe de `slam` cae en el tick 30, igual que el telegrafiado en el suelo. Los esbirros aparecen a los 14 ticks de `summon`.
- **Fase 2**: aparecen partes extra (cristales, segunda aureola, luna llena, alas ardientes).
- **Código**: modelo genérico data-driven en `client/boss/` (`BossModel`, `BossModelData`, `BossRenderer`, `BossClient`).
  Los datos viven en `src/main/resources/tarot_boss/*.json` y las texturas en `assets/tarot/textures/entity/`.
- **Editar o ajustar**: modificá `gen_bosses.py` (cajas, pivotes, keyframes) y corré `python3 gen_bosses.py`.
  Con `python3 previews.py` se regeneran las imágenes/GIF de `previews/` para ver el resultado sin abrir Minecraft.
  Convención: `rx<0` levanta algo hacia el frente; `rz>0` abre el brazo derecho hacia afuera.
- **Pendiente / notas**: no hay capa de brillo (ojos y runas usan colores claros, no emisivos); el mini-jefe "Guardián del Presagio" sigue siendo un Esqueleto Wither.

## Menú de prueba (tecla K, solo en creativo)
Pantalla con botones para probar todo sin farmear: `client/DebugScreen` (cliente) + `debug/DebugActions` (servidor, valida creativo).
- **Jefes**: invocar los 3 sin cartas ni noche, lanzar cada animación, forzar cada ataque, forzar fase 2, curar, matar (con drops), eliminar, mini-jefe.
- **Cartas**: dar una carta o las 22, eligiendo nivel (Normal/Astral/Cósmica) e invertida.
- **Destino**: +1/+10/+100 puntos, desbloquear árbol, forjar Cósmica, completar/vaciar colección, reiniciar progreso, abrir Árbol y Grimorio.
- **Eventos**: cumplir profecías (Fortuna/Peligro/Encuentro) normal, preparada o invertida con poder 1-5, programarlas, acelerarlas, Cielo Rojo.
- **Objetos**: mazo, sobres, polvo, páginas, materiales de jefe, Altar, Mesa, kits de ritual de cada jefe y curarse.
Para añadir un botón: una línea en `DebugScreen` y un `case` en `DebugActions.run`.
