export default consigliere => {
  const item = $(`<tr>
            <input type="hidden" value="${consigliere.socio.id}">
            <td class="cognome">${consigliere.socio.cognome}</td>
            <td class="nome">${consigliere.socio.nome}</td>
            <td class="ruolo">${consigliere.ruolo.ruolo}</td>
            <td class="sezione">${consigliere.socio.sezione.denominazione}</td>
            <td class="email"><a href="mailto:${consigliere.email}">${consigliere.email}</a></td>
            <td class="consigliere-dal">${consigliere.inCaricaDal}</td>
        </tr>`);
  return item;
};
