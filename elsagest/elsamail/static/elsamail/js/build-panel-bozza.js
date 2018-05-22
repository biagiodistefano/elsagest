
export default bozza => {
  const template = $(`<div class="panel panel-default panel-email">
                <div class="panel-heading">
                    <h3 class="panel-title">${bozza.oggetto}</h3>
                </div>
                <div class="panel-body">
                    <div class="row corpo-email">${bozza.corpo}</div>
                    <div class="row azioni-bozza">
                    <button class="btn btn-primary btn-elsagest btn-usa-bozza float-right" type="button">
                    Usa
                    </button>
                    </div>
                </div>
            </div>`);
  if (bozza.canDelete) {
    template.find('.azioni-bozza').append($(`
<form action="/elsamail/elimina-bozza/" class="form-elimina-bozza">
<input name="id" type="hidden" value="${bozza.id}">
<button class="btn btn-danger btn-elsagest btn-elimina-bozza float-right" type="submit">Elimina</button>
<div class="form-result"></div>
</form>`));
  }
  return template;
};
