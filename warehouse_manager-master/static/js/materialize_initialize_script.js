/* part of the materialize requirements, each javasript elemtn to be use within the classes must be called in a document ready function */

$(document).ready(function() {
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown();
    $('select').formSelect();
    $('.modal').modal();
});

