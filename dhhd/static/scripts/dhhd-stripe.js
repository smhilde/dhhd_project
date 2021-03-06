Stripe.setPublishableKey('pk_live_uAbkWSKJLrs04ETeXMELNv1I');

function reportError(msg) {
    var $form = $('#payment-form');
    // Show the error in the form:
    $form.find('.payment-errors').text(msg).addClass('alert alert-error');
    // re-enable the submit button
    $form.find('button').prop('disabled', false);
    return false;
}
    
function stripeResponseHandler(status, response) {
  var $form = $('#payment-form');

  if (response.error) {
    // Show the errors on the form
    $form.find('.payment-errors').text(response.error.message);
    $form.find('button').prop('disabled', false);
  } else {
    // response contains id and card, which contains additional card details
    var token = response.id;
    // Insert the token into the form so it gets submitted to the server
    $form.append($('<input type="hidden" name="stripeToken" />').val(token));
    // and submit
    $form.get(0).submit();
  }
};


// Watch for the document to be ready
$(document).ready(function() {

  // Watch for a form submission:
  $('#payment-form').submit(function(event) {
    var $form = $(this);
    
    // Flag variable
    var error = false;

    // Disable the submit button to prevent repeated clicks
    $form.find('button').prop('disabled', true);

    // Get the values
    var ccNum = $('.card-number').val();
    var cvcNum = $('.card-cvc').val();
    var expMonth = $('.card-expiry-month').val();
    var expYear = $('.card-expiry-year').val();
    var custName = $('#id_customer_name').val();
    var addrLine1 = $('#id_address_line1').val();
    var addrLine2 = $('#id_address_line2').val();
    var addrCity = $('#id_address_city').val();
    var addrState = $('#id_address_state').val();
    var addrZip = $('#id_address_zip').val();
    var addrCountry = $('#id_address_country').val();
    
    // Validate the number
    if (!Stripe.validateCardNumber(ccNum)) {
      error = true;
      reportError('The credit card number appears to be invalid.');
    }
    
    // Validate the CVC number
    if (!Stripe.validateCVC(cvcNum)) {
      error = true;
      reportError('The CVC number appears to be invalid.');
    }
    
    // Vaildate the expiration
    if (!Stripe.validateExpiry(expMonth, expYear)) {
      error = true;
      reportError('The expiration date appears to be invalid.')
    }
    
    // Check for errors:
    if (!error) {
      // Get the Stripe token
      //Stripe.card.createToken($form, stripeResponseHandler);
      Stripe.card.createToken({
        number: ccNum,
        cvc: cvcNum,
        exp_month: expMonth,
        exp_year: expYear,
        name: custName,
        address_line1: addrLine1,
        address_line2: addrLine2,
        address_city: addrCity,
        address_state: addrState,
        address_zip: addrZip,
        address_country: addrCountry
      }, stripeResponseHandler);
    }

    // Prevent the form from submitting with the default action
    return false;
    
  }); // Form submission
  
  // $('a.popup').popup();
  
}); // Document ready
