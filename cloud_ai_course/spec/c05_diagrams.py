from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'ledger': bars([('weights (bf16)', 2, 'teal', '2'), ('gradients (bf16)', 2, 'orange', '2'), ('fp32 master copy', 4, 'blue', '4'), ('Adam memory m', 4, 'blue', '4'), ('Adam memory v', 4, 'blue', '4')],
               [0, 0, 1, 1, 1], 4, head=('part', 'bytes per parameter: 2 + 2 + 12 = 16'), x0=290, wmax=420, y0=44, dy=50, bh=36, note=('the weights are the small part', 2, 'red')),
'ledger_measured': bars([('weights', 4, 'teal', '4.0 bytes'), ('gradients', 4, 'orange', '4.0 bytes'), ('Adam m + v', 8, 'blue', '8.0 bytes')], [0, 0, 1], 8,
                        head=('part', 'MEASURED on 33,574,912 parameters (float32)'), x0=230, wmax=480, y0=50, dy=64, bh=42, note=('total: 16.0 bytes per parameter', 1, 'green')),
'bigstate': bars([('7B', 112, 'teal', '112 GB'), ('70B', 1120, 'orange', '1,120 GB'), ('405B', 6480, 'red', '6,480 GB')], [0, 0, 1], 6480,
                 head=('model', 'training state at 16 bytes per parameter'), x0=130, wmax=640, y0=50, dy=64, bh=42, line=(80, 'one H100: 80 GB', 1, 'blue')),
'zero': bars([('DDP, nothing shared', 1120, 'red', '1,120 GB'), ('ZeRO-1', 293, 'orange', '293 GB'), ('ZeRO-2', 155, 'orange', '155 GB'), ('ZeRO-3 / FSDP', 17.5, 'green', '17.5 GB')], [0, 1, 1, 2], 1120,
             head=('method', 'per-GPU GB for a 70B model on 64 GPUs (arithmetic)'), x0=260, wmax=470, y0=50, dy=58, bh=40, line=(80, 'one H100: 80 GB', 2, 'blue')),
'rc_result': boxes([('activation memory', '793 MB → 426 MB', 'green'), ('time per step', '5.6 s → 6.9 s', 'orange'), ('in plain words', 'half the memory, a fifth more time', 'teal')], [0, 1, 2], y=50, h=190,
                   note=('measured on a CPU, 12 blocks, 2,048 tokens', 2, 'blue')),
'gpuhours': boxes([('6 × N × D', '6 × 7B × 2T', 'blue'), ('8.4e22', 'FLOPs needed', 'teal'), ('58,982', 'GPU-hours at 40% MFU', 'orange'), ('2.4 days', 'on 1,024 GPUs', 'green')], [0, 0, 1, 1], y=50, h=180, arrows=True,
                  note=('at an assumed $2 per GPU-hour: about $118,000', 2, 'red')),
'split4': boxes([('data', 'same model, different data', 'blue'), ('tensor', 'split inside a layer', 'orange'), ('pipeline', 'split layers into stages', 'teal'), ('expert', 'split the experts', 'green')], [0, 1, 1, 2], y=50, h=190, size=27,
                note=('each one cuts a different thing', 2, 'red')),
'bubble': r"""
 const p=4,m=4,T=2*(m+p-1),cw=64,ch=44,x0=150,y0=36;
 for(let s=0;s<p;s++){ d.at(S+'.0',s*0.1).text(x0-14,y0+s*(ch+10)+30,'stage '+s,{size:24,color:C.ink,anchor:'end'});
   for(let t=0;t<T;t++){ let k='.'; for(let mb=0;mb<m;mb++){ if(t===s+mb)k='F'; if(t===(m+p-1)+(p-1-s)+mb)k='B'; }
     const col=k==='F'?C.blue:k==='B'?C.orange:C.gray, fill=k==='F'?C.blueSoft:k==='B'?C.orangeSoft:'#f3f4f6';
     d.at(S+'.'+(k==='.'?1:0),0.2+t*0.05).box(x0+t*cw*0.88,y0+s*(ch+10),cw*0.82,ch,k==='.'?null:k,{stroke:col,fill:fill,fillStyle:'solid',size:24,color:col,sw:1.5}); } }
 d.at(S+'.1',0.5).text(500,268,'gray = a GPU sitting idle: 6 of 14 slots, 42.9%',{size:28,color:C.red,font:'Caveat'});
""",
'bubble_tbl': bars([('p=4, m=4', 42.9, 'red', '42.9% idle'), ('p=8, m=8', 46.7, 'red', '46.7%'), ('p=8, m=32', 17.9, 'orange', '17.9%'), ('p=8, m=128', 5.2, 'green', '5.2%'), ('p=8, m=32, v=4', 4.5, 'green', 'about 4.5%')],
                   [0, 0, 1, 1, 1], 50, head=('stages p, micro-batches m', 'share of GPU time idle (simulation, formula-checked)'), x0=330, wmax=400, y0=44, dy=52, bh=36,
                   note=('more micro-batches shrink the bubble', 1, 'green')),
'mapping': boxes([('tensor (TP)', 'inside a node, NVLink', 'red'), ('pipeline (PP)', 'across nodes', 'orange'), ('data / FSDP', 'outermost, overlaps compute', 'blue')], [0, 0, 1], y=50, h=190, arrows=True,
                 note=('the chattiest group sits closest', 1, 'green')),
'netcost': bars([('7B, scale-out 50 GB/s', 0.56, 'red', '0.56 s'), ('7B, NVLink 450 GB/s', 0.06, 'green', '0.06 s'), ('70B, scale-out 50 GB/s', 5.6, 'red', '5.6 s')], [0, 0, 1], 5.6,
                head=('model, link', 'seconds per step to all-reduce gradients if not overlapped'), x0=300, wmax=480, y0=50, dy=64, bh=42),
'lora': bars([('full training', 268.6, 'red', '268.6 MB'), ('LoRA rank 16', 5.2, 'orange', '5.2 MB'), ('LoRA rank 8', 2.6, 'green', '2.6 MB')], [0, 0, 1], 268.6,
             head=('what you train', 'Adam optimiser memory, measured on the same small model'), x0=250, wmax=470, y0=50, dy=64, bh=42, note=('rank 8 trains 0.97% of the parameters', 1, 'green')),
'mini_thumb': mini2('weights only (70B)', '140 GB', 'grey', 'training state', '1,120 GB', 'red', '16 bytes per parameter'),
'mini_ledger': mini2('inference weights', '140 GB', 'grey', 'training state', '1,120 GB', 'red', '70B model, bf16 recipe'),
'mini_lora': mini2('full training', '268.6 MB', 'red', 'LoRA rank 8', '2.6 MB', 'green', 'optimiser memory, measured'),
'mini_bubble': mini2('4 stages, 4 batches', '43% idle', 'red', '8 stages, 128 batches', '5% idle', 'green', 'pipeline bubble'),
}
