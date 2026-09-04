document.addEventListener('DOMContentLoaded',()=>{
  const year=document.querySelector('[data-current-year]');
  if(year) year.textContent=new Date().getFullYear();

  // Temporary staging guard until the final team bios are folded into EN/TR markup.
  document.querySelectorAll('.person').forEach(card=>{
    const name=card.querySelector('h3')?.textContent?.trim();
    if(name==='Mert Özel') card.remove();
  });
  document.querySelectorAll('.team-grid').forEach(grid=>{
    if(grid.children.length===2) grid.classList.add('team-grid-two');
  });
  const teamStyle=document.createElement('style');
  teamStyle.textContent='.team-grid-two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px}@media(max-width:1040px){.team-grid-two{grid-template-columns:1fr;max-width:none}}';
  document.head.appendChild(teamStyle);

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
