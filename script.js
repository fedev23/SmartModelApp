Shiny.addCustomMessageHandler('navigate', function(screen) {
    $('a[data-value="' + screen + '"]').tab('show');
});


Shiny.addCustomMessageHandler('open-accordion', function(data) {
    var section = document.getElementById(data.section_id);
    if (section) {
        section.querySelector('button').click(); // Simula un click para abrir el acordeón
    }
});

// Manejo de la apertura y cierre de los menús
document.querySelectorAll('.menu-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var menuContent = this.nextElementSibling;
        menuContent.style.display = (menuContent.style.display === 'block') ? 'none' : 'block';
    });
});

// Manejo de la apertura y cierre del submenú
document.querySelectorAll('.menu-content a').forEach(function(link) {
    link.addEventListener('click', function(event) {
        var submenu = this.nextElementSibling;
        if (submenu) {
            submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
        }
    });
});

// Cerrar el menú si se hace clic fuera de él
document.addEventListener('click', function(event) {
    document.querySelectorAll('.menu-container').forEach(function(menu) {
        var button = menu.querySelector('.menu-btn');
        var menuContent = menu.querySelector('.menu-content');
        if (!menu.contains(event.target) && event.target !== button) {
            menuContent.style.display = 'none';
        }
    });
}); 

 // Manejo de la apertura y cierre de los menús
document.querySelectorAll('.results-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var menuContent = this.nextElementSibling;
        menuContent.style.display = (menuContent.style.display === 'block') ? 'none' : 'block';
    });
});


 // Manejo de la apertura y cierre del submenú
document.querySelectorAll('.results-content a').forEach(function(link) {
    link.addEventListener('click', function(event) {
        var submenu = this.nextElementSibling;
        if (submenu) {
            submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
        }
    });
});


// Cerrar el contenido del nuevo botón si se hace clic fuera de él
document.addEventListener('click', function(event) {
document.querySelectorAll('.results-btn').forEach(function(button) {
var resultsContent = document.querySelector('.results-content');
if (!resultsContent.contains(event.target) && event.target !== button) {
    resultsContent.style.display = 'none';
}
});
});


// Nuevo boton

  // Manejo de la apertura y cierre de los menús
  document.querySelectorAll('.resultados-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var menuContent = this.nextElementSibling;
        menuContent.style.display = (menuContent.style.display === 'block') ? 'none' : 'block';
    });
});


 // Manejo de la apertura y cierre del submenú
document.querySelectorAll('.resultados-content a').forEach(function(link) {
    link.addEventListener('click', function(event) {
        var submenu = this.nextElementSibling;
        if (submenu) {
            submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
        }
    });
});


// Cerrar el contenido del nuevo botón si se hace clic fuera de él
document.addEventListener('click', function(event) {
document.querySelectorAll('.resultados-btn').forEach(function(button) {
var resultsContent = document.querySelector('.resultados-content');
if (!resultsContent.contains(event.target) && event.target !== button) {
    resultsContent.style.display = 'none';
}
});
});






 // Manejo de la apertura y cierre de los menús
 document.querySelectorAll('.desplegable-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        var menuContent = this.nextElementSibling;
        menuContent.style.display = (menuContent.style.display === 'block') ? 'none' : 'block';
    });
});


 // Manejo de la apertura y cierre del submenú
document.querySelectorAll('.desplegable-content a').forEach(function(link) {
    link.addEventListener('click', function(event) {
        var submenu = this.nextElementSibling;
        if (submenu) {
            submenu.style.display = (submenu.style.display === 'block') ? 'none' : 'block';
        }
    });
});


// Cerrar el contenido del nuevo botón si se hace clic fuera de él
document.addEventListener('click', function(event) {
document.querySelectorAll('.desplegable-btn').forEach(function(button) {
var resultsContent = document.querySelector('.desplegable-content');
if (!resultsContent.contains(event.target) && event.target !== button) {
    resultsContent.style.display = 'none';
}
});
});