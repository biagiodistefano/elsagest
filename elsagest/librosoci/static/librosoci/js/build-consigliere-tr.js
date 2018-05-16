export default consigliere => {
  const {
    id, nome, cognome, ruolo, consigliereDal, emailconsigliere
  } = consigliere;
  const item = $(`<tr>
            <input type="hidden" value="${id}">
            <td class="cognome">${cognome}</td>
            <td class="nome">${nome}</td>
            <td class="ruolo">${ruolo.ruolo}</td>
            <td class="email">${emailconsigliere.email}</td>
            <td class="consigliere-dal">${consigliereDal}</td>
        </tr>`);
  return item;
};
