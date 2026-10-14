from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'pipeline': (boxes([('1 Parse', 'read the files', 'blue'), ('2 Chunk', 'cut into pieces', 'teal'), ('3 Context', 'say where it came from', 'orange'), ('4 Embed', 'turn into vectors', 'green')], [0, 0, 1, 1], y=10, h=120, arrows=True, size=26)
             + boxes([('5 Hybrid', 'keywords + vectors', 'blue'), ('6 Rerank', 'sort the best', 'teal'), ('7 Generate', 'answer + citations', 'red')], [2, 2, 2], y=160, h=120, arrows=True, size=26)),
'chunk_hit3': bars([('BM25, 100 words', 83.3, 'orange', '83.3%'), ('BM25, 300 words', 87.5, 'green', '87.5%'), ('BM25, 800 words', 79.2, 'red', '79.2%'), ('dense, 100 words', 83.3, 'orange', '83.3%'), ('dense, 300 words', 91.7, 'green', '91.7%'), ('dense, 800 words', 87.5, 'orange', '87.5%')],
                   [0, 0, 0, 1, 1, 1], 100, head=('retriever, chunk size', 'answer found in the top 3 chunks (measured, 24 questions)'), x0=270, wmax=450, y0=40, dy=48, bh=34),
'methods300': bars([('BM25', 87.5, 'teal', '87.5%'), ('dense (LSA stand-in)', 91.7, 'green', '91.7%'), ('hybrid (RRF)', 87.5, 'teal', '87.5%')], [0, 1, 2], 100,
                   head=('retriever, 300-word chunks', 'answer found in the top 3 (measured)'), x0=290, wmax=430, y0=50, dy=64, bh=42, note=('the fancy fusion did not win here', 2, 'red')),
'overlap': boxes([('both found it', '21 questions', 'green'), ('only BM25', '0', 'blue'), ('only dense', '1', 'orange'), ('neither', '2', 'red')], [0, 0, 1, 1], y=50, h=180, size=26,
                 note=('fusion needs methods that fail on DIFFERENT questions', 1, 'red')),
'ctx': bars([('BM25, plain', 83.3, 'gray', '83.3%'), ('BM25 + title', 83.3, 'gray', '83.3%'), ('dense, plain', 83.3, 'gray', '83.3%'), ('dense + title', 87.5, 'teal', '87.5%')], [0, 0, 1, 1], 100,
            head=('100-word chunks', 'answer found in the top 3 (measured)'), x0=250, wmax=470, y0=50, dy=60, bh=42, note=('a title prefix is a very weak form of context', 1, 'orange')),
'longctx': boxes([('under about 200K tokens', 'stable, one tenant', 'green'), ('include it all', 'cache the prompt', 'teal'), ('larger or changing', 'permissions, many tenants', 'orange'), ('use RAG', 'retrieve per question', 'red')], [0, 0, 1, 1], y=50, h=180, size=26,
              note=('cached long prompt: over 2x lower latency, up to 90% cheaper (vendor)', 1, 'blue')),
'mini_thumb': mini2('300-word chunks', '91.7%', 'green', '800-word chunks', '87.5%', 'amber', 'answer in the top 3, measured'),
'mini_chunks': mini2('100-word chunks (BM25)', '83.3%', 'amber', '300-word chunks (BM25)', '87.5%', 'green', 'answer in the top 3', fs=32),
'mini_hybrid': mini2('dense alone', '91.7%', 'green', 'hybrid (RRF)', '87.5%', 'red', '300-word chunks, top 3'),
'mini_long': mini2('under ~200K tokens', 'skip RAG', 'green', 'larger or changing', 'use RAG', 'rose', 'long prompt or RAG?'),
}
