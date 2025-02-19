Shiny.addCustomMessageHandler('navigate', function(screen) {
    $('a[data-value="' + screen + '"]').tab('show');
});

Shiny.addCustomMessageHandler('redirectToURL', function(user_id) {
    console.log("Redirigiendo a: http://localhost:8000/?user_id=" + user_id);  // Imprime la URL
    window.location.href = "http://localhost:8000/?user_id=" + encodeURIComponent(user_id);
});

// Asumiendo que estás usando JavaScript en el frontend
Shiny.addCustomMessageHandler('store_credentials', function(message) {
    localStorage.setItem('access_token', message.access_token);
    localStorage.setItem('user_email', message.user_email);
    console.log("Credentials stored in localStorage.");
});

Shiny.addCustomMessageHandler('open-accordion', function(data) {
    var section = document.getElementById(data.section_id);
    if (section) {
        section.querySelector('button').click(); // Simula un click para abrir el acordeón
    }
});

Shiny.addCustomMessageHandler("redirect", function(url) {
    window.location.href = url;
});


Shiny.addCustomMessageHandler("render_screen", function(message) {
    var screen_id = message.screen_id;

    // Mostrar los elementos de la pantalla solicitada, pero sin cambiar la pestaña activa
    var screen_elements = document.getElementById(screen_id);

    if (screen_elements) {
        // Aquí simplemente se asegura de que el contenido de la pantalla se renderice.
        // No se cambia el display de la pestaña activa, solo renderizamos los elementos.
        screen_elements.style.display = 'block'; // Aseguramos que los componentes se muestren
    }
});



Shiny.addCustomMessageHandler('crearCookie', function(data) {
    fetch("http://localhost:3000/api/login_starlette_session", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: data.user_id })
    })
    .then(resp => resp.json())
    .then(json => {
      console.log("Cookie set. Now go /shiny/");
      window.location.href = "http://localhost:3000/shiny/";
    });
  });
  
