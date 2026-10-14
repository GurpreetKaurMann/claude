from cai_lib import bars, boxes, mini2

DIAGRAMS = {
'loop': boxes([('Inform', 'see it: tag, meter, publish unit costs', 'blue'), ('Optimize', 'fix it: rates and usage', 'teal'), ('Operate', 'keep it fixed: budgets, alerts', 'green')], [0, 1, 1], y=50, h=180, arrows=True, size=38,
              note=('I-O-O: see it, fix it, keep it fixed', 1, 'green')),
'realprice': bars([('5% used', 63.40, 'red', '$63.40'), ('22% used', 14.41, 'orange', '$14.41'), ('50% used', 6.34, 'teal', '$6.34'), ('80% used', 3.96, 'green', '$3.96'), ('100% used', 3.17, 'green', '$3.17 (the sticker price)')], [0, 0, 1, 1, 1], 65,
                  head=('utilisation', 'real price per USEFUL GPU-hour, H100 listed at $3.17 (arithmetic)'), x0=190, wmax=470, y0=44, dy=50, bh=36, note=('5% to 50% used: ten times cheaper, no negotiating', 1, 'green')),
'five': bars([('index $3.17', 68168, 'green', '$68,168'), ('market $3.84', 82575, 'teal', '$82,575'), ('capacity block', 128379, 'orange', '$128,379'), ('on-demand', 147948, 'red', '$147,948'), ('spot ~60% off', 27267, 'green', '$27,267 + restarts')], [0, 0, 1, 1, 1], 150000,
              head=('how you pay', '64 GPUs for 14 days = 21,504 GPU-hours (arithmetic, Sep-Oct 2026 prices)'), x0=210, wmax=480, y0=44, dy=50, bh=36, note=('the same job costs up to 5.4 times more, depending on how you buy', 1, 'red')),
'bot': bars([('no cache', 12000, 'red', '$12,000'), ('cache hit', 6300, 'orange', '$6,300'), ('cascade', 4200, 'teal', '$4,200'), ('batch + hit', 3150, 'green', '$3,150')], [0, 0, 1, 1], 12000,
            head=('lever', 'Sonnet 5.5 support bot, cost per million requests (arithmetic, list prices 14 Oct 2026)'), x0=210, wmax=470, y0=44, dy=56, bh=40, note=('cache first, then batch, then model choice', 1, 'green')),
'ttl': bars([('1 per minute', 99.2, 'green', '99.2% hit'), ('1 per 10 min', 38.9, 'orange', '38.9% hit'), ('1 per hour', 8.0, 'red', '8.0% hit')], [0, 1, 1], 100,
            head=('traffic', 'cache hit rate with a five-minute lifetime (simulated, formula 1 - e^(-rate x time) agrees)'), x0=230, wmax=420, y0=44, dy=60, bh=42, note=('a cache only helps if requests keep arriving', 1, 'orange')),
'ts': bars([('timestamp at top', 0.3, 'red', '0% of tokens cached'), ('timestamp after', 74.9, 'green', '74.9% cached')], [0, 1], 100,
           head=('field position', 'share of tokens served from a toy prefix cache (measured, 5,000 requests)'), x0=250, wmax=420, y0=50, dy=70, bh=48, note=('input bill: 3.5 times higher with the timestamp on top', 1, 'red')),
'breakeven': bars([('Opus 5.5 API', 10.6, 'green', '10.6M'), ('Sonnet 5.5 API', 21.1, 'orange', '21.1M'), ('Haiku 5.5 API', 45, 'red', '422.7M: off the chart')], [0, 0, 1], 45,
                  head=('API you compare with', 'millions of tokens per day before ONE H100 beats it (arithmetic)'), x0=230, wmax=500, y0=50, dy=60, bh=42, line=(34.6, 'one H100 tops out at 34.6M', 1, 'red')),
'ckpt': bars([('keep 48 hourly', 1236, 'red', '$1,236 a month'), ('keep last 3', 77, 'green', '$77 a month')], [0, 1], 1236,
             head=('checkpoint policy', '70B model, 1,120 GB per full checkpoint (arithmetic, assumed prices)'), x0=210, wmax=420, y0=50, dy=70, bh=48, note=('94% cheaper, same safety', 1, 'green')),
'mini_thumb': mini2('H100 listed $3.17, used 5%', '$63.40', 'red', 'same GPU, used 50%', '$6.34', 'green', 'real price per useful GPU-hour', fs=30, vs=50),
'mini_ts': mini2('timestamp at the TOP', '0% cached', 'red', 'timestamp AFTER', '75% cached', 'green', 'toy prefix cache, 5,000 requests', fs=32, vs=44),
'mini_be': mini2('Sonnet API: one H100 wins above', '21M/day', 'amber', 'Haiku API: one H100 wins above', '423M/day', 'red', 'tokens per day, one GPU holds 35M', fs=28, vs=44),
}
