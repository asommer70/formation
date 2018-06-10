$(document).ready(function() {
  $(document).foundation();

  if ($('#id_content').length) {
    CodeMirror.fromTextArea(document.getElementById("id_content"), {
      lineNumbers: true,
      mode: "htmlmixed"
    });
  }

});
