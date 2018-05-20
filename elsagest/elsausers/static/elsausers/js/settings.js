$('#form-impostazioni').submit(evt => {
  evt.preventDefault();
  const form = $(evt.currentTarget);
  const formResult = form.find('.form-result');
  const datastring = form.serialize();
  $.post({
    url: '/impostazioni/',
    data: datastring,
    dataType: 'json'
  }).done(response => {
    const { success, message } = response;
    if (success) {
      $(formResult).append($(`<h4 class="text-center text-success bg-success">${message}</h4>`));
    } else {
      $(formResult).append($(`<h4 class="text-center text-danger bg-danger">${message}</h4>`));
    }
  }).fail(err => {
    console.log(err);
  }).always(() => {
    setTimeout(() => {
      $(formResult).empty();
    }, 3000);
  });
});
