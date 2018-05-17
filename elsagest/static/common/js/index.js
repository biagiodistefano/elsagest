import '../css/common.scss';
import './helpers/csrf';
import './helpers/date-picker';
import './helpers/copy-tooltip-handler';
import './helpers/save-sentenza-handler';
import copyToClipboard from './helpers/copy-to-clipboard';
import delay from './helpers/delay';
import setTooltip from './helpers/set-tooltip';
import hideTooltip from './helpers/hide-tooltip';
import doc from './helpers/doc-jspdf';
import specialElementHandlers from './helpers/special-element-handlers';
import salvaPdf from './helpers/salva-pdf';
import logger from './helpers/logger';
import config from './config';

// global css stuff
import '../scss/main.scss';

// bootstrap studio stuff
// TODO IMPORTANT: Do we need it?
import './bootstrap/script.min';
import '../css/bootstrap/styles.min.css';

export {
  copyToClipboard,
  delay,
  setTooltip,
  hideTooltip,
  doc,
  specialElementHandlers,
  salvaPdf,
  logger,
  config
};
