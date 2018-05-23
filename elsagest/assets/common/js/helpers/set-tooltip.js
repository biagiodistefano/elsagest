export default (el, message) => {
  $(el)
    .tooltip('hide')
    .attr('data-original-title', message)
    .tooltip('show');
};
