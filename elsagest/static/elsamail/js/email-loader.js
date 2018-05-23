import buildPanelEmail from './build-panel-email';
import buildPanelBozza from './build-panel-bozza';

const deltaScrollPx = 30;

class EmailLoader {
  constructor() {
    this.init();
  }

  init() {
    this.cleanup();
  }

  fetchBozze(empty) {
    const target = $('#bozze-email');
    if ($(target).length) {
      if (empty) {
        $(target).find('.tab-pane').empty();
      }
      EmailLoader.addLoader(target);
      const query = `
        {
          allBozze{
            id
            oggetto
            corpo
            disponibilePer
            canDelete
          }
        }
      `;
      $.post({
        url: '/graphql/',
        data: JSON.stringify({ query }),
        contentType: 'application/json'
      })
        .done(response => {
          const { allBozze } = response.data;
          EmailLoader.removeLoader(target);
          if (allBozze.length > 0) {
            // populate panel with results
            allBozze.forEach(bozza => {
              const item = buildPanelBozza(bozza);
              let wrapper;
              switch (bozza.disponibilePer) {
                case 0:
                  wrapper = $('#tab-mie-bozze');
                  break;
                case 1:
                  wrapper = $('#tab-bozze-sezione');
                  break;
                case 2:
                  wrapper = $('#tab-bozze-nazionali');
                  break;
                default:
                  wrapper = $('#tab-mie-bozze');
              }
              wrapper.append(item);
            });
          }
          target.find('.tab-pane').each((index, tab) => {
            if (!$(tab).find('.panel-email').length) {
              $(tab).append(
                $(
                  `
                  <div class="no-results">
                    <p>Nessuna bozza disponibile!</p>
                  </div>
                  `
                )
              );
            }
          });
        })
        .fail(() => {
          EmailLoader.removeLoader(target);
          this.handleError();
        })
        .always(() => {
          EmailLoader.removeLoader(target);
        });
    }
  }
  fetchEmail(empty) {
    const target = $('#lista-email');
    if ($(target).length) {
      if (empty) {
        $(target).empty();
      }
      EmailLoader.addLoader(target);
      const query = `
        {
          allEmails(first: 5) {
            edges {
              node {
                oggetto
                corpo
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
          const { allEmails } = response.data;
          const { edges } = allEmails;
          EmailLoader.removeLoader(target);
          if (edges.length > 0) {
            // populate panel with results
            edges.forEach(edge => {
              const item = buildPanelEmail(edge.node);
              target.append(item);
            });
          } else {
            $(target).append(
              $(
                `
                <div class="no-results">
                  <p>Nessuna email disponibile!</p>
                </div>
                `
              )
            );
          }
        })
        .fail(() => {
          EmailLoader.removeLoader(target);
          this.handleError();
        })
        .always(() => {
          EmailLoader.removeLoader(target);
        });
    }
  }
  initInfiniteScroll() {
    $(window).scroll(() => {
      const { infiniteScrollEnabled, canFetchMore } = this.state;
      if (
        infiniteScrollEnabled &&
        canFetchMore &&
        ($(window).scrollTop() + $(window).height() > $(document).height() - deltaScrollPx)
      ) {
        // fetch additional items
        this.state.infiniteScrollEnabled = false;
        this.fetchSoci(false);
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

  static removeLoader(target) {
    $(target)
      .find('.loader')
      .remove();
  }

  cleanup() {
    this.state = {
      infiniteScrollInit: false,
      infiniteScrollEnabled: false,
      lastItemId: null,
      canFetchMore: false
    };
  }
}


export default new EmailLoader();
