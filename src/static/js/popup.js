const dialog = document.getElementById('orderDialog')
const dialogOpener = document.querySelectorAll('.openDialogBtn')
const dialogCloser = dialog.querySelector('.closeDialogBtn')

function openModalAndLockScroll() {
  dialog.showModal()
  document.body.classList.add('scroll-lock')
}

function returnScroll() {
  document.body.classList.remove('scroll-lock')
}

function close() {
  dialog.close()
  returnScroll()
}

function closeOnBackDropClick({ currentTarget, target }) {
  const dialog = currentTarget
  const isClickedOnBackDrop = target === dialog
  if (isClickedOnBackDrop) {
    close()
  }
}

dialogCloser.addEventListener('click', close)
dialogOpener.forEach(opener => {
  opener.addEventListener('click', openModalAndLockScroll);
});

dialog.addEventListener('click', closeOnBackDropClick)
dialog.addEventListener('cancel', (event) => {
  returnScroll()
});