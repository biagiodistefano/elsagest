import config from './config';
import buildSocioTr from './build-socio-tr';
import buildConsigliereTr from './build-consigliere-tr';

class SociLoader {
  constructor() {
    this.init();
  }

  init() {
    this.fetchSoci();
    this.fetchConsiglieri();
  }

  fetchSoci() {
    $('.table-soci').each((index, table) => {
      const target = $(table).find('.lista-soci');

      $(target).empty();

      let first = '';
      let scadenza = '';

      if ($(target).attr('data-first')) {
        first = `first: ${config.SOCI_MIN_RESULTS}`;
      }
      if ($(target).attr('data-scadenza')) {
        scadenza = 'scadenza: true';
      }

      const orderby = 'orderby: "cognome"';

      const settings = [first, scadenza, orderby].join(', ');

      SociLoader.addLoader(target);
      const query = `
        {
          allSoci(
            ${settings}
            ) {
            edges {
                node {
                  id
                  nome
                  cognome
                  numeroTessera
                  email
                  dataIscrizione
                  ultimoRinnovo
                  scadenzaIscrizione
                }
              }
              pageInfo {
                hasNextPage
              }
            }
          }
      `;

      $.post({
        url: '/graphql/',
        data: JSON.stringify({ query }),
        contentType: 'application/json'
      })
        .done(response => {
          console.log(response.data);
          const { pageInfo, edges } = response.data.allSoci;
          const { hasNextPage } = pageInfo;
          if (edges.length > 0) {
            // populate panel with results
            const wrapper = $(target);
            console.log(wrapper);
            edges.forEach(edge => {
              const item = buildSocioTr(edge.node);
              wrapper.append(item);
            });

            if (scadenza) {
              $('#soci-in-scadenza h3 button').removeClass('hidden');
            }

            if (hasNextPage) {
              $(table).append($('<a target="_blank" href="/librosoci" class="float-right">Vedi tutti</a>'));
            }
          } else {
            // show 'no results' message
            $(target).append(
              $(
                `
                <div class="no-results">
                  <p>Ottimo, nessun socio in scadenza!</p>
                </div>
                `
              )
            );
          }
        })
        .fail(err => {
          console.log(err);
          this.handleError();
        })
        .always(() => {
          SociLoader.removeLoader(target);
        });
    });
  }

  fetchConsiglieri() {
    $('.table-consiglio-direttivo').each((index, table) => {
      const target = $(table).find('.lista-consiglieri');
      $(target).empty();
      SociLoader.addLoader(target);
      const query = `
        {
          allSoci(consiglieri: true){
            edges{
              node{
                id
                nome
                cognome
                ruolo{
                  ruolo
                }
                consigliereDal
                emailconsigliere{
                  email
                }
              }
            }
          }
        }
      `;

      $.post({
        url: '/graphql/',
        data: JSON.stringify({ query }),
        contentType: 'application/json'
      })
        .done(response => {
          const { edges } = response.data.allSoci;
          if (edges.length > 0) {
            // populate panel with results
            const wrapper = $(target);
            console.log(wrapper);
            edges.forEach(edge => {
              const item = buildConsigliereTr(edge.node);
              wrapper.append(item);
            });
          } else {
            // show 'no results' message
            $(target).append(
              $(
                `
                <div class="no-results">
                  <p>Ooops, nessun consigliere trovato!</p>
                </div>
                `
              )
            );
          }
        })
        .fail(err => {
          console.log(err);
          this.handleError();
        })
        .always(() => {
          SociLoader.removeLoader(target);
        });
    });
  }

  handleError() {
    // prevent infinite scroll from triggering
    this.state.infiniteScrollEnabled = false;
  }

  static addLoader(target) {
    $(target).append(
      $(
        `
        <div class="loader">
          <i class="fa fa-spinner fa-spin fa-3x fa-fw"></i>
        </div>
        `
      )
    );
  }

  static removeLoader(target) {
    $(target)
      .find('.loader')
      .remove();
  }
}

export default new SociLoader();
