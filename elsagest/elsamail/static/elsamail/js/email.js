
$('#email-promemoria').submit(evt => {
  evt.preventDefault();
  const $this = $(evt.currentTarget);
  const formResult = $($this.find('.form-result'));
  $.post({
    url: '/elsamail/sendmail/',
    data: '',
    dataType: 'json'
  }).done(response => {
    const { success, message } = response;
    let alertClass = 'alert-success';
    if (!success) {
      alertClass = 'alert-danger';
    }
    const messageBox = $(`<div class="alert ${alertClass} alert-dismissible fade in">
    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
    ${message}
    </div>`);
    formResult.append(messageBox);
  }).fail(err => {
    console.log(err);
  }).always(() => {
    setTimeout(() => {
      $(formResult).empty();
    }, 3000);
  });
});

$('#new_email').summernote({ dialogsInBody: true, height: 300 });
