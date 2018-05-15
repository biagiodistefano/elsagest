// N.B: This library does not seem to be working... not v2 neither v1.7...
// TODO: Fix this
// import ClipboardJS from 'clipboard';

export default element => {
  const $temp = $('<input id="copia">');
  $(element)
    .parent()
    .append($temp);

  // select text
  if ($(element).is('p')) {
    $temp.val($(element).text()).select();
  } else {
    $temp.val($(element).val()).select();
  }

  // copy it
  document.execCommand('copy');

  $temp.remove();
};
