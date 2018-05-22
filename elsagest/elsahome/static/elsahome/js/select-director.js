export default () => $(`<div class="row row-director">
    <div class="col-md-3 col-sm-3">
        <div class="form-group">
            <select name="ruolo" class="form-control">
                <option value="21">Director IM</option>
                <option value="22">Director Tesoreria</option>
                <option value="23">Director Marketing</option>
                <option value="24">Director Attività Accademiche</option>
                <option value="25">Director Seminari e Conferenze</option>
                <option value="26">Director STEP</option>
                <option value="0">Rimuovi Director</option>
            </select>
        </div>
    </div>
    <div class="col-md-3 col-sm-3">
        <div class="form-group">
            <input name="ruolo" class="form-control consiglio-autocomplete" autocomplete="off" required>
            </input>
        </div>
    </div>
    <div class="col-md-3 col-sm-3">
        <div class="form-group">
            <input name="ruolo" class="form-control email-istituzionale"
            type="email" autocomplete="off" placeholder="Email istituzionale" required>
            </input>
        </div>
    </div>
    <div class="col-md-3 col-sm-3">
        <div class="form-group">
            <input name="ruolo" class="datepicker-modal text-center form-control" type="text" required>
        </div>
    </div>
</div>
`);
