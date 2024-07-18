$(document).ready(function () {
  $('#summary-form').submit(function () {
    console.log('submitting form')
    // disable button
    $('#submit').prop('disabled', true)
    // add spinner to button
    $('#submit').html(
      `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
    )
    $('#overlay').show()
  })
})
