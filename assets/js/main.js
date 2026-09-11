document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded',()=>{
  const isTr=document.documentElement.lang==='tr';
  const year=document.querySelector('[data-current-year]');
  if(year) year.textContent=new Date().getFullYear();

  const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const nav=document.querySelector('.nav');
  const navInner=document.querySelector('.nav-inner');
  const desktopLinks=document.querySelector('.nav-links');
  const langLink=document.querySelector('.lang-link');

  if(nav&&navInner&&desktopLinks&&langLink){
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
      inner.querySelector('a')?.focus();
    };

    toggle.addEventListener('click',()=>{
      const open=toggle.getAttribute('aria-expanded')==='true';
      if(open) closeMenu(); else openMenu();
    });

    inner.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>closeMenu()));
    document.addEventListener('keydown',event=>{
      if(event.key==='Escape') closeMenu(true);
      if(event.key==='Tab'&&!menu.hidden){
        const focusables=[toggle,...inner.querySelectorAll('a'),langLink].filter(el=>!el.hasAttribute('disabled'));
        const first=focusables[0];
        const last=focusables[focusables.length-1];
        if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
        else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
      }
    });
    document.addEventListener('click',event=>{
      if(!menu.hidden&&!nav.contains(event.target)) closeMenu();
    });
    window.addEventListener('resize',()=>{
      if(window.innerWidth>900) closeMenu();
    },{passive:true});

    const sectionLinks=[...desktopLinks.querySelectorAll('a[href^="#"]')]
      .map(link=>{
        const id=link.getAttribute('href')?.slice(1);
        const target=id?document.getElementById(id):null;
        return id&&target?{id,target}:null;
      })
      .filter(Boolean);

    const allSectionLinks=()=>[
      ...desktopLinks.querySelectorAll('a[href^="#"]'),
      ...inner.querySelectorAll('a[href^="#"]')
    ];

    let navFramePending=false;
    const updateNavigationState=()=>{
      navFramePending=false;
      nav.classList.toggle('is-compact',window.scrollY>28);

      const activationLine=window.scrollY+nav.offsetHeight+Math.min(window.innerHeight*.2,150);
      let activeId='';
      sectionLinks.forEach(({id,target})=>{
        const top=target.getBoundingClientRect().top+window.scrollY;
        if(top<=activationLine) activeId=id;
      });

      allSectionLinks().forEach(link=>{
        const active=Boolean(activeId)&&link.getAttribute('href')===`#${activeId}`;
        link.classList.toggle('is-active',active);
        if(active) link.setAttribute('aria-current','location');
        else link.removeAttribute('aria-current');
      });
    };

    const requestNavigationUpdate=()=>{
      if(navFramePending) return;
      navFramePending=true;
      window.requestAnimationFrame(updateNavigationState);
    };

    window.addEventListener('scroll',requestNavigationUpdate,{passive:true});
    window.addEventListener('resize',requestNavigationUpdate,{passive:true});
    window.addEventListener('hashchange',requestNavigationUpdate);
    requestNavigationUpdate();
  }

  const items=document.querySelectorAll('.reveal');

  if(reduceMotion||!('IntersectionObserver' in window)){
    items.forEach(el=>el.classList.add('visible'));
  }else{
    const observer=new IntersectionObserver((entries,obs)=>{
      entries.forEach(entry=>{
        if(entry.isIntersecting){
          entry.target.classList.add('visible');
          obs.unobserve(entry.target);
        }
      });
    },{threshold:.12,rootMargin:'0px 0px -24px 0px'});

    items.forEach(el=>observer.observe(el));
  }
});
