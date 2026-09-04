document.addEventListener('DOMContentLoaded',()=>{
  const year=document.querySelector('[data-current-year]');
  if(year) year.textContent=new Date().getFullYear();

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const items=document.querySelectorAll('.reveal');

  if(reduceMotion||!('IntersectionObserver' in window)){
    items.forEach(el=>el.classList.add('visible'));
    return;
  }

  const observer=new IntersectionObserver((entries,obs)=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  },{threshold:.12,rootMargin:'0px 0px -24px 0px'});

  items.forEach(el=>observer.observe(el));
});
