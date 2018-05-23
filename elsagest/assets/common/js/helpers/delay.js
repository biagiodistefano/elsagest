export default () => {
  let timer;

  return (cb, ms) => {
    if (timer) {
      clearTimeout(timer);
    }

    timer = setTimeout(cb, ms);
  };
};
