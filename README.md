# JARVIS

A personal AI assistant with a mobile web voice interface and a cloud communication layer.

## Current development status

The repository is being prepared for the cloud voice project. The existing desktop assistant source has not yet been imported into this repository.

## Target experience

- Open JARVIS from an Android phone using a mobile-friendly web app or installable PWA.
- Start a two-way voice conversation through the browser.
- Receive notifications when JARVIS has a completed task or requests attention.
- Keep cloud-based conversations available while the desktop computer is offline.
- Connect the desktop agent when the computer is online for approved local actions.

## Architecture

See [the implementation plan](docs/IMPLEMENTATION_PLAN.md).

## Security

- Never commit API keys, environment files, OAuth tokens, private certificates, or personal memory databases.
- Keep Gemini credentials on the server.
- Use authenticated sessions and short-lived credentials for browser voice sessions.
- Require explicit approval for sensitive desktop actions.
