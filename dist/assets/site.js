
const q=document.querySelector('[data-search-input]');
if(q){q.addEventListener('input',()=>{const v=q.value.trim().toLowerCase();document.querySelectorAll('[data-search]').forEach(el=>{el.hidden=v && !el.dataset.search.includes(v);});});}
