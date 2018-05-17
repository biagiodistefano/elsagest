import './aggiungi-socio';
import SociLoader from './soci-loader';


$('#btn-aggiungi-socio').on('click', () => {
  $('#modal-aggiungi-socio').modal('show');
});

$('.lista-soci tr').on('click', () => {
  $('#modal-modifica-socio').modal('show');
});


$('.datepicker-modal').datepicker({
  format: 'dd-mm-yyyy',
  maxViewMode: 2,
  language: 'it',
  autoclose: true,
  todayHighlight: true,
  todayBtn: 'linked',
  //startDate: firstDay.toDate(),
  //endDate: lastDay.toDate(),
  ignoreReadonly: true
});

// eslint-disable-next-line no-new
new SociLoader();
