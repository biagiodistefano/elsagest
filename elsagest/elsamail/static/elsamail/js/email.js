import SociLoader from 'librosoci/js/soci-loader';
import EmailLoader from './email-loader';

$('#email-promemoria').submit(evt => {
  evt.preventDefault();
  const $this = $(evt.currentTarget);
  const action = $this.attr('action');
  const formResult = $($this.find('.form-result'));
  formResult.append($(
    `
    <div class="loader">
      <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
    </div>
    `
  ));
  $this.find('button[type="submit"]').attr('disabled', true);
  $.post({
    url: action,
    data: { dry: true },
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
    formResult.find('.loader').remove();
    setTimeout(() => {
      $this.find('button[type="submit"]').attr('disabled', false);
      $(formResult).empty();
      SociLoader.init();
      SociLoader.fetchSoci(true);
    }, 5000);
  });
});

$('#new_email').summernote({ dialogsInBody: true, height: 300 });

$('#form-invia-email').submit(evt => {
  evt.preventDefault();
  const $this = $(evt.currentTarget);
  const action = $this.attr('action');
  const formResult = $($this.find('.form-result'));
  formResult.append($(
    `
    <div class="loader">
      <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
    </div>
    `
  ));
  $this.find('button[type="submit"]').attr('disabled', true);
  const datastring = $this.serialize();
  $.post({
    url: action,
    data: datastring,
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
    formResult.find('.loader').remove();
    $this.find('button[type="submit"]').attr('disabled', false);
    setTimeout(() => {
      $(formResult).empty();
    }, 5000);
  });
});

$('#btn-salva-bozza').click(evt => {
  const $this = $(evt.currentTarget);
  $this.attr('disabled', true);
  const oggetto = $('#oggetto-email').val();
  const corpo = $('#new_email').val();
  const disponibilePer = $('#disponibile-per option:selected').val();
  const formResult = $($this.parent().parent().parent().find('.form-result'));
  $.post({
    url: '/elsamail/salva-bozza/',
    data: { oggetto, corpo, disponibilePer },
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
    formResult.append($(`<div class="alert alert-dangerè alert-dismissible fade in">
    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
    Si è verificato un errore: ${err}
    </div>`));
  }).always(() => {
    setTimeout(() => {
      $this.attr('disabled', false);
      $(formResult).empty();
      EmailLoader.fetchBozze(true);
    }, 3000);
  });
});

$(document).on('click', '.btn-usa-bozza', evt => {
  const $this = $(evt.currentTarget);
  const panel = $this.parent().parent().parent();
  const oggetto = $(panel).find('.panel-title').text();
  const corpo = $(panel).find('.corpo-email').html();
  $('#oggetto-email').val(oggetto);
  $('#new_email').summernote('code', corpo);
  $('html, body').animate({ scrollTop: 0 });
});

$(document).on('submit', '.form-elimina-bozza', evt => {
  evt.preventDefault();
  const $this = $(evt.currentTarget);
  const action = $this.attr('action');
  const formResult = $($this.find('.form-result'));
  formResult.append($(
    `
    <div class="loader">
      <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
    </div>
    `
  ));
  $this.find('button[type="submit"]').attr('disabled', true);
  const datastring = $this.serialize();
  $.post({
    url: action,
    data: datastring,
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
    const messageBox = $(`<div class="alert alert-danger alert-dismissible fade in">
    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
    Si è verificato un errore: ${err}
    </div>`);
    formResult.append(messageBox);
  }).always(() => {
    formResult.find('.loader').remove();
    setTimeout(() => {
      $(formResult).empty();
      EmailLoader.fetchBozze(true);
    }, 1000);
  });
});

EmailLoader.fetchEmail(true);
EmailLoader.fetchBozze(true);
