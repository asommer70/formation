$(document).ready(function() {
  $(document).foundation();

  CodeMirror.fromTextArea(document.getElementById("form_content"), {
    lineNumbers: true,
    mode: "htmlmixed"
  });

});
