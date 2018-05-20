export default consigliere => {
  const item = $(`<tr>
            <input type="hidden" value="${consigliere.socio.id}">
            <td class="cognome">${consigliere.socio.cognome}</td>
            <td class="nome">${consigliere.socio.nome}</td>
            <td class="ruolo">${consigliere.ruolo.ruolo}</td>
            <td class="sezione">${consigliere.socio.sezione.nome}</td>
            <td class="email">nessuna@example.elsa</td>
            <td class="consigliere-dal">${consigliere.inCaricaDal}</td>
        </tr>`);
  return item;
};
