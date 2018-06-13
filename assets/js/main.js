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
  Vue.config.devtools = true;
  window.app = new Vue ({
    el: '.form-content',
    data:  {
      input: {}
    },
    methods: {
      submitForm: function(event) {
	// Serialize form into a JSON object to send to /inbox/create.
	var $form = $('#input-form');
	var formData = $form.serializeObject();
	var data = {
	  form: $form.attr('name'),
	  data: JSON.stringify(formData),
	  user: userId
	};

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
      var pathParts = window.location.pathname.split('/');
      if (pathParts[pathParts.length - 1] !== "" && pathParts[1] === "inbox") {
	console.log('Input...');
	$.ajax({
	  url: '/api/inbox/' + pathParts[pathParts.length - 1],
	  method: 'get',
	  headers: {
	    Authorization: 'Token ' + token,
	    contentType: 'application/json; charset=utf-8'
	  },
	  success: function(data) {
	    console.log('input data:', data.data);
	    this.input = data.data;
	  }
	});
      }
    }
  });
});



