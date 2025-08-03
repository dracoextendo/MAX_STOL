const individualOrderDialog = document.getElementById('individualOrderDialog')
const individualOrderDialogOpener = document.querySelectorAll('.individualOpenDialogBtn')
const individualOrderDialogCloser = individualOrderDialog.querySelector('.closeDialogBtn')

async function openIndividualModalAndLockScroll() {
    document.body.classList.add('scroll-lock');
    individualOrderDialog.showModal();
}

function returnScroll() {
  document.body.classList.remove('scroll-lock')
}

function closeIIndividual() {
  individualOrderDialog.close()
  returnScroll()
}

function closeOnBackDropClickIndividual({ currentTarget, target }) {
  const dialog = currentTarget
  const isClickedOnBackDrop = target === dialog
  if (isClickedOnBackDrop) {
    closeIIndividual()
  }
}

individualOrderDialogCloser.addEventListener('click', closeIIndividual)
individualOrderDialogOpener.forEach(opener => {
  opener.addEventListener('click', openIndividualModalAndLockScroll);
});

individualOrderDialog.addEventListener('click', closeOnBackDropClickIndividual)
individualOrderDialog.addEventListener('cancel', (event) => {
  returnScroll()
});