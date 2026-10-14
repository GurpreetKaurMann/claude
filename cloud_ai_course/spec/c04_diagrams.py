from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'tiers': boxes([('Regional', 'the truth, durable', 'blue'), ('One zone', 'speed, re-creatable', 'orange'), ('Archive', 'rarely read, cheapest', 'gray')], [0, 1, 2], y=50, h=190,
               note=('region = truth, zone = speed', 2, 'red')),
'files': bars([('20,000 files of 4 KB', 1.337, 'red', '1.34 s'), ('80 files of 1 MB', 0.079, 'orange', '0.08 s'), ('one 80 MB shard', 0.053, 'green', '0.05 s')], [0, 0, 1], 1.337,
              head=('layout', 'seconds to read 80 MB from local disk (measured)'), x0=290, wmax=520, y0=50, dy=66, bh=44),
'objmodel': bars([('20,000 files of 4 KB', 400.8, 'red', '401 s'), ('80 files of 1 MB', 2.4, 'orange', '2.4 s'), ('one 80 MB shard', 0.8, 'green', '0.8 s')], [0, 0, 1], 400.8,
                 head=('layout', 'object store MODEL: 20 ms per request + 100 MB/s (assumed)'), x0=290, wmax=520, y0=50, dy=66, bh=44),
'ckpt': bars([('70B at 10 GB/s', 98, 'red', '98 s'), ('70B at 100 GB/s', 10, 'green', '10 s'), ('405B at 10 GB/s', 567, 'red', '567 s'), ('405B at 100 GB/s', 57, 'orange', '57 s')], [0, 0, 1, 1], 567,
             head=('model, write speed', 'seconds the GPUs wait per checkpoint (assumed speeds)'), x0=260, wmax=520, y0=44, dy=56, bh=40),
'lake': boxes([('Parquet files', 'in object storage', 'blue'), ('table format', 'Delta / Iceberg', 'teal'), ('catalog', 'names + permissions', 'orange'), ('any engine', 'comes and goes', 'gray')], [0, 0, 1, 1], y=50, h=180, arrows=True,
              note=('engines come and go, the tables stay', 1, 'green')),
'versions': boxes([('file level', 'DVC, Hugging Face', 'blue'), ('lake level', 'lakeFS branches', 'teal'), ('table level', 'snapshots', 'orange')], [0, 0, 1], y=50, h=190,
                  note=('pin every training run to a version', 1, 'green')),
'formats': bars([('float32', 153.6, 'gray', '153.6 MB · recall 1.000'), ('float16', 76.8, 'green', '76.8 MB · recall 1.000'), ('int8', 38.4, 'teal', '38.4 MB · recall 0.985'),
                 ('binary', 4.8, 'orange', '4.8 MB · recall 0.212, 0.741 rescored')], [0, 1, 2, 2], 153.6,
                head=('format', '50,000 vectors x 768 numbers (synthetic): size and recall@10'), x0=190, wmax=360, y0=50, dy=58, bh=40),
'hnsw': r"""
 d.at(S+'.0',0).text(960,62,'top',{size:22,color:'#6b7280',anchor:'end',bold:false}); d.at(S+'.0',0.2).text(960,152,'middle',{size:22,color:'#6b7280',anchor:'end',bold:false}); d.at(S+'.0',0.4).text(960,232,'bottom: every vector',{size:22,color:'#6b7280',anchor:'end',bold:false});
 [[60,[320,620]],[140,[150,330,470,610,780]],[220,[60,150,240,330,420,520,610,700,790,880]]].forEach(([y,xs],r)=>{ xs.forEach((x,i)=>{ d.at(S+'.0',0.3+r*0.3+i*0.04).circle(x,y,26,{stroke:C.gray,fill:'#fff'}); }); });
 d.at(S+'.1',0).circle(320,60,30,{stroke:C.red,fill:C.redSoft});
 d.at(S+'.1',0.3).arrow(335,76,455,128,{sw:3,stroke:C.red}); d.at(S+'.1',0.5).circle(470,140,30,{stroke:C.red,fill:C.redSoft});
 d.at(S+'.1',0.8).arrow(480,160,600,206,{sw:3,stroke:C.red}); d.at(S+'.1',1.0).circle(610,220,30,{stroke:C.red,fill:C.redSoft});
 d.at(S+'.2',0).circle(700,220,30,{stroke:C.green,fill:'#dcfce7'}); d.at(S+'.2',0.2).circle(520,220,30,{stroke:C.green,fill:'#dcfce7'});
 d.at(S+'.2',0.5).text(500,285,'hop toward the query, drop a layer when stuck, then look around: the nearest friends',{size:24,color:C.red,font:'Caveat'});
""",
'hnsw_ef': bars([('effort 10', 0.563, 'red', 'recall 0.56 · 0.12 ms'), ('effort 20', 0.787, 'orange', 'recall 0.79 · 0.15 ms'), ('effort 50', 0.963, 'teal', 'recall 0.96 · 0.20 ms'),
                 ('effort 100', 0.998, 'green', 'recall 1.00 · 0.24 ms'), ('effort 200', 1.0, 'green', 'recall 1.00 · 0.34 ms')], [0, 0, 0, 1, 1], 1.0,
                head=('search effort (ef)', 'recall@10 and time per query (exact search: 1.21 ms)'), x0=200, wmax=380, y0=44, dy=52, bh=36,
                note=('about 0.2 ms at 96% recall, six times faster than exact', 1, 'green')),
'mini_thumb': mini2('20,000 small files', '1.34 s', 'red', 'one 80 MB shard', '0.05 s', 'green', 'read 80 MB (measured)'),
'mini_files': mini2('20,000 files', '1.34 s', 'red', 'one shard', '0.05 s', 'green', '25x slower, same 80 MB'),
'mini_vec': mini2('float32 vectors', '153.6 MB', 'grey', 'int8 vectors', '38.4 MB', 'green', 'recall@10 stays 0.985'),
'mini_egress': mini2('store 100 TB', 'cheap', 'green', 'move 100 TB out', '$9,000', 'red', 'at the ~$0.09/GB list price'),
}
