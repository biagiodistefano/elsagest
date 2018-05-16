import './soci-loader';
import './aggiungi-socio';


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
