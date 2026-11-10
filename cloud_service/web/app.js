const byId = (id) => document.getElementById(id);

async function refreshStatus() {
  try {
    const response = await fetch("/api/status", { cache: "no-store" });
    if (!response.ok) throw new Error("status request failed");
    const data = await response.json();

    byId("service-status").innerHTML = "<i></i> " + (data.service === "online" ? "ONLINE" : "OFFLINE");
    byId("service-status").querySelector("i").style.background = data.service === "online" ? "#51d5a2" : "#e06b6b";
    byId("cloud-value").textContent = data.service === "online" ? "Online" : "Unavailable";
    byId("voice-value").textContent = data.voice === "provider_configured" ? "Provider configured" : "Not configured";
    byId("desktop-value").textContent = data.desktop_agent === "connected" ? "Connected" : "Not connected";

    const ready = data.voice === "provider_configured";
    byId("call-label").textContent = ready ? "VOICE SERVICE PENDING" : "VOICE NOT CONFIGURED";
    byId("voice-status").textContent = ready
      ? "Gemini credentials are present. Secure user authentication and the Live voice transport are the next implementation steps."
      : "Voice calling will be enabled after server-side Gemini configuration, secure account authentication and Gemini Live integration.";
  } catch {
    byId("service-status").textContent = "OFFLINE";
    byId("cloud-value").textContent = "Unavailable";
    byId("voice-value").textContent = "Unknown";
  }
}

if ("serviceWorker" in navigator && location.protocol === "https:") {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => {}));
}
refreshStatus();
