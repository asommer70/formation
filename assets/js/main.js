$(document).ready(function() {
  $(document).foundation();


  // Apply CodeMirror to Form content field.
  if ($('#id_content').length) {
    CodeMirror.fromTextArea(document.getElementById("id_content"), {
      lineNumbers: true,
      mode: "htmlmixed"
    });
  }

  // Create Vue app for creating Inputs.
  new Vue ({
    el: '.form-content',
    data:  { } ,
    methods: {
      submitForm: function(event) {
	// Serialize form into a JSON object to send to /inbox/create.
	var $form = $('#input-form');
	var formData = $form.serializeObject();
	var data = {
	  form: $form.attr('name'),
	  data: formData,
	  user: userId
	};

	console.log('data:', data);

	$.ajax({
	  url: '/api/inbox/',
	  method: 'post',
	  data: data,
	  headers: {
	    Authorization: 'Token ' + token,
	    contentType: 'application/json; charset=utf-8'
	  },
	  success: function(data) {
	    console.log('post data:', data);
	  }
	});
      }
    },
    created: function() {
      console.log('Vue app...');
    }
  });

});
