
// navbar fixed
// window.onscroll = function() {
//   const header = document.querySelector('header');
//   const fixedNav = header.offsetTop;
//   const toTop = document.querySelector('#to-top');
//   
//   if(window.pageYOffset > fixedNav) {
//     header.classList.add('navbar-fixed');
//     toTop.classList.remove('hidden');
//     toTop.classList.add('flex');
//   } else {
//     header.classList.remove('navbar-fixed');
//     toTop.classList.remove('flex');
//     toTop.classList.add('hidden');
//   }
// };


// Temukan tombol profil
const userMenuButton = document.getElementById('user-menu-button');
// Temukan menu dropdown profil
const userMenu = document.querySelector('[aria-labelledby="user-menu-button"]');
// Sembunyikan menu dropdown profil saat halaman dimuat
userMenu.style.display = 'none';

// Temukan tombol mobile menu
const mobileMenuButton = document.querySelector('[aria-controls="mobile-menu"]');
// Temukan menu mobile menu
const mobileMenu = document.getElementById('mobile-menu');
// Sembunyikan menu mobile menu saat halaman dimuat
mobileMenu.style.display = 'none';

// Tambahkan event listener untuk mengelola klik tombol profil
userMenuButton.addEventListener('click', () => {
  const isUserMenuOpen = userMenu.style.display === 'block';

  // Jika menu profil terbuka, tutup; jika tidak, buka
  if (isUserMenuOpen) {
    userMenu.style.display = 'none';
  } else {
    userMenu.style.display = 'block';
    mobileMenu.style.display = 'none'; // Sembunyikan mobile menu jika terbuka
  }
});

// Tambahkan event listener untuk mengelola klik tombol mobile menu
mobileMenuButton.addEventListener('click', () => {
  const isMobileMenuOpen = mobileMenu.style.display === 'block';

  // Jika mobile menu terbuka, tutup; jika tidak, buka
  if (isMobileMenuOpen) {
    mobileMenu.style.display = 'none';
  } else {
    mobileMenu.style.display = 'block';
    userMenu.style.display = 'none'; // Sembunyikan dropdown profil jika terbuka
  }
});
const list = document.querySelectorAll(".list");

function activeLink() {
  list.forEach((item) => item.classList.remove("active"));
  this.classList.add("active");
}
list.forEach((item) => item.addEventListener("click", activeLink));


// dark mode
const darkToggle = document.querySelector('#dark-toggle');
const html = document.querySelector('html');

// dark mode
darkToggle.addEventListener("click", function() {
  if(darkToggle.checked) {
    html.setAttribute('data-theme', 'dark');
    localStorage.theme = 'dark';
  } else {
    html.setAttribute('data-theme', 'light');
    localStorage.theme = 'light';
  }
});

// pindahkan toggle sesuai mode
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
 
  darkToggle.checked = true;
} else {
  darkToggle.checked = false;
}