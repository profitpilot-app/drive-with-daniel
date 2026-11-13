(function(){
var m=document.getElementById('modal'),f=document.getElementById('f'),mode='drive';
var day=document.getElementById('day'),time=document.getElementById('time');
var D=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function fillDays(){day.innerHTML='';var t=new Date();for(var i=0,n=0;n<14&&i<20;i++){var x=new Date(t.getFullYear(),t.getMonth(),t.getDate()+i);if(x.getDay()===0)continue;n++;var o=document.createElement('option');o.value=(i===0?'Today, ':i===1?'Tomorrow, ':'')+D[x.getDay()]+' '+M[x.getMonth()]+' '+x.getDate()+', '+x.getFullYear();o.textContent=o.value.replace(/, \d{4}$/,'');o.dataset.i=i;day.appendChild(o);}fillTimes();}
function fillTimes(){time.innerHTML='';var today=day.selectedOptions[0]&&day.selectedOptions[0].dataset.i==='0',now=new Date(),h0=today?now.getHours()+1:9;
for(var h=9;h<=19;h++)for(var mm=0;mm<60;mm+=30){if(h===19&&mm>0)continue;if(today&&(h<h0||(h===h0&&mm<now.getMinutes())))continue;var o=document.createElement('option');var hh=h%12||12;o.value=hh+':'+(mm?'30':'00')+(h<12?' AM':' PM');o.textContent=o.value;time.appendChild(o);}
if(!time.options.length){day.remove(day.selectedIndex);if(day.options.length)fillTimes();}}
day.addEventListener('change',fillTimes);
document.querySelectorAll('[data-open]').forEach(function(b){b.addEventListener('click',function(){mode=b.dataset.open;document.getElementById('mt').textContent=mode==='drive'?'Schedule a Test Drive':'Confirm Availability';
document.getElementById('dt').hidden=mode!=='drive';document.getElementById('sb').textContent=mode==='drive'?'Request test drive':'Check availability';
f.hidden=false;document.getElementById('ok').hidden=true;document.getElementById('err').hidden=true;m.hidden=false;document.body.style.overflow='hidden';});});
function close(){m.hidden=true;document.body.style.overflow='';}
m.querySelector('.x').addEventListener('click',close);m.addEventListener('click',function(ev){if(ev.target===m)close();});
fillDays();
f.addEventListener('submit',function(ev){ev.preventDefault();var fd=new FormData(f),err=document.getElementById('err');
if(fd.get('_honey'))return;
var name=(fd.get('name')||'').trim(),phone=(fd.get('phone')||'').trim(),email=(fd.get('email')||'').trim();
if(!name||phone.replace(/\D/g,'').length<10||!/^\S+@\S+\.\S+$/.test(email)){err.textContent='Please enter your name, a 10-digit phone number, and a valid email.';err.hidden=false;return;}
var V=window.VEH,kind=mode==='drive'?'Test Drive Request':'Availability Check';
var data={_subject:kind+': '+V.title+' ('+V.stock+') - '+name,_template:'table',_replyto:email,
'Request type':kind,'Vehicle':V.title,'Stock #':V.stock,'Listed price':V.price,'Mileage':V.miles,'VIN':V.vin,
'Requested day':mode==='drive'?fd.get('day'):'n/a','Requested time':mode==='drive'?fd.get('time'):'n/a',
'Name':name,'Phone':phone,'Email':email,'Preferred contact':fd.get('contact'),'Notes':fd.get('notes')||'',
'Vehicle page':location.href,'Marketplace listing':V.fb,'Submitted':new Date().toString()};
var sb=document.getElementById('sb');sb.disabled=true;sb.textContent='Sending…';err.hidden=true;
fetch(window.FORM,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data)})
.then(function(r){return r.json();}).then(function(j){if(j.success===true||j.success==='true'){f.hidden=true;document.getElementById('ok').hidden=false;}else throw new Error(j.message||'send failed');})
.catch(function(){err.innerHTML='Sorry, that didn\'t go through. Please call or text Daniel at <a href="tel:+18326202855">'+window.PHONE+'</a>.';err.hidden=false;})
.finally(function(){sb.disabled=false;sb.textContent=mode==='drive'?'Request test drive':'Check availability';});});
})();
