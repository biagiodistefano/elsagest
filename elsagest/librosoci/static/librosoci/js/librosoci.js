//import datepickerSettings from 'common/js/datepicker-settings';
import 'elsamail/js/email';
import './aggiungi-socio';
import './modifica-socio';
import SociLoader from './soci-loader';


//$('.datepicker-modal').datepicker(datepickerSettings);

SociLoader.fetchSoci();
SociLoader.fetchConsiglieri();
