// per fare le richieste al server
// c'è un problema di sicurezza quanto una casa
const csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

$.ajaxSetup({
  beforeSend: (xhr, settings) => {
    if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});
