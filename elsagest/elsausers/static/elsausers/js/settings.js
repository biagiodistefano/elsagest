$('form').submit(evt => {
  evt.preventDefault();
  const form = $(evt.currentTarget);
  const action = form.attr('action');
  const formResult = form.find('.form-result');
  const datastring = form.serialize();
  $.post({
    url: action,
    data: datastring,
    dataType: 'json'
  }).done(response => {
    const { success, message } = response;
    if (success) {
      $(formResult).append($(`<h4 class="text-center text-success bg-success">${message}</h4>`));
      setTimeout(() => {
        form.find('option:selected').remove();
        form.trigger('reset');
      }, 3000);
    } else {
      $(formResult).append($(`<h4 class="text-center text-danger bg-danger">${message}</h4>`));
    }
  }).fail(err => {
    $(formResult).append($(`<h4 class="text-center text-danger bg-danger">Si è verificato un errore: ${err}</h4>`));
  }).always(() => {
    setTimeout(() => {
      $(formResult).empty();
    }, 3000);
  });
});
