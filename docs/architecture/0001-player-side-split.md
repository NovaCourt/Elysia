# 0001 -- The player-side split

## What

The player's machine runs four things:

1. **The app** -- everything the player sees and touches. TypeScript, React for the screens, Electron for the window.
2. **The mechanics** -- the game's rules, in Python, as a local process on the player's own CPU.
3. **The spirit's engine** -- llama.cpp running the player's own model, installed as a prebuilt wheel for their GPU.
4. **The gateway** -- one local TypeScript (Fastify) process, the only door to the Court's servers.

The app and the mechanics talk to the gateway over localhost HTTP with JSON bodies, described by the schemas in
`contract/`.

## Why

- **TypeScript for what the player sees:** type checking before anything runs, and the most mature ecosystem for
  desktop interfaces.
- **Python for the mechanics:** the same language as the living world the game is drawn from, so rules can be shared
  rather than rewritten.
- **One gateway:** one door out is one door to audit. The player's credentials live only inside it; neither the app nor
  the mechanics ever sees them.
- **Refusals are enforced on the server side.** Everything on the player's machine can be read and edited by the
  player, so no rule that protects someone else may rely on code running there.

## Turned down

- **Tauri instead of Electron:** Tauri draws with each system's own webview, which differs from distro to distro;
  Electron carries its own. Electron is larger, and chosen for now for predictability.
- **The mechanics calling the Court directly:** two doors instead of one.
- **A llama.cpp server binary for the spirit:** in-process calls through a wheel instead.

## What it rests on

- FACT: the engine wheels (`xllamacpp`, MIT) install and run on NVIDIA hardware from a clean machine with only a
  driver installed, measured on two machines with different GPU generations, through the installer.
- FACT: the engine opens a localhost HTTP port even when called in-process. It is locked to 127.0.0.1 with a random
  key made at each launch and no CORS origins; calls without the key get 401.
- GUESS: Electron's size and memory cost are acceptable for this game. To be measured on low-end machines.

## How it is tested

The contract's schemas are validated on both sides at startup. The installer carries its own tests and a smoke test
that fails when a GPU machine silently runs on the CPU.
