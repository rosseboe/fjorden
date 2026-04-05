// Minimal service worker to enable PWA installation.
// No caching — the app always needs live departure data.
self.addEventListener('fetch', event => {
  event.respondWith(fetch(event.request));
});
