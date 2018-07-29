$(document).ready(function() {
  $(document).foundation();

  // Make the current menu item active.
  var pathParts = window.location.pathname.split('/');
  var route = pathParts[pathParts.length - 2];
  
  if (route == 'inbox') {
    $('#inbox-menu-item').addClass('active');
    $('#inbox-count').css({background: 'white', color: '#212121'});
  } else if (route == 'archive') {
    $('#archive-menu-item').addClass('active');
  } else if (route == 'approvals') {
    $('#approvals-menu-item').addClass('active');
  } else if (route == 'admin') {
    $('#admin-menu-item').addClass('active');
  } else {
    $('#forms-menu-item').addClass('active');
  }


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
