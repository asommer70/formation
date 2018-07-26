$(document).ready(function() {
  $(document).foundation();


  // Apply CodeMirror to Form content field.
  if ($('#id_content').length) {
    CodeMirror.fromTextArea(document.getElementById("id_content"), {
      lineNumbers: true,
      mode: "htmlmixed"
    });
  }

  // Submit search.
  var $searchInput = $('#search-input');
  $searchInput.keydown(function(event) {
    if (event.which === 13) {
      window.location.href = '/inbox/?search=' + $searchInput.val();
    }
  });

  $('#search-button').click(function(event) {
    event.preventDefault();
    window.location.href = '/inbox/?search=' + $searchInput.val();
  });

});
