import config from './config';
import buildSocioTr from './build-socio-tr';

const deltaScrollPx = 30;

class SociLoader {
  constructor() {
    console.log('DIO ABBAIA CONSTRUCTOR');
    this.cleanup();
    this.init();
  }

  init() {
    console.log('DIO ABBAIA INIT');
    this.cleanup();
    this.fetchTuttiSoci();
    this.fetchSociScadenza();
  }

  fetchTuttiSoci() {
    SociLoader.addLoader('#tutti-i-soci tbody');
    const query = `
      {
        allSoci(
          first: ${config.SOCI_MIN_RESULTS},
          after: "${this.state.lastItemId || ''}"
          ) {
          edges {
              node {
                nome
                cognome
                email
                dataIscrizione
                scadenzaIscrizione
              }
            }
            pageInfo {
              startCursor
              endCursor
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
        const { infiniteScrollInit } = this.state;
        const { pageInfo, edges } = response.data.allSoci;
        const { hasNextPage, endCursor } = pageInfo;

        // update local data structures with graphql help
        this.state.canFetchMore = hasNextPage;
        this.state.lastItemId = endCursor || null;

        if (edges.length > 0) {
          // populate panel with results
          const wrapper = $('#tutti-i-soci tbody');
          console.log(wrapper);
          edges.forEach(edge => {
            const item = buildSocioTr(edge.node);
            wrapper.append(item);
          });

          // init infinite scroll
          if (!infiniteScrollInit) {
            this.state.infiniteScrollInit = true;
            this.state.infiniteScrollEnabled = true;
            this.initInfiniteScroll();
          }

          // enable infinite scroll again
          this.state.infiniteScrollEnabled = true;
        } else {
          // show 'no results' message
          $('#tutti-i-soci tbody').append(
            $(
              `
              <div class="no-results">
                <p>Nessun risultato trovato</p>
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
        SociLoader.removeLoader();
      });
  }

  fetchSociScadenza() {
    SociLoader.addLoader('#soci-in-scadenza tbody');
    const query = `
      {
        allSoci(
          scadenza: "True"
          ) {
          edges {
              node {
                nome
                cognome
                email
                dataIscrizione
                scadenzaIscrizione
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
          const wrapper = $('#soci-in-scadenza tbody');
          console.log(wrapper);
          edges.forEach(edge => {
            const item = buildSocioTr(edge.node);
            wrapper.append(item);
          });

          // enable infinite scroll again
        } else {
          // show 'no results' message
          $('#soci-in-scadenza tbody').append(
            $(
              `
              <div class="no-results">
                <p>Nessun socio in scadenza</p>
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
        SociLoader.removeLoader();
      });
  }

  initInfiniteScroll() {
    $('.les__modal-sentenze .modal-body').scroll(evt => {
      const target = $(evt.target);
      const { infiniteScrollEnabled, canFetchMore } = this.state;

      if (
        infiniteScrollEnabled &&
        canFetchMore &&
        target.scrollTop() + target.innerHeight() >= target.get(0).scrollHeight - deltaScrollPx
      ) {
        // fetch additional items
        this.state.infiniteScrollEnabled = false;

        this.fetchItems();
      }
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

  static removeLoader() {
    $('#tutti-i-soci tbody')
      .find('.loader')
      .remove();
  }

  cleanup() {
    $('#tutti-i-soci tbody').empty();

    this.state = {
      infiniteScrollInit: false,
      infiniteScrollEnabled: false,
      lastItemId: null,
      canFetchMore: false
    };
  }
}

const soci = new SociLoader();
soci.init();
