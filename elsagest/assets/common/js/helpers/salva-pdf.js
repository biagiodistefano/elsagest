import doc from './doc-jspdf';
import specialElementHandlers from './special-element-handlers';

export default target => {
  doc.fromHTML($(target).html(), 15, 15, {
    width: 170,
    elementHandlers: specialElementHandlers
  });

  doc.save(`${$(target).attr('name')}.pdf`);
};
