document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('a.nav-item').forEach(a=>a.addEventListener('click',()=>document.body.classList.remove('sidebar-open')));
});
