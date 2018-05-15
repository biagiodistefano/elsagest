import setTooltip from './set-tooltip';
import hideTooltip from './hide-tooltip';

$(document).on('click', '.copia', evt => {
  const element = $(evt.currentTarget);

  element.tooltip({
    trigger: 'click',
    placement: 'top'
  });

  setTooltip(element, 'Copiato!');
  hideTooltip(element);
});
