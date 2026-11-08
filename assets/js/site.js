(function(){
  'use strict';
  const toggle=document.querySelector('.menu-toggle');
  const nav=document.querySelector('.nav-links');
  if(toggle&&nav){
    toggle.addEventListener('click',()=>{const opened=nav.classList.toggle('is-open');toggle.setAttribute('aria-expanded',String(opened));});
    nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');}));
    document.addEventListener('keydown',e=>{if(e.key==='Escape'){nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');}});
    document.addEventListener('click',e=>{if(!nav.contains(e.target)&&!toggle.contains(e.target)){nav.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');}});
  }
  const tablist=document.querySelector('[role="tablist"]');
  if(tablist){
    const tabs=[...tablist.querySelectorAll('[role="tab"]')];
    function activate(id,updateUrl){
      tabs.forEach(tab=>{const active=tab.id===id;tab.setAttribute('aria-selected',active?'true':'false');tab.tabIndex=active?0:-1;document.getElementById(tab.getAttribute('aria-controls')).hidden=!active;});
      if(updateUrl){const uri=new URL(location.href);uri.searchParams.set('service',id==='dinner-tab'?'dinner':'lunch');history.replaceState(null,'',uri.toString());}
    }
    tabs.forEach((tab,i)=>{
      tab.addEventListener('click',()=>activate(tab.id,true));
      tab.addEventListener('keydown',e=>{if(['ArrowRight','ArrowLeft','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;activate(tabs[next].id,true);tabs[next].focus();}});
    });
    const params=new URLSearchParams(location.search);activate(params.get('service')==='dinner'?'dinner-tab':'lunch-tab',false);
  }
  document.querySelectorAll('a[target="_blank"]').forEach(a=>{a.rel='noopener noreferrer';});
})();
