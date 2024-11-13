document.addEventListener('DOMContentLoaded', () => {
const swiper = new Swiper('.swiper-container', {
    slidesPerView: 1,
    breakpoints: {
        768: {
          slidesPerView: 3, 
        },
    },
    spaceBetween: 8,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    loop: true,
    loopedSlides: 8, 
});  
const currentPage = document.querySelector('.current-page');
const totalPages = document.querySelector('.total-pages');
totalPages.textContent = swiper.slides.length;
swiper.on('slideChange', () => {
    currentPage.textContent = swiper.realIndex + 1; 
});
})