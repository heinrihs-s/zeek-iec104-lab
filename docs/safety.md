# safety

These tools are for synthetic data only. They do not open sockets, do not
talk to live IEC-104 devices, and do not send packets.

Each script refuses to run if any of these arguments are passed:

- `--host`
- `--ip`
- `--target`
- `--port`
- `--connect`
- `--send`

If you find yourself wanting to add live behaviour, fork into a separate
project. Keep this one boring.

The scenario files are templates of shapes, not weaponised tooling. Treat
them as input for offline analysis pipelines, not as a recipe to run
anywhere.
