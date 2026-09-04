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

  const runtimeStyle=document.createElement('style');
  runtimeStyle.textContent=`
    .team-grid-two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px}
    .mobile-menu-toggle,.mobile-menu{display:none}
    @media(max-width:1040px){.team-grid-two{grid-template-columns:1fr;max-width:none}}
    @media(max-width:900px){
      .mobile-menu-toggle{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;margin-left:auto;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.34);color:var(--ink);cursor:pointer}
      .mobile-menu-toggle span,.mobile-menu-toggle span:before,.mobile-menu-toggle span:after{display:block;width:15px;height:1px;background:currentColor;position:relative;transition:.18s ease}
      .mobile-menu-toggle span:before,.mobile-menu-toggle span:after{content:'';position:absolute;left:0}
      .mobile-menu-toggle span:before{top:-5px}.mobile-menu-toggle span:after{top:5px}
      .mobile-menu-toggle[aria-expanded='true'] span{background:transparent}
      .mobile-menu-toggle[aria-expanded='true'] span:before{top:0;transform:rotate(45deg)}
      .mobile-menu-toggle[aria-expanded='true'] span:after{top:0;transform:rotate(-45deg)}
      .mobile-menu{position:absolute;top:100%;left:0;right:0;background:rgba(242,239,232,.98);border-bottom:1px solid rgba(17,20,23,.1);box-shadow:0 18px 30px rgba(17,20,23,.06)}
      .mobile-menu.is-open{display:block}
      .mobile-menu-inner{display:grid;padding-top:10px;padding-bottom:18px}
      .mobile-menu a{padding:13px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--text)}
    }
  `;
  document.head.appendChild(runtimeStyle);

  const nav=document.querySelector('.nav');
  const navInner=document.querySelector('.nav-inner');
  const desktopLinks=document.querySelector('.nav-links');
  const langLink=document.querySelector('.lang-link');
  if(nav&&navInner&&desktopLinks&&langLink){
    const toggle=document.createElement('button');
    toggle.className='mobile-menu-toggle';
    toggle.type='button';
    toggle.setAttribute('aria-label','Open navigation');
    toggle.setAttribute('aria-expanded','false');
    toggle.setAttribute('aria-controls','mobile-navigation');
    toggle.innerHTML='<span aria-hidden="true"></span>';
    navInner.insertBefore(toggle,langLink);

    const menu=document.createElement('div');
    menu.className='mobile-menu';
    menu.id='mobile-navigation';
    const inner=document.createElement('div');
    inner.className='wrap mobile-menu-inner';
    desktopLinks.querySelectorAll('a').forEach(link=>inner.appendChild(link.cloneNode(true)));
    menu.appendChild(inner);
    nav.appendChild(menu);

    const closeMenu=()=>{
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded','false');
    };
    toggle.addEventListener('click',()=>{
      const open=toggle.getAttribute('aria-expanded')==='true';
      toggle.setAttribute('aria-expanded',String(!open));
      menu.classList.toggle('is-open',!open);
    });
    inner.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
    document.addEventListener('keydown',event=>{if(event.key==='Escape') closeMenu();});
    window.addEventListener('resize',()=>{if(window.innerWidth>900) closeMenu();},{passive:true});
  }

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
