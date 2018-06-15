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

    new Vue({
      el: '.form-content',
      data: function() {
	return {
	  input: {}
	}
      }
    });
    
    Vue.component('FormInputComponent', {
      props: ['value'],
      methods: {
	submitForm: function(event) {
	  // Serialize form into a JSON object to send to /inbox/create.
	  var self = this;
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
	      localStorage.setItem('form_' + self.pathParts[self.pathParts.length - 1], null);
	      window.location.href = '/inbox/' + data.id;
	    }
	  });
	},

	saveInput: function(event) {
	  this.input[event.target.name] = event.target.value;
	  console.log('saveInput event.target:', event.target.checked);

	  // Handle checkboxes.
	  if (event.target.type === 'checkbox') {
	    if (event.target.checked) {
	      this.input[event.target.name] = 'checked';
	    } else {
	      this.input[event.target.name] = null;
	    }
	  }

	  // Handle radio buttons.
	  /* if (event.target.type === 'radio') {
	     console.log('event.target.id:', event.target.id);
	     if (event.target.checked) {
	     this.input[event.target.name] = event.target.value;
	     } else {
	     this.input[event.target.name] = null;
	     }
	     } */

	  console.log('this.input:', this.input);
	  localStorage.setItem('form_' + this.pathParts[this.pathParts.length - 1], JSON.stringify(this.input));
	},

	propertySetter: function(key, value) {
	  this.localValue = Object.assign({}, this.localValue, {[key]:value});
	}
      },
      computed: {
	localValue: {
	  get: function() {
	    return this.value
	  },
	  set: function(value) {
	    console.log('emit called');
	    this.$emit('input', value);
	  }
	},
	test: {
	  get: function() {
	    return this.localValue.test;
	  },
	  set: function(value) {
	    this.propertySetter('test', value);
	  }
	},
      }
      /* created: function() {
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

	 // Restore inputs on load.
	 if (this.pathParts[this.pathParts.length - 1] !== "" && this.pathParts[this.pathParts.length - 1] !== "delete" && this.pathParts[1] === "forms") {
	 console.log('loading from localStorage...');
	 var data = localStorage.getItem('form_' + this.pathParts[this.pathParts.length - 1]);
	 console.log('data:', data);
	 if (data !== 'null' && data !== null) {
	 this.input = JSON.parse(data);
	 }
	 }
       * } */
    });
  }
});
