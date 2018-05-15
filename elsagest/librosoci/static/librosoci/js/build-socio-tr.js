export default socio => $(`<tr>
                <td>${socio.nome}</td>
                <td>${socio.cognome}</td>
                <td>${socio.email}</td>
                <td>${socio.dataIscrizione}</td>
                <td>${socio.scadenzaIscrizione}</td>
            </tr>`);
