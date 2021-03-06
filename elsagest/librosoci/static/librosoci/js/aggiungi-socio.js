import datepickerSettings from 'common/js/datepicker-settings';
import SociLoader from './soci-loader';

const modalAggiungiSocio = $('#modal-aggiungi-socio');


$('#btn-aggiungi-socio').on('click', () => {
  modalAggiungiSocio.modal('show');
  modalAggiungiSocio.find('.datepicker-modal').datepicker(datepickerSettings);
});

modalAggiungiSocio.on('hide.bs.modal', () => {
  modalAggiungiSocio.find('.datepicker-modal').datepicker('destroy');
});


$('#form-aggiungi-socio').submit(event => {
  event.preventDefault();
  const $this = $(event.currentTarget);
  const formResult = $this.find('.form-result');
  formResult.append($(
    `
    <div class="loader">
      <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
    </div>
    `
  ));
  $this.find('button[type="submit"]').attr('disabled', true);
  const datastring = $(event.currentTarget).serialize();
  $.post({
    url: '/librosoci/aggiungisocio/',
    data: datastring,
    dataType: 'json'
  }
  ).done(response => {
    const { success } = response;
    $(formResult).empty();
    if (success) {
      $(formResult).append($('<h4 class="text-center text-success bg-success">Nuovo socio aggiunto!</h4>'));
    } else {
      $(formResult).append($('<h4 class="text-center text-danger bg-danger">Si è verificato un errore</h4>'));
    }
  }).fail(() => {
    $(formResult).empty();
    $(formResult).append($('<h4 class="text-center text-danger bg-danger">Si è verificato un errore</h4>'));
  }).always(() => {
    formResult.find('.loader').remove();
    setTimeout(() => {
      $(formResult).empty();
      $this.find('button[type="submit"]').attr('disabled', false);
      SociLoader.init();
      SociLoader.fetchSoci(true);
      $this.trigger('reset');
    }, 3000);
  });
});
