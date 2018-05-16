import SociLoader from './soci-loader';

$('#form-aggiungi-socio').submit(event => {
  event.preventDefault();
  const datastring = $(event.currentTarget).serialize();
  $.post({
    url: '/librosoci/aggiungisocio/',
    data: datastring,
    dataType: 'json'
  }
  ).done(response => {
    const { success } = response;
    const formResult = $('#form-aggiungi-socio-result');
    $(formResult).empty();
    if (success) {
      $(formResult).append($('<h4 class="text-center text-success bg-success">Nuovo socio aggiunto!</h4>'));
      $('#form-aggiungi-socio').trigger('reset');
      SociLoader.fetchSoci();
    } else {
      $(formResult).append($('<h4 class="text-center text-danger bg-danger">Si è verificato un errore</h4>'));
    }
  }).fail(() => {
    const formResult = $('#form-aggiungi-socio-result');
    $(formResult).empty();
    $(formResult).append($('<h4 class="text-center text-danger bg-danger">Si è verificato un errore</h4>'));
  }).always(() => {
    const formResult = $('#form-aggiungi-socio-result');
    setTimeout(() => {
      $(formResult).empty();
    }, 3000);
  });
});
