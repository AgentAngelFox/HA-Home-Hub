# HA Home Hub

One Docker container serves all displays. Each display saves its own layout in its browser. Use the same hub URL on each display and omit the room query parameter to keep room selections editable.

## Arcane

Set these in the project environment before redeploying.

- `HA_URL` is your Home Assistant base URL. Use an address the container can reach and the displays can use for camera and media images.
- `HA_ACCESS_TOKEN` is the Home Assistant token. Enter it once in Arcane.
- `HUB_DISPLAY_IPS` is a comma-separated list of the displays' IP addresses. Use a direct connection to the Docker host. Access is denied by default and checked against the incoming connection address.
- `HUB_PORT` defaults to 8080 for Git Sync deployments.

For Git Sync, select `compose.yaml`, enable **Sync Files**, and use **Build & Deploy**. If you pasted the remote build URL into a standalone Arcane project, add the three settings to the service:

```yaml
    environment:
      HA_URL: ${HA_URL}
      HA_ACCESS_TOKEN: ${HA_ACCESS_TOKEN}
      HUB_DISPLAY_IPS: ${HUB_DISPLAY_IPS}
```

Keep the dashboard on your LAN. An allowed display can act as the configured Home Assistant user. Keep the token in Arcane's project environment and out of Git.
