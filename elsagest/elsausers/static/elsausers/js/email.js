
$('#email-promemoria').submit(evt => {
  evt.preventDefault();
  console.log('Invio email');
  $.post({
    url: '/elsausers/sendmail/',
    data: '',
    dataType: 'json'
  }).done(response => {
    const { success, message } = response;
    console.log(success, message);
  }).fail(err => {
    console.log(err);
  }).always(() => {
    console.log('dio cane');
  });
});
