$(document).ready(function() {
  $(document).foundation();

  CodeMirror.fromTextArea(document.getElementById("id_content"), {
    lineNumbers: true,
    mode: "html",
    smartIndent: true
  });

});







