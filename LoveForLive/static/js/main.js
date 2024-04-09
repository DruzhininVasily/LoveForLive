document.querySelector('video').addEventListener('contextmenu', event => {
    event.preventDefault(); /* Контекстное меню не появится. */
});

const copyLink = (e) => {
    e.preventDefault();
    let aux = document.createElement('input');
    let url = e.target.getAttribute('href');
    aux.setAttribute('value', url);
    document.body.appendChild(aux);
    aux.select();
    document.execCommand('copy');
    document.body.removeChild(aux);
  };

let links = document.querySelectorAll('.email_link');
for (link in links) {
    link.addEventListener('click', copyLink);
}
