try {document.querySelector('video').addEventListener('contextmenu', event => {
    event.preventDefault(); /* Контекстное меню не появится. */
});}
catch {}

let emailLinks = document.querySelectorAll('.email_link')
let copyAlert = document.querySelector('.copy_alert')

let hideAlert = function (obj) {
    obj.style.opacity = '0';
}

let copyLink = function () {
    navigator.clipboard.writeText("info_loveforlive@mail.ru");
    copyAlert.style.opacity = '0.8';
    setTimeout(hideAlert, 3000, copyAlert)
};

for (let index = 0; index<emailLinks.length; index++) {
    emailLinks[index].addEventListener('click', copyLink);
};
