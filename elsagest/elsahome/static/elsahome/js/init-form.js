import selectDirector from 'elsahome/js/select-director';

const formConsiglio = $('#form-modifica-consiglio');

export default consiglieri => {
  consiglieri.forEach(consigliere => {
    const { ruolo, inCaricaDal, socio } = consigliere;
    console.log(ruolo);
    let row, dir, input, data;
    if (ruolo.ruolo.indexOf('Presidente') > -1) {
      row = formConsiglio.find('#row-presidente');
    } else if (ruolo.ruolo.indexOf('Segretario') > -1) {
      row = formConsiglio.find('#row-secgen');
    } else if (ruolo.ruolo.indexOf('Tesor') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '22';
      } else {
        row = formConsiglio.find('#row-tesoriere');
      }
    } else if (ruolo.ruolo.indexOf('Marketing') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '23';
      } else {
        row = formConsiglio.find('#row-vpmkt');
      }
    } else if (ruolo.ruolo.indexOf('Accademiche') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '24';
      } else {
        row = formConsiglio.find('#row-vpaa');
      }
    } else if (ruolo.ruolo.indexOf('Seminari') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '25';
      } else {
        row = formConsiglio.find('#row-vpsc');
      }
    } else if (ruolo.ruolo.indexOf('STEP') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '26';
      } else {
        row = formConsiglio.find('#row-vpstep');
      }
    } else if (ruolo.ruolo.indexOf('IM') > -1) {
      if (ruolo.ruolo.indexOf('Director') > -1) {
        dir = '21';
      } else {
        row = formConsiglio.find('#row-secgen');
      }
    }
    if (row) {
      input = row.find('input.consiglio-autocomplete');
      data = row.find('input.datepicker-modal');
    } else if (dir) {
      const nuovoDirector = selectDirector();
      nuovoDirector.find(`option[value="${dir}"]`).attr('selected', true);
      input = nuovoDirector.find('input.consiglio-autocomplete');
      data = nuovoDirector.find('input.datepicker-modal');
      nuovoDirector.insertBefore(formConsiglio.find('.btn-nuovo-director'));
    }
    input.val(`${socio.nome} ${socio.cognome}`);
    input.attr('data-id', socio.id);
    input.attr('data-label', `${socio.nome} ${socio.cognome}`);
    data.val(inCaricaDal);
  });
};
