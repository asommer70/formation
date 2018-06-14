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
  if ($('.form-content').length) {
    Vue.config.devtools = true;
    window.app = new Vue ({
      el: '.form-content',
      data:  {
	input: {},
	pathParts: null
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

	  var url, method;
	  if (this.pathParts[this.pathParts.length - 1] !== "" && this.pathParts[1] !== 'forms' && this.pathParts[this.pathParts.length - 1] !== "Delete") {
	    url = '/api/inbox/' + this.pathParts[this.pathParts.length - 1];
	    method = 'put';
          } else {
	    url = '/api/inbox/';
	    method = 'post';
	  }
	  console.log('url:', url, 'method:', method, 'this.pathParts:', this.pathParts);
	  
  	  $.ajax({
	    url: url,
	    method: method,
	    data: data,
	    headers: {
	      Authorization: 'Token ' + token,
	      contentType: 'application/json; charset=utf-8'
	    },
	    success: function(data) {
	      console.log('post data:', data);
	      window.location.href = '/inbox/' + data.id;
	    }
	  });
	}
      },
      created: function() {
	this.pathParts = window.location.pathname.split('/');
	if (this.pathParts[this.pathParts.length - 1] !== "" && this.pathParts[this.pathParts.length - 1] !== "delete" && this.pathParts[1] === "inbox") {
	  self = this;
	  $.ajax({
	    url: '/api/inbox/' + this.pathParts[this.pathParts.length - 1],
	    method: 'get',
	    headers: {
	      Authorization: 'Token ' + token,
	      contentType: 'application/json; charset=utf-8'
	    },
	    success: function(data) {
	      console.log('input data:', data.data);
	      if (data.data) {
		self.input = data.data;
	      }
	    }
	  });
	}
      }
    });
  }
});
