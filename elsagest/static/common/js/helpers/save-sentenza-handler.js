import salvaPdf from './salva-pdf';

$(document).on('click', '.salva-sentenza', evt => {
  const element = $(evt.currentTarget);

  const sentenza = element
    .parent()
    .parent()
    .find('.sentenza');

  salvaPdf(sentenza);
});
