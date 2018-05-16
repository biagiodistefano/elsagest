import moment from 'moment';
import config from './config';

export default socio => {
  const tr = $(`<tr>
            <input type="hidden" value="${socio.id}">
            <td class="cognome">${socio.cognome}</td>
            <td class="nome">${socio.nome}</td>
            <td class="numero-tessera">${socio.numeroTessera}</td>
            <td class="email">${socio.email}</td>
            <td class="data-iscrizione">${socio.dataIscrizione}</td>
            <td class="ultimo-rinnovo">${socio.ultimoRinnovo}</td>
            <td class="scadenza-iscrizione">${socio.scadenzaIscrizione}</td>
        </tr>`);
  const scadenza = moment(socio.scadenzaIscrizione, config.MOMENT_DATE_FORMAT);
  if (scadenza.isBefore(moment())) {
    $(tr).addClass('danger');
  }
  return tr;
};
