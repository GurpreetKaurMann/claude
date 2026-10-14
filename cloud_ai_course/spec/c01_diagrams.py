DIAGRAMS = {
'workers': r'''
 d.at(S+'.0',0).text(250,30,'CPU: a few strong workers',{size:28,color:C.blue});
 for(let i=0;i<4;i++){ d.at(S+'.0',0.3+i*0.2).box(60+i*105,60,90,90,null,{stroke:C.blue,fill:C.blueSoft,fillStyle:'solid'}); }
 d.at(S+'.0',1.2).text(250,205,'great at many different jobs',{size:24,color:'#4b5563',font:'Caveat'});
 d.at(S+'.1',0).text(750,30,'GPU: thousands of simple workers',{size:28,color:C.teal});
 for(let r=0;r<5;r++){ for(let c=0;c<10;c++){ d.at(S+'.1',0.2+(r*10+c)*0.02).box(550+c*40,55+r*34,30,26,null,{stroke:C.teal,fill:C.tealSoft,fillStyle:'solid',sw:1}); } }
 d.at(S+'.1',1.4).text(750,250,'all doing the same sum at once',{size:24,color:'#4b5563',font:'Caveat'});
 d.at(S+'.2',0).text(500,285,'AI is mostly one job: multiply big tables of numbers',{size:26,color:C.orange,font:'Caveat'});
''',
'four': r'''
 const it=[['1','memory size','what fits',C.teal],['2','memory speed','how fast chat runs',C.orange],['3','compute','how fast it thinks',C.blue],['4','connection','how GPUs talk',C.green]];
 it.forEach(([n,a,b,c],i)=>{ const x=14+i*247, sg=S+'.'+(i<2?0:1), dl=(i%2)*0.9;
   d.at(sg,dl).box(x,40,230,200,null,{stroke:c,fill:'#fff',fillStyle:'solid'});
   d.at(sg,dl+0.15).text(x+115,95,n,{size:54,color:c,font:'Caveat'});
   d.at(sg,dl+0.3).text(x+115,150,a,{size:28,color:c});
   d.at(sg,dl+0.45).text(x+115,195,b,{size:22,color:'#4b5563',bold:false}); });
''',
'fitbars': r'''
 const g=[['H100',80],['H200',141],['B200',192],['B300',288]]; const X=v=>170+v*2.5;
 g.forEach(([n,v],i)=>{ const y=44+i*56;
   d.at(S+'.0',i*0.35).text(30,y+34,n,{size:28,color:C.ink,anchor:'start'});
   d.at(S+'.0',i*0.35+0.1).box(170,y+6,v*2.5,40,null,{stroke:C.gray,fill:'#f3f4f6',fillStyle:'solid'});
   d.at(S+'.0',i*0.35+0.2).text(170+v*2.5+10,y+34,v+' GB',{size:24,color:'#4b5563',anchor:'start'}); });
 d.at(S+'.1',0).line(X(70),36,X(70),270,{sw:4,stroke:C.teal});
 d.at(S+'.1',0.2).text(X(70)-8,26,'70B, FP8: 70 GB',{size:24,color:C.teal,anchor:'end',font:'Caveat'});
 d.at(S+'.2',0).line(X(140),36,X(140),270,{sw:4,stroke:C.red,dash:true});
 d.at(S+'.2',0.2).text(X(140)+8,26,'70B, BF16: 140 GB',{size:24,color:C.red,anchor:'start',font:'Caveat'});
''',
'kv_stack': r'''
 const X=v=>40+v*3.4;
 d.at(S+'.0',0).box(X(0),70,70*3.4,70,'weights 70 GB',{stroke:C.teal,fill:C.tealSoft,fillStyle:'solid',size:24});
 d.at(S+'.1',0).box(X(70),70,86*3.4,70,'32 chats: 86 GB',{stroke:C.orange,fill:C.orangeSoft,fillStyle:'solid',size:24});
 d.at(S+'.2',0).box(X(156),70,31*3.4,70,'+20%',{stroke:C.gray,fill:'#f3f4f6',fillStyle:'solid',size:24});
 d.at(S+'.2',0.5).text(X(93),40,'187 GB needed',{size:30,color:C.red,font:'Caveat'});
 [[80,'H100'],[141,'H200'],[192,'B200']].forEach(([v,n],i)=>{
   d.at(S+'.3',0.3+i*0.5).line(X(v),150,X(v),235,{sw:3,stroke:(v<187?C.red:C.green)});
   d.at(S+'.3',0.4+i*0.5).text(X(v),262,n+' '+(v<187?'no':'yes'),{size:24,color:(v<187?C.red:C.green),font:'Caveat'}); });
''',
'kvper': r'''
 const r=[['2 for K and V',C.blue],['x 80 layers',C.teal],['x 8 KV heads',C.orange],['x 128 numbers',C.green],['x 2 bytes',C.gray]];
 r.forEach(([t,c],i)=>{ d.at(S+'.'+(i<3?0:1),(i<3?i:i-3)*0.8).box(20+i*196,60,182,100,t,{stroke:c,fill:'#fff',fillStyle:'solid',size:24,color:c}); });
 d.at(S+'.2',0).arrow(500,172,500,215,{sw:3,stroke:C.red});
 d.at(S+'.2',0.3).text(500,262,'= 327,680 bytes for every token of every chat',{size:30,color:C.red,font:'Caveat'});
''',
'sizes': r'''
 const rows=[['4 MB',0.15],['17 MB',0.62],['67 MB',2.43],['268 MB',20.35]]; const X=v=>230+v*30;
 d.at(S+'.0',0).text(120,22,'matrix size',{size:20,bold:false,color:'#6b7280'});
 d.at(S+'.0',0).text(560,22,'time for one token (milliseconds, measured)',{size:20,bold:false,color:'#6b7280'});
 rows.forEach(([n,v],i)=>{ const y=40+i*62, sg=S+'.'+(i<3?0:1), dl=(i<3?i:0)*0.6;
   d.at(sg,dl).text(120,y+34,n,{size:28,color:C.ink});
   d.at(sg,dl+0.15).box(230,y+6,Math.max(v*30,6),40,null,{stroke:(i==3?C.red:C.teal),fill:(i==3?C.redSoft:C.tealSoft),fillStyle:'solid'});
   d.at(sg,dl+0.3).text(X(v)+14,y+34,v+' ms',{size:26,color:(i==3?C.red:C.teal),anchor:'start'}); });
 d.at(S+'.2',0).text(700,150,'4x the bytes',{size:30,color:C.red,font:'Caveat'});
 d.at(S+'.2',0.5).text(700,190,'8.4x the time',{size:40,color:C.red,font:'Caveat'});
''',
'bwcalc': r'''
 const r=[['H100','3.4 TB/s',20.6],['H200','4.8 TB/s',14.6],['B200','8.0 TB/s',8.8]];
 d.at(S+'.0',0).text(500,26,'70 GB of weights, read once per token',{size:26,color:'#6b7280',bold:false});
 r.forEach(([n,b,v],i)=>{ const y=50+i*70;
   d.at(S+'.'+(i<1?0:1),i*0.6).text(30,y+38,n,{size:30,color:C.ink,anchor:'start'});
   d.at(S+'.'+(i<1?0:1),i*0.6+0.1).text(150,y+38,b,{size:22,color:'#6b7280',anchor:'start',bold:false});
   d.at(S+'.'+(i<1?0:1),i*0.6+0.2).box(330,y+6,v*21,46,null,{stroke:C.orange,fill:C.orangeSoft,fillStyle:'solid'});
   d.at(S+'.'+(i<1?0:1),i*0.6+0.3).text(340+v*21+12,y+38,'at least '+v+' ms',{size:24,color:'#92400e',anchor:'start'}); });
 d.at(S+'.2',0).text(500,285,'a floor from vendor specs, not a benchmark',{size:24,color:C.red,font:'Caveat'});
''',
'batch': r'''
 const r=[['1',387],['8',1165],['64',3393],['256',4180]]; const X=v=>200+v*0.15;
 d.at(S+'.0',0).text(100,22,'tokens at once',{size:20,bold:false,color:'#6b7280'});
 d.at(S+'.0',0).text(640,22,'tokens per second (measured, same matrix)',{size:20,bold:false,color:'#6b7280'});
 r.forEach(([n,v],i)=>{ const y=40+i*58, sg=S+'.'+(i<2?0:1), dl=(i%2)*0.7;
   d.at(sg,dl).text(100,y+34,n,{size:30,color:C.ink});
   d.at(sg,dl+0.15).box(200,y+6,v*0.15,40,null,{stroke:(i==3?C.teal:C.gray),fill:(i==3?C.tealSoft:'#f3f4f6'),fillStyle:'solid'});
   d.at(sg,dl+0.3).text(X(v)+14,y+34,String(v),{size:26,color:(i==3?C.teal:'#4b5563'),anchor:'start'}); });
 d.at(S+'.2',0).text(500,292,'about 10x the tokens per second, from reading the weights once',{size:28,color:C.teal,font:'Caveat'});
''',
'islands': r'''
 d.at(S+'.0',0).box(30,50,400,180,null,{stroke:C.teal,fill:C.tealSoft});
 d.at(S+'.0',0.2).text(230,32,'one NVLink island (8 GPUs)',{size:24,color:C.teal});
 for(let i=0;i<4;i++){ d.at(S+'.0',0.4+i*0.15).box(60+i*90,90,70,45,'GPU',{stroke:C.teal,fill:'#fff',fillStyle:'solid',size:20}); d.at(S+'.0',0.7+i*0.15).box(60+i*90,160,70,45,'GPU',{stroke:C.teal,fill:'#fff',fillStyle:'solid',size:20}); }
 d.at(S+'.1',0).box(570,50,400,180,null,{stroke:C.blue,fill:C.blueSoft});
 d.at(S+'.1',0.2).text(770,32,'another island',{size:24,color:C.blue});
 for(let i=0;i<4;i++){ d.at(S+'.1',0.4+i*0.1).box(600+i*90,90,70,45,'GPU',{stroke:C.blue,fill:'#fff',fillStyle:'solid',size:20}); d.at(S+'.1',0.6+i*0.1).box(600+i*90,160,70,45,'GPU',{stroke:C.blue,fill:'#fff',fillStyle:'solid',size:20}); }
 d.at(S+'.2',0).arrow(440,140,560,140,{sw:4,stroke:C.red,dash:true});
 d.at(S+'.2',0.3).text(500,115,'network',{size:26,color:C.red,font:'Caveat'});
 d.at(S+'.2',0.8).text(500,275,'inside the island: about 450. between islands: about 50 (GB/s per GPU, H100)',{size:24,color:C.red,font:'Caveat'});
''',
'decide': r'''
 const st=[['1 fit','weights + chats',C.teal],['2 speed','memory bandwidth',C.orange],['3 compute','prefill, training',C.blue],['4 connect','more than 8 GPUs?',C.green]];
 st.forEach(([a,b,c],i)=>{ const x=14+i*247, sg=S+'.'+(i<2?0:1), dl=(i%2)*0.9;
   d.at(sg,dl).box(x,70,215,150,null,{stroke:c,fill:'#fff',fillStyle:'solid'});
   d.at(sg,dl+0.15).text(x+108,125,a,{size:36,color:c,font:'Caveat'});
   d.at(sg,dl+0.3).text(x+108,175,b,{size:22,color:'#4b5563',bold:false});
   if(i<3) d.at(sg,dl+0.5).arrow(x+218,145,x+245,145,{sw:3}); });
''',
'mini_thumb': r'''
 d.text(40,70,'70B weights',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,70,'70 GB',{size:50,color:'#0f766e',font:'P',anchor:'end'});
 d.text(40,150,'32 chats',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,150,'86 GB',{size:50,color:'#dc2626',font:'P',anchor:'end'});
 d.text(380,230,'one H100 = 80 GB',{size:34,color:'#be123c',font:'P'});
''',
'mini_fit': r'''
 d.box(40,40,300,70,null,{stroke:'#0f766e',fill:'#ccfbf1',fillStyle:'solid'}); d.text(190,88,'weights 70',{size:34,color:'#0f766e',font:'P'});
 d.box(340,40,369,70,null,{stroke:'#dc2626',fill:'#fee2e2',fillStyle:'solid'}); d.text(525,88,'32 chats 86',{size:34,color:'#dc2626',font:'P'});
 d.line(383,25,383,140,{sw:5,stroke:'#1e2440'}); d.text(383,168,'H100 = 80 GB',{size:32,color:'#1e2440',font:'P'});
 d.text(380,240,'187 GB needed',{size:44,color:'#dc2626',font:'P'});
''',
'mini_mem': r'''
 d.text(40,75,'67 MB matrix',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,75,'2.4 ms',{size:52,color:'#0f766e',font:'P',anchor:'end'});
 d.text(40,160,'268 MB matrix',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,160,'20 ms',{size:52,color:'#dc2626',font:'P',anchor:'end'});
 d.text(380,238,'4x the bytes, 8x the time',{size:34,color:'#be123c',font:'P'});
''',
'mini_batch': r'''
 d.text(40,75,'1 at a time',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,75,'387 /s',{size:52,color:'#dc2626',font:'P',anchor:'end'});
 d.text(40,160,'256 at once',{size:36,color:'#6b7280',font:'P',anchor:'start'}); d.text(720,160,'4,180 /s',{size:52,color:'#0f766e',font:'P',anchor:'end'});
 d.text(380,238,'tokens per second, measured',{size:34,color:'#be123c',font:'P'});
''',
}
