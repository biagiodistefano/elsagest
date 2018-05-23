export default el => {
  setTimeout(() => {
    $(el).tooltip('hide');
  }, 1000);
};
