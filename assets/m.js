(function(){function oa(){var d=new Date(Date.now()+7*3600e3),m=d.getUTCHours()*60+d.getUTCMinutes(),W=[[975,1010],[1035,1070],[1095,1125]],on=W.some(function(w){return m>=w[0]&&m<=w[1]});document.querySelectorAll('.tab a[href$="truc-tiep/"]').forEach(function(a){a.classList.toggle('onair',on)})}oa();setInterval(oa,30000)})();
(function(){var D=document.querySelectorAll('.mbar details');function closeAll(x){D.forEach(function(d){if(d!==x)d.open=false})}
D.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)closeAll(d)})});
document.querySelectorAll('.subnav').forEach(function(n){var f=function(){n.classList.toggle('end',n.scrollLeft+n.clientWidth>=n.scrollWidth-4)};n.addEventListener('scroll',f,{passive:true});f();var c=n.querySelector('[aria-current]');if(c&&c.offsetLeft+c.offsetWidth>n.clientWidth)n.scrollLeft=c.offsetLeft-12});var MR=document.querySelector('.mrow');if(MR){var me=function(){MR.parentNode.classList.toggle('end',MR.scrollLeft+MR.clientWidth>=MR.scrollWidth-4)};MR.addEventListener('scroll',me,{passive:true});addEventListener('resize',me);me();
var cu=MR.querySelector('.is-cur');if(cu&&cu.offsetLeft+cu.offsetWidth>MR.clientWidth)MR.scrollLeft=cu.offsetLeft-12;}
document.addEventListener('click',function(e){if(!e.target.closest('.mbar'))closeAll()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll()});
if(window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches)D.forEach(function(d){var t;
d.addEventListener('mouseenter',function(){clearTimeout(t);closeAll(d);d.open=true});
d.addEventListener('mouseleave',function(){t=setTimeout(function(){d.open=false},200)});
d.querySelector('summary').addEventListener('click',function(e){var h=d.getAttribute('data-href');if(h){e.preventDefault();location.href=h}});
d.addEventListener('focusin',function(){closeAll(d);d.open=true});d.addEventListener('focusout',function(e){if(!d.contains(e.relatedTarget))d.open=false})});
if(!document.body.classList.contains('static'))return;
var TH=[['auto','Tự động'],['light','Sáng'],['dark','Tối']];function get(){try{return JSON.parse(localStorage.getItem('xs-theme'))||'auto'}catch(e){return 'auto'}}
function lab(){var t=get(),n=TH.find(function(x){return x[0]===t})||TH[0];document.querySelectorAll('.themebtn').forEach(function(b){b.textContent='Giao diện: '+n[1]})}
function cyc(){var t=get(),i=TH.findIndex(function(x){return x[0]===t});t=TH[(i+1)%3][0];try{localStorage.setItem('xs-theme',JSON.stringify(t))}catch(e){}if(t==='auto')delete document.documentElement.dataset.theme;else document.documentElement.dataset.theme=t;lab()}
document.querySelectorAll('.mtheme,.themebtn').forEach(function(b){b.addEventListener('click',cyc)});lab()})();