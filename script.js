Shiny.addCustomMessageHandler('navigate', function(screen) {
    $('a[data-value="' + screen + '"]').tab('show');
});


Shiny.addCustomMessageHandler('open-accordion', function(data) {
    var section = document.getElementById(data.section_id);
    if (section) {
        section.querySelector('button').click(); // Simula un click para abrir el acordeón
    }
});
