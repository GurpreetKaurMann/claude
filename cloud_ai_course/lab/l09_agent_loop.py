"""Lesson 9 lab C: a WORKING agent loop, with a SCRIPTED stand-in for the model (no language model is called).

The 'model' is a rule-based function that picks the next tool from what has happened so far. The loop has the parts a real agent needs:
a step budget (stop condition), tool errors returned to the model as results, an approval gate before a risky tool, and a checkpoint saved
after every step. Task: look up an order, check the refund policy, ISSUE A REFUND (needs approval), email the customer, close the ticket (10 steps).
We crash the process at step 7, then recover two ways: RESTART from step 1, or RESUME from the checkpoint. Side effects (refunds issued, emails sent) are counted
with and without idempotency keys. Run: python3 l09_agent_loop.py
"""
import json, os, tempfile
PLAN = ['lookup_order', 'lookup_order', 'read_policy', 'check_eligibility', 'draft_reply', 'request_approval', 'issue_refund', 'send_email', 'update_ticket', 'finish']
class Crash(Exception): pass

class World:                                      # the outside world: counts real side effects
    def __init__(self): self.refunds, self.emails, self.calls, self.seen_keys = 0, 0, 0, set()
def run_tool(world, name, step, use_keys):
    key = f'refund-order-1001' if name == 'issue_refund' else f'email-order-1001' if name == 'send_email' else None
    world.calls += 1
    if use_keys and key and key in world.seen_keys: return 'skipped: already done (idempotency key)'
    if name == 'lookup_order' and step == 0: return 'ERROR: order id must be a string'      # a tool error goes back to the model
    if key: world.seen_keys.add(key)
    if name == 'issue_refund': world.refunds += 1
    if name == 'send_email': world.emails += 1
    return f'ok: {name}'

def agent(world, ckpt, use_keys, crash_at=None, budget=12, resume=True):
    state = json.load(open(ckpt)) if (resume and os.path.exists(ckpt)) else {'step': 0, 'log': []}
    while True:
        if state['step'] >= budget: raise RuntimeError('step budget exceeded')          # stop condition 1: fail loudly
        name = PLAN[state['step']]                                                      # the scripted 'model' chooses the tool
        if name == 'finish': return state
        if name == 'request_approval': state['log'].append('approved by human')          # approval gate (stand-in)
        else:
            if crash_at is not None and state['step'] == crash_at: raise Crash(f'process died at step {state["step"] + 1}')
            state['log'].append(run_tool(world, name, state['step'], use_keys))
        state['step'] += 1; json.dump(state, open(ckpt, 'w'))                           # checkpoint after every step

def scenario(label, resume, use_keys):
    w = World(); ck = tempfile.mktemp()
    try: agent(w, ck, use_keys, crash_at=7, resume=resume)
    except Crash: pass
    if not resume and os.path.exists(ck): os.remove(ck)                                 # a plain restart forgets everything
    st = agent(w, ck, use_keys, resume=resume)
    print(f'{label:34} tool calls in total: {w.calls:2d} · refunds issued: {w.refunds} · emails sent: {w.emails}')
print('the process dies just before the email step (step 8 of 9), then we recover (a tool error at step 1 is returned to the agent and handled)')
scenario('restart from step 1, no keys', resume=False, use_keys=False)
scenario('restart from step 1, with keys', resume=False, use_keys=True)
scenario('resume from checkpoint, no keys', resume=True, use_keys=False)
scenario('resume from checkpoint, with keys', resume=True, use_keys=True)
