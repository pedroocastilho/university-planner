self.addEventListener("install", function(e) {
    console.log("Service Worker instalado");
    e.waitUntil(
      caches.open("planner-cache").then(function(cache) {
        return cache.addAll(["/"]);
      })
    );
  });
  
  self.addEventListener("fetch", function(e) {
    e.respondWith(
      caches.match(e.request).then(function(response) {
        return response || fetch(e.request);
      })
    );
  });
  