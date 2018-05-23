export default email => $(`<div class="panel panel-default panel-email">
                <div class="panel-heading">
                    <h3 class="panel-title">${email.oggetto}</h3>
                </div>
                <div class="panel-body">
                    <div class="row corpo-email">${email.corpo}</div>
                    
                    </div>
                </div>
            </div>`);
