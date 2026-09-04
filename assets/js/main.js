document.addEventListener('DOMContentLoaded',()=>{
  const year=document.querySelector('[data-current-year]');
  if(year) year.textContent=new Date().getFullYear();

  const runtimeStyle=document.createElement('style');
  runtimeStyle.textContent=`
    [id]{scroll-margin-top:96px}
    .hero-main,.hero-side,.cap,.work,.panel,.person,.insight-card>*{min-width:0}
    .team-grid-two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:900px}
    .mobile-menu-toggle,.mobile-menu{display:none}
    .mobile-menu-toggle,.lang-link,.btn{touch-action:manipulation}

    @media(max-width:1040px){
      .team-grid-two{grid-template-columns:repeat(2,minmax(0,1fr));max-width:none}
      .hero-side{min-height:360px}
    }

    @media(max-width:900px){
      .mobile-menu-toggle{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;margin-left:auto;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.34);color:var(--ink);cursor:pointer;flex:0 0 auto}
      .mobile-menu-toggle span,.mobile-menu-toggle span:before,.mobile-menu-toggle span:after{display:block;width:15px;height:1px;background:currentColor;position:relative;transition:.18s ease}
      .mobile-menu-toggle span:before,.mobile-menu-toggle span:after{content:'';position:absolute;left:0}
      .mobile-menu-toggle span:before{top:-5px}.mobile-menu-toggle span:after{top:5px}
      .mobile-menu-toggle[aria-expanded='true'] span{background:transparent}
      .mobile-menu-toggle[aria-expanded='true'] span:before{top:0;transform:rotate(45deg)}
      .mobile-menu-toggle[aria-expanded='true'] span:after{top:0;transform:rotate(-45deg)}
      .mobile-menu{position:absolute;top:100%;left:0;right:0;background:rgba(242,239,232,.985);border-bottom:1px solid rgba(17,20,23,.1);box-shadow:0 18px 30px rgba(17,20,23,.06);max-height:calc(100vh - 66px);overflow:auto;overscroll-behavior:contain}
      .mobile-menu.is-open{display:block}
      .mobile-menu-inner{display:grid;padding-top:10px;padding-bottom:18px}
      .mobile-menu a{padding:14px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--text)}
      .mobile-menu a:last-child{border-bottom:0}
    }

    @media(max-width:760px){
      .team-grid-two{grid-template-columns:1fr}
      .side-fact{grid-template-columns:88px minmax(0,1fr)}
      .work-topline{flex-wrap:wrap}
      .work-status{margin-left:0}
    }

    @media(max-width:430px){
      [id]{scroll-margin-top:82px}
      section{padding:72px 0}
      .hero-shell{border-radius:24px}
      .hero-main{padding:40px 20px 36px}
      .hero-side{padding:25px 20px;min-height:auto}
      h1{font-size:clamp(43px,13vw,49px)}
      h2{font-size:clamp(37px,11vw,45px)}
      .hero-copy,.lead{font-size:17px}
      .side-title{font-size:27px}
      .side-fact{grid-template-columns:78px minmax(0,1fr);gap:10px}
      .cap,.panel,.person,.work{padding:22px}
      .work{min-height:340px}
      .work-topline{display:grid;justify-items:start}
      .work-status{white-space:normal}
      .work-metric{font-size:39px;margin-top:26px}
      .insight-card{padding:22px}
      .contact{padding:88px 0}
      .contact:before,.contact:after{width:280px;height:280px}
    }

    @media(max-width:360px){
      .wrap{width:min(calc(100% - 24px),var(--max))}
      .brand{gap:10px}
      .mark{width:32px}
      .mark:before,.mark:after{width:19px;height:19px}
      .brand-name{font-size:11px}
      .nav-inner{gap:10px}
      .lang-link{padding:7px 9px}
      .mobile-menu-toggle{width:40px;height:40px}
      h1{font-size:43px}
      .actions{gap:9px}
    }
  `;
  document.head.appendChild(runtimeStyle);

  const nav=document.querySelector('.nav');
  const navInner=document.querySelector('.nav-inner');
  const desktopLinks=document.querySelector('.nav-links');
  const langLink=document.querySelector('.lang-link');
  if(nav&&navInner&&desktopLinks&&langLink){
    const isTr=document.documentElement.lang==='tr';
    const openLabel=isTr?'Navigasyonu aç':'Open navigation';
    const closeLabel=isTr?'Navigasyonu kapat':'Close navigation';

    const toggle=document.createElement('button');
    toggle.className='mobile-menu-toggle';
    toggle.type='button';
    toggle.setAttribute('aria-label',openLabel);
    toggle.setAttribute('aria-expanded','false');
    toggle.setAttribute('aria-controls','mobile-navigation');
    toggle.innerHTML='<span aria-hidden="true"></span>';
    navInner.insertBefore(toggle,langLink);

    const menu=document.createElement('nav');
    menu.className='mobile-menu';
    menu.id='mobile-navigation';
    menu.setAttribute('aria-label',isTr?'Mobil navigasyon':'Mobile navigation');
    menu.hidden=true;

    const inner=document.createElement('div');
    inner.className='wrap mobile-menu-inner';
    desktopLinks.querySelectorAll('a').forEach(link=>inner.appendChild(link.cloneNode(true)));
    menu.appendChild(inner);
    nav.appendChild(menu);

    const closeMenu=(restoreFocus=false)=>{
      const wasOpen=toggle.getAttribute('aria-expanded')==='true';
      menu.classList.remove('is-open');
      menu.hidden=true;
      toggle.setAttribute('aria-expanded','false');
      toggle.setAttribute('aria-label',openLabel);
      if(restoreFocus&&wasOpen) toggle.focus();
    };

    const openMenu=()=>{
      menu.hidden=false;
      menu.classList.add('is-open');
      toggle.setAttribute('aria-expanded','true');
      toggle.setAttribute('aria-label',closeLabel);
    };

    toggle.addEventListener('click',()=>{
      const open=toggle.getAttribute('aria-expanded')==='true';
      if(open) closeMenu(); else openMenu();
    });

    inner.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>closeMenu()));
    document.addEventListener('keydown',event=>{
      if(event.key==='Escape') closeMenu(true);
    });
    document.addEventListener('click',event=>{
      if(!menu.hidden&&!nav.contains(event.target)) closeMenu();
    });
    window.addEventListener('resize',()=>{
      if(window.innerWidth>900) closeMenu();
    },{passive:true});
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
