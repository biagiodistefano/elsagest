export default {
  MOMENT_DATE_FORMAT: 'DD/MM/YYYY',

  TICKS_ENABLED: true,
  MAX_SEARCH_PREVIEW_CHARS: 100,
  MIN_SEARCH_LENGTH: 2,
  SEARCH_RESULTS_HIGHLIGHT_CLASS: 'highlight',
  SOCI_MIN_RESULTS: 10,

  HIDDEN_CLASS: 'les--hidden',
  HIDDEN_SIMPLE_MODE_CLASS: 'les--hidden-simple-mode',
  HIDDEN_COMMI_NUMBER: 'les--hidden-commi-number',
  HIDDEN_SEARCH_PANEL: 'les--hidden-search-panel',
  HIDDEN_ERROR_SEARCH_PANEL: 'les--hidden-error-search-panel',
  HIDDEN_ERROR_LEGGI_MODIFICA: 'les--hidden-error-leggi-modifica',
  HIDDEN_EMPTY_LEGGI_MODIFICA: 'les--hidden-empty-leggi-modifica',
  HIDDEN_PRINTABLE_VERSION: 'les--hidden-printable-version',

  HIDDEN_MODAL_ELEMENT: 'les--hidden-modal-element',
  MODAL_DOUBLE_PANEL_ENABLED: true,
  MODAL_SHOW_EDITS_ENABLED: false,
  MODAL_LOCK_SYNC_ENABLED: true,

  ATTO_OPAQUE_CLASS: 'les__atto--opaque',
  ATTO_BLURRED_CLASS: 'les__atto--blurred',
  MENU_INVISIBLE_CLASS: 'les__menu--invisible',
  MOBILE_MENU_WIDTH_TRIGGER: 768,

  // here we add a bunch of classes that are toggled dynamically
  // N.B: these need to stay on sync with templates!
  MOBILE_MENU_DEFAULT_CLASSES: 'les__menu hidden-xs col-sm-4 col-md-3',
  MOBILE_MENU_VISIBLE_CLASSES:
    'les__menu les__menu--mobile les__menu--invisible hidden-sm hidden-md hidden-lg',
  MOBILE_MENU_CLOSED_CLASSES: 'les__menu hidden-xs hidden-sm hidden-md hidden-lg',

  ATTO_WRAPPER_DEFAULT_CLASSES: 'les__atto-wrapper col-xs-12 col-sm-8 col-md-9',
  ATTO_WRAPPER_FULL_WIDTH_CLASSES: 'les__atto-wrapper col-xs-12'
};
