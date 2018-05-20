import datepickerSettings from 'common/js/datepicker-settings';

const modalConsiglioDirettivo = $('#modal-consiglio-direttivo');

$('.datepicker-modal').datepicker(datepickerSettings);

$('#aggiorna-consiglio').click(() => {
  modalConsiglioDirettivo.modal();
  //modalConsiglioDirettivo.find('.datepicker-modal').datepicker(datepickerSettings);
});


const formConsiglio = $('#modal-consiglio-direttivo').find('form');

// modalConsiglioDirettivo.on('hide.bs.modal', () => {
//   formConsiglio.trigger('reset');
// });


formConsiglio.on('focus', '.consiglio-autocomplete', evt => {
  const $this = $(evt.currentTarget);
  $this.autocomplete({
    source: (request, response) => {
      const query = `
        {
          allSoci(first: 50, search: "${request.term}"){
            edges{
              node{
                id
                nome
                cognome
                codiceFiscale
                sezione {
                  id
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
        .done(jresponse => {
          const { allSoci } = jresponse.data;
          const { edges } = allSoci;
          const results = [];
          edges.forEach(edge => {
            const { node } = edge;
            const result = { value: `${node.nome} ${node.cognome}`, id: node.id };
            results.push(result);
          });
          response(results);
        });
    },
    select: (event, ui) => {
      $this.val(ui.item.id);
      $this.attr('data-id', ui.item.id);
      $this.attr('data-label', ui.item.value);
    }
  });
});

formConsiglio.submit(evt => {
  evt.preventDefault();
  const $this = $(evt.currentTarget);
  const formResult = $($this.find('.form-result'));
  $this.find('.consiglio-autocomplete').each((idx, elm) => {
    $(elm).val($(elm).attr('data-id'));
  });
  const datastring = $this.serialize();
  $this.find('.consiglio-autocomplete').each((idx, elm) => {
    $(elm).val($(elm).attr('data-label'));
  });
  $.post({
    url: '/librosoci/modificaconsiglio/',
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
    ${err}
    </div>`);
    formResult.append(messageBox);
  }).always(() => {
    setTimeout(() => {
      $(formResult).empty();
    }, 30000);
  });
});

$('.btn-nuovo-director').on('click', evt => {
  const $this = $(evt.currentTarget);
  //const thisParent = $($this.parent());
  const nuovoDirector = $(`<div class="row">
                      <div class="col-md-4 col-sm-4">
                          <div class="form-group">
                              <select name="ruolo" class="form-control">
                              <option value="21">Director IM</option>
                              <option value="22">Director Tesoreria</option>
                              <option value="23">Director Marketing</option>
                              <option value="24">Director Attività Accademice</option>
                              <option value="25">Director Seminari e Conferenze</option>
                              <option value="26">Director STEP</option>
                              <option value="0">Rimuovi Director</option>
                              </select>
                          </div>
                      </div>
                      <div class="col-md-4 col-sm-4">
                          <div class="form-group">
                              <input name="vpstep" class="form-control consiglio-autocomplete" autocomplete="off" required>
                              </input>
                          </div>
                      </div>
                      <div class="col-md-4 col-sm-4">
                          <div class="form-group">
                              <input class="datepicker-modal text-center form-control" type="text" required>
                          </div>
                      </div>
                  </div>
                    
                  </div>
                  </div>`);
  nuovoDirector.find('.datepicker-modal').datepicker(datepickerSettings);
  nuovoDirector.on('change', 'select', selevt => {
    const select = $(selevt.currentTarget);
    if (select.val() === '0') {
      select.parent().parent().parent().remove();
    }
  });
  $(nuovoDirector).insertBefore($this);
});

