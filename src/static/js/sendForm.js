///////////////////////////////////////ВСПЛЫВАШКА НА ОТПРАВКУ ФОРМЫ//////////////////////////////////////////////

for (let i = 0; i < open_modal.length; i++) {
  open_modal[i].onclick = function() { 
    modal.classList.add('modal_vis', 'animate__animated', 'animate__fadeInUp'); 
    modal.classList.remove('animate__bounceOutDown'); 
    setTimeout(() => {
      modal.classList.add('animate__animated', 'animate__bounceOutDown');
      modal.classList.remove('animate__fadeInUp');
      setTimeout(() => {
        modal.classList.remove('modal_vis');
      }, 1000); 
    }, 3000);
  };
}
close_modal.onclick = function() { 
  modal.classList.add('animate__animated', 'animate__bounceOutDown'); 
  modal.classList.remove('animate__fadeInUp');
  setTimeout(() => {
    modal.classList.remove('modal_vis');
  }, 1000);
};
///////////////////////////////////////////////////////////////////////////////////////////////////////