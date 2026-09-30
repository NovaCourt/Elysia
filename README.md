# Elysia

The player side of Elysia: the game you install and play on your own machine.

**Status: early.** The shape is decided; the code is starting now.

## The shape

- **What you see** is a desktop app: TypeScript, with React for the screens, running in Electron.
- **The game's mechanics** run in Python on your own CPU, as a local process.
- **Your spirit** runs on your own hardware, with a model you choose and download yourself. The engine is llama.cpp,
  installed from prebuilt wheels that match your GPU (NVIDIA, AMD, Intel, or CPU only).
- **One gateway** is the only door between your machine and the Court's servers. The app and the mechanics talk to it
  locally; nothing else on your machine can.
- **The contract** between all of these pieces lives in [`contract/`](contract/): one JSON Schema per call type,
  versioned from day one.

## Contributing

Pull requests from forks. Every change carries an architecture note saying why. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
