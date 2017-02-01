// Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the registration form.
  // It has the name attribute "registration"
  $("form[name='createSlice']").validate({
    // Specify validation rules
    rules: {
      // The key name on the left side is the name attribute
      // of an input field. Validation rules are defined
      // on the right side
      SliceName: "required",
      SliceIp: "required",
      AdminEmail: {
        required: true,
        // Specify that email should be validated
        // by the built-in "email" rule
        email: true
      },
      SlicePort: {
        required: true,
        maxlength: 5
      }
    },
    // Specify validation error messages
    messages: {
      SliceName: "Please enter slice name",
      SliceIp: "Please enter slice IP adresse",
      SlicePort: {
        required: "Please provide a port",
        minlength: "Your port number must be at least 5 characters long"
      },
      AdminEmail: "Please enter a valid email address"
    },
    // Make sure the form is submitted to the destination defined
    // in the "action" attribute of the form when valid
    submitHandler: function(form) {
      form.submit();
    }
  });
});