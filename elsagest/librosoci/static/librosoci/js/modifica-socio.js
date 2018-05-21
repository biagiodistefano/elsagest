import datepickerSettings from 'common/js/datepicker-settings';
import SociLoader from './soci-loader';

const modalModificaSocio = $('#modal-modifica-socio');


const caricaInfoSocio = socioId => {
  const editForm = $('#form-modifica-socio');
  $(editForm).trigger('reset'); // per sicurezza
  const query = `
    {
      socio(id: "${socioId}"){
        id
        nome
        cognome
        numeroTessera
        email
        dataIscrizione
        ultimoRinnovo
        scadenzaIscrizione
        codiceFiscale
        quotaIscrizione
        rinnovoiscrizioneSet{
          edges{
            node{
              id
              dataRinnovo
              quotaRinnovo
            }
          }
        }
      }
    }
  `;
  $.post({
    url: '/graphql/',
    data: JSON.stringify({ query }),
    contentType: 'application/json'
  })
    .done(response => {
      const { socio } = response.data;
      const rinnoviPrecedenti = $(editForm).find('.rinnovi-iscrizione-precedenti');
      $(rinnoviPrecedenti).empty();
      socio.dataIscrizione = socio.dataIscrizione.split('-').reverse().join('-');
      socio.scadenzaIscrizione = socio.dataIscrizione.split('-').reverse().join('-');
      Object.keys(socio).forEach(key => {
        if (key !== 'rinnovoiscrizioneSet') {
          const name = key.split(/(?=[A-Z])/).join('_').toLowerCase();
          const value = socio[key];
          $(editForm).find(`input[name="${name}"]`).val(value);
        }
      });
      const { rinnovoiscrizioneSet } = socio;
      const { edges } = rinnovoiscrizioneSet;
      if (edges.length) {
        $(rinnoviPrecedenti).append('<label>Rinnovi precedenti</label>');
        edges.forEach(edge => {
          const rinnovo = edge.node;
          const rinnovoPrecedente = $('<div class="rinnovo-precedente"></div>');
          const idRinnovo = $(`<input type="hidden" name="rinnovo_id" value="${rinnovo.id}"/>`);
          const dataRinnovo = $(` <div class="col-xs-6 col-md-6">
            <input class="form-control datepicker-modal" name="data_rinnovo"
                   placeholder="Data rinnovo (dd-mm-aaaa)" type="text" value="${rinnovo.dataRinnovo.split('-').reverse().join('-')}"
                   required autofocus/></div>`);
          const quotaRinnovo = $(`<div class="col-xs-6 col-md-6">
                                  <input class="form-control" name="quota_rinnovo" placeholder="Quota rinnovo (EUR)"
                                         type="text" value="${rinnovo.quotaRinnovo}"
                                         required/>
                              </div>`);
          $(rinnovoPrecedente).append(idRinnovo);
          $(rinnovoPrecedente).append(dataRinnovo);
          $(rinnovoPrecedente).append(quotaRinnovo);
          $(rinnovoPrecedente).appendTo($(rinnoviPrecedenti));
        });
      }
      editForm.find('.datepicker-modal').datepicker(datepickerSettings);
    })
    .fail()
    .always();
};


$(document).on('click', '.lista-soci tr', evt => {
  caricaInfoSocio($(evt.currentTarget).find('input').val());
  modalModificaSocio.modal('show');
  modalModificaSocio.find('.datepicker-modal').datepicker(datepickerSettings);
});

modalModificaSocio.on('hide.bs.modal', () => {
  modalModificaSocio.find('.datepicker-modal').datepicker('destroy');
});


$('#form-modifica-socio').submit(event => {
  event.preventDefault();
  const $this = $(event.currentTarget);
  const formResult = $this.find('.form-result');
  const datastring = $(event.currentTarget).serialize();
  $.post({
    url: '/librosoci/modificasocio/',
    data: datastring,
    dataType: 'json'
  }
  ).done(response => {
    const { success, message } = response;
    $(formResult).empty();
    console.log(formResult);
    if (success) {
      $(formResult).append($(`<h4 class="text-center text-success bg-success">${message}</h4>`));
    } else {
      $(formResult).append($(`<h4 class="text-center text-danger bg-danger">${message}</h4>`));
    }
  }).fail(() => {
    $(formResult).empty();
    $(formResult).append($('<h4 class="text-center text-danger bg-danger">Si è verificato un errore</h4>'));
  }).always(() => {
    setTimeout(() => {
      $(formResult).empty();
      SociLoader.init();
      SociLoader.fetchSoci(true);
    }, 3000);
  });
});

$('#chiudi-modal-modifica-socio').on('click', () => {
  const editForm = $('#form-modifica-socio');
  const rinnBtn = editForm.find('.btn-nuovo-rinnovo');
  const nuovoRinn = editForm.find('.nuovo-rinnovo');
  if (nuovoRinn.length) {
    nuovoRinn.remove();
  }
  rinnBtn.attr('data-action', 'add');
  rinnBtn.text('Nuovo rinnovo');
});


$('#ripristina-info-socio').on('click', () => {
  caricaInfoSocio($('#form-modifica-socio').find('input[name="id"]').val());
});


$('.btn-nuovo-rinnovo').on('click', evt => {
  const $this = $(evt.currentTarget);
  const thisParent = $($this.parent());
  if ($this.attr('data-action') === 'add') {
    const nuovoRinnovo = $(`<div class="nuovo-rinnovo">
                    <div class="col-xs-6 col-md-6">
                        <input class="form-control datepicker-modal" name="data_nuovo_rinnovo"
                               placeholder="Data rinnovo (dd-mm-aaaa)" type="text"
                                autofocus/>
                    </div>
                    <div class="col-xs-6 col-md-6">
                        <input class="form-control" name="quota_nuovo_rinnovo" placeholder="Quota rinnovo (EUR)"
                               type="text"
                               />
                    </div>
                    </div>`);
    nuovoRinnovo.find('.datepicker-modal').datepicker(datepickerSettings);
    thisParent.append(nuovoRinnovo);
    $this.attr('data-action', 'remove');
    $this.text('Annulla');
  } else {
    thisParent.find('.nuovo-rinnovo').remove();
    $this.attr('data-action', 'add');
    $this.text('Nuovo rinnovo');
  }
});
