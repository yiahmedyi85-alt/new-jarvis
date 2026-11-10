# JARVIS cloud voice implementation plan

## 1. Current codebase findings

The source archive available for this project contains a Python desktop assistant with:

- A FastAPI dashboard in `dashboard/server.py`.
- Existing device pairing and bearer-token authentication for the local dashboard.
- A phone microphone WebSocket at `/ws/phone-audio`.
- A bounded `_phone_audio_queue` that receives PCM audio frames.
- A relay in `main.py` that forwards phone microphone audio into the active Gemini Live session.
- Gemini Live session setup in `main.py` and `core/gemini.py`.
- Audio output currently routed through the desktop assistant's local audio playback pipeline.

Important limitation: the existing phone audio path is designed for a phone connected to the desktop dashboard. It is not a cloud calling service. It sends microphone audio toward the desktop session, and the current output path plays assistant audio on the desktop. It does not yet provide a complete browser-to-cloud two-way call.

The GitHub repository was empty when this plan was created. The source archive has not been copied into the repository.

## 2. Target architecture

```text
Android browser / installable PWA
  | HTTPS, authenticated API, WebRTC
  v
Cloud FastAPI service
  |-- user authentication and device sessions
  |-- call/session coordinator
  |-- Gemini Live session broker
  |-- conversation and task event storage
  |-- Web Push notification service
  |
  +---- Cloud AI conversation works while the desktop is offline
  |
  +---- Secure outbound connection
          v
      Local JARVIS desktop agent
          |-- approved desktop actions
          |-- local files and apps
          |-- status and task completion events
          +-- only works while the PC is online
```

The browser must never receive the permanent Gemini API key. The cloud service will authenticate the user and issue only short-lived session credentials or proxy the Live connection server-side, depending on the supported Gemini Live API flow.

## 3. Implementation phases

### Phase 0: repository and source integration

- Import the existing desktop assistant source while preserving its original attribution and license.
- Keep secrets, OAuth credentials, certificates, local memory databases, and runtime data out of Git.
- Add a repeatable development setup and environment-variable example with placeholder values only.

### Phase 1: cloud service foundation

- Add a separate cloud application so the desktop dashboard remains usable.
- Add configuration validation, health endpoint, structured logs, and production startup settings.
- Add persistent storage for users, paired devices, sessions, and task events.
- Add secure authentication, token expiry, revocation, and rate limits.

### Phase 2: mobile web app

- Build a responsive mobile-first call screen.
- Add sign-in, call start/end, connection state, microphone permission handling, and reconnect behavior.
- Add PWA manifest and service worker.
- Add a conversation history and task notification view.

### Phase 3: two-way voice

- Integrate Gemini Live using server-held credentials.
- Use WebRTC for low-latency browser audio.
- Stream microphone audio to the active session and assistant audio back to the browser.
- Handle interruptions, disconnects, session expiry, and network changes.
- Test on Android Chrome and desktop browsers.

### Phase 4: task notifications and incoming call experience

- Add Web Push subscription management.
- Notify the phone when a task finishes or JARVIS needs attention.
- Let the user open the PWA and start a browser voice session.
- Do not present browser notifications as guaranteed incoming phone calls. Browser and Android background restrictions still apply.

### Phase 5: connect the desktop agent

- Make the local agent establish an authenticated outbound connection to the cloud.
- Use a device-specific credential with rotation and revocation.
- Send approved action requests to the desktop only while it is online.
- Return task status and completion events to the cloud.
- Require user confirmation for sensitive or destructive local actions.

### Phase 6: deployment and verification

- Deploy the cloud API and static PWA behind HTTPS.
- Configure secrets through the host's secret manager.
- Add database backups, health checks, and error monitoring.
- Test laptop-offline conversations, laptop-online desktop actions, push notifications, reconnects, and token revocation.

## 4. Security requirements

- Never commit `config/api_keys.json`, `.env` files, OAuth tokens, private certificates, or personal memory data.
- Store Gemini credentials only in server-side secrets.
- Hash stored refresh/device tokens where practical.
- Use short-lived access tokens, rotation, and revocation.
- Validate WebSocket/WebRTC session ownership before accepting media.
- Apply request size limits, rate limits, and origin checks.
- Keep desktop actions behind an explicit allowlist and confirmation gate.
- Do not expose a public unauthenticated endpoint that can execute commands on the user's PC.

## 5. Key product boundary

Cloud conversations can continue while the laptop is off because the cloud service owns the AI session. Actions that require the laptop, its applications, or its local files cannot run while the laptop is off. The phone interface is a web app, not a telephone-number or PSTN calling service.

## 6. First engineering milestone

Before implementing the call transport, import and review the existing source in this repository. Then build the cloud service as a separate package and connect it to the existing Gemini Live and desktop-agent interfaces without breaking the current local dashboard.
