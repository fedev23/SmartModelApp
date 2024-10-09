Shiny.addCustomMessageHandler('navigate', function(screen) {
    $('a[data-value="' + screen + '"]').tab('show');
});


Shiny.addCustomMessageHandler('navigate', function(screen) {
    var screen = message.screen;
    var elementId = message.element;

    // Mostrar la pestaña correspondiente
    var tabElement = $('a[data-value="' + screen + '"]');
    if (tabElement.length) {
        tabElement.tab('show');
        console.log('Pestaña mostrada:', screen);
    } else {
        console.log('No se encontró la pestaña para data-value:', screen);
    }

    // Si se proporciona un ID de elemento, desplazarlo a la vista
    if (elementId) {
        var targetElement = $('#' + elementId);
        if (targetElement.length) {
            // Puedes hacer scroll al elemento o realizar otras acciones
            targetElement[0].scrollIntoView({ behavior: 'smooth' });
            console.log('Elemento desplazado a la vista:', elementId);
        } else {
            console.log('No se encontró el elemento con ID:', elementId);
        }
    }
});




function toggleMenu(buttonClass, contentClass) {
    document.querySelectorAll(buttonClass).forEach(function(button) {
        button.addEventListener('click', function() {
            var content = this.nextElementSibling;
            content.style.display = (content.style.display === 'block') ? 'none' : 'block';
        });
    });

    document.addEventListener('click', function(event) {
        document.querySelectorAll(contentClass).forEach(function(menu) {
            var button = menu.previousElementSibling;
            if (!menu.contains(event.target) && event.target !== button) {
                menu.style.display = 'none';
            }
        });
    });
}

// Aplicar la función a los distintos botones y contenidos
toggleMenu('.menu-btn', '.menu-content');
toggleMenu('.results-btn', '.results-content');
toggleMenu('.datos-btn', '.datos-content');
toggleMenu('.right-button', '.menu-content_right');  // Nueva línea para manejar los botones con clase right-button