# Isolation

Run these labs on a development machine or disposable VM. Compose publishes on 127.0.0.1, uses an internal network, drops capabilities, runs as a non-root UID, sets a read-only filesystem, and limits memory and process counts. There are no host mounts or persistent volumes in the starter labs.

Containers share the host kernel; they are not a boundary for kernel exploits. Network attacks needing raw sockets, host networking, or privileged containers belong in a separately designed VM lab. These starter labs do not require those capabilities.

The unauthenticated network example is a purpose-built line-oriented TCP service, not a vulnerable implementation of a production protocol. The fixed service removes unauthenticated configuration access while retaining PING.

Use `python lab.py down <id> --purge` after use. If deployment verification fails, containers may remain running so logs can be inspected; use the same cleanup command.
