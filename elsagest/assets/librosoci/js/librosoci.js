//import datepickerSettings from 'common/js/datepicker-settings';
import 'elsamail/js/email';
import './aggiungi-socio';
import './modifica-socio';
import SociLoader from './soci-loader';


//$('.datepicker-modal').datepicker(datepickerSettings);

SociLoader.fetchSoci();
SociLoader.fetchConsiglieri();
const sezioneOriginale = $('#table-consiglieri').attr('data-sezione');


$('#select-soci').change(evt => {
  const $this = $(evt.currentTarget);
  const sezione = $this.find('option:selected').val();
  $('#table-soci').attr('data-sezione', sezione);
  SociLoader.init();
  SociLoader.fetchSoci(true);
});

$('#select-sezioni').change(evt => {
  const $this = $(evt.currentTarget);
  const sezione = $this.find('option:selected').val();
  $('#table-consiglieri').attr('data-sezione', sezione);
  if (sezione !== sezioneOriginale) {
    $('#aggiorna-consiglio').attr('disabled', true);
  } else {
    $('#aggiorna-consiglio').attr('disabled', false);
  }
  SociLoader.init();
  SociLoader.fetchConsiglieri(true);
});
