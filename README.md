# HA Home Hub

A standalone touch dashboard for Home Assistant. Edit `hub.html` to customize the display, then rebuild the container.

## Deploy with Arcane

1. Add this repository as a Git source and create a Git Sync project on `main`.
2. Select `compose.yaml` and enable **Sync Files** so Arcane includes the Dockerfile and dashboard.
3. Open the project and choose **Build & Deploy**. Set `HUB_PORT` in the project environment if port 8080 is in use.
4. Open `http://<arcane-host>:8080/` on the display. Enter the Home Assistant address reachable by that display and a Home Assistant long-lived access token. Use `/#setup` to revisit these settings.

The display browser connects directly to Home Assistant over WebSocket and stores its settings and token locally. Keep the stack on a trusted network. If you serve the hub over HTTPS, use an HTTPS Home Assistant address too so the browser can connect over WSS. Keep tokens out of the repository and Compose environment.

For local Docker use, run `docker compose up --build -d`.
