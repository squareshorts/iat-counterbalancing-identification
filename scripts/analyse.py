"""Identified analysis of pairing and block position in a counterbalanced IAT.

Reads the per-participant, per-block sufficient statistics and produces:
  1. cell means of the 2 (order) x 2 (block position) design
  2. a numerical check of the pairing/position identity
  3. the conventional D score and its order dependence
  4. error-rate contrasts
  5. the order-imbalance bias table
"""
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'results'
OUTT = ROOT / 'results'
OUTT.mkdir(parents=True, exist_ok=True)

def boot_ci(x, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    x = np.asarray(x); idx = rng.integers(0, len(x), size=(n, len(x)))
    m = x[idx].mean(axis=1)
    return np.percentile(m, [2.5, 97.5])

rows_summary, rows_cells, rows_bias, rows_rel = [], [], [], []

for ds, fn in [('Gender-Science', 'block_aggregates_gender_science.csv'),
               ('Age', 'block_aggregates_age.csv')]:
    p = D / fn
    if not p.exists():
        print('missing', p); continue
    b = pd.read_csv(p)
    b = b[b['n_ok'] > 0]
    b['mean_log_rt'] = b['logrt_sum'] / b['n_ok']
    b['pair'] = np.where(b['block'].isin([3, 6]), 'practice', 'test')

    # participant must have all four critical blocks with an internally
    # consistent pairing assignment: blocks 3 and 4 share one combined rule,
    # blocks 6 and 7 the reversed rule.
    n_start = b['pid'].nunique()
    wide = b.pivot_table(index='pid', columns='block', values='pairing', aggfunc='first')
    wide = wide.dropna()
    good = wide[(wide[3] == wide[4]) & (wide[6] == wide[7]) & (wide[3] != wide[6])].index
    b = b[b['pid'].isin(good)]
    n_drop = n_start - len(good)
    print(f'{ds}: {n_start} participants with critical blocks, '
          f'{n_drop} dropped for inconsistent or incomplete block coding '
          f'({100 * n_drop / n_start:.2f}%)')

    # order: pairing shown in block 3
    order = (b[b['block'] == 3].set_index('pid')['pairing']
             .rename('first_pairing'))
    b = b.join(order, on='pid')
    b['order'] = np.where(b['first_pairing'] == 'congruent',
                          'congruent_first', 'incongruent_first')

    # ---- participant-level log-latency means by pairing and by position
    w = b.pivot_table(index=['pid', 'order'], columns='pairing',
                      values='mean_log_rt', aggfunc='mean').reset_index()
    pos = b.copy()
    pos['position'] = np.where(pos['block'].isin([3, 4]), 'first', 'second')
    wp = pos.pivot_table(index='pid', columns='position',
                         values='mean_log_rt', aggfunc='mean')
    w = w.merge(wp, on='pid')
    w['C'] = w['incongruent'] - w['congruent']          # pairing contrast
    w['P'] = w['second'] - w['first']                    # position contrast
    sign = np.where(w['order'] == 'congruent_first', 1.0, -1.0)
    ident = float(np.nanmax(np.abs(w['P'] - sign * w['C'])))

    # ---- error rates
    b['err_rate'] = b['n_err'] / b['n_all']
    we = b.pivot_table(index='pid', columns='pairing', values='err_rate', aggfunc='mean')
    we.columns = ['err_' + c for c in we.columns]
    wpe = pos.assign(err_rate=pos['n_err'] / pos['n_all']).pivot_table(
        index='pid', columns='position', values='err_rate', aggfunc='mean')
    wpe.columns = ['err_' + c for c in wpe.columns]
    w = w.merge(we, on='pid').merge(wpe, on='pid')
    w['CE'] = w['err_incongruent'] - w['err_congruent']
    w['PE'] = w['err_second'] - w['err_first']

    # ---- conventional D score on the same cleaned trials
    dparts = {}
    for pr in ['practice', 'test']:
        sub = b[b['pair'] == pr]
        g = sub.pivot_table(index='pid', columns='pairing',
                            values=['n_all', 'rt_sum', 'rt_sumsq'], aggfunc='sum')
        n = g[('n_all', 'congruent')] + g[('n_all', 'incongruent')]
        s = g[('rt_sum', 'congruent')] + g[('rt_sum', 'incongruent')]
        ss = g[('rt_sumsq', 'congruent')] + g[('rt_sumsq', 'incongruent')]
        var = (ss - s ** 2 / n) / (n - 1)
        sd = np.sqrt(var)
        m_c = g[('rt_sum', 'congruent')] / g[('n_all', 'congruent')]
        m_i = g[('rt_sum', 'incongruent')] / g[('n_all', 'incongruent')]
        dparts[pr] = ((m_i - m_c) / sd).rename('d_' + pr)
    dd = pd.concat([dparts['practice'], dparts['test']], axis=1)
    dd['D'] = dd[['d_practice', 'd_test']].mean(axis=1)
    w = w.merge(dd.reset_index(), on='pid')
    w = w.replace([np.inf, -np.inf], np.nan).dropna(subset=['C', 'P', 'D'])

    # ---- summaries
    def summarise(col, label):
        x = w[col].to_numpy()
        lo, hi = boot_ci(x)
        g = w.groupby('order')[col].agg(['count', 'mean', 'std'])
        cc = g.loc['congruent_first', 'mean']; ci_ = g.loc['incongruent_first', 'mean']
        rows_summary.append(dict(dataset=ds, measure=label, n=len(x),
                                 mean=x.mean(), ci_low=lo, ci_high=hi,
                                 sd=x.std(ddof=1), d=x.mean() / x.std(ddof=1),
                                 mean_cong_first=cc, mean_incong_first=ci_,
                                 order_diff=cc - ci_,
                                 n_cong_first=g.loc['congruent_first', 'count'],
                                 n_incong_first=g.loc['incongruent_first', 'count']))
        return cc - ci_

    od_C = summarise('C', 'log-latency pairing contrast')
    summarise('P', 'log-latency position contrast')
    od_CE = summarise('CE', 'error-rate pairing contrast')
    summarise('PE', 'error-rate position contrast')
    od_D = summarise('D', 'conventional D score')

    # cell means (order x position) on raw log RT
    cm = pos.groupby(['order', 'position'])['mean_log_rt'].agg(['count', 'mean', 'std']).reset_index()
    cm.insert(0, 'dataset', ds)
    rows_cells.append(cm)

    # identity check row
    rows_summary.append(dict(dataset=ds, measure='identity max |P - sign*C|',
                             n=len(w), mean=ident))

    # split-half reliability of D by order group
    wr = w.dropna(subset=['d_practice', 'd_test'])
    for o, g in wr.groupby('order'):
        r = np.corrcoef(g['d_practice'], g['d_test'])[0, 1]
        rows_rel.append(dict(dataset=ds, order=o, n=len(g), r_halves=r,
                             spearman_brown=2 * r / (1 + r)))
    r_all = np.corrcoef(wr['d_practice'], wr['d_test'])[0, 1]
    rows_rel.append(dict(dataset=ds, order='all', n=len(wr), r_halves=r_all,
                         spearman_brown=2 * r_all / (1 + r_all)))

    # bias table: spurious group difference per order-allocation imbalance
    for dp in [0.02, 0.05, 0.10, 0.20]:
        rows_bias.append(dict(dataset=ds, imbalance=dp,
                              bias_logrt=dp * od_C,
                              pct_of_effect_logrt=100 * dp * od_C / w['C'].mean(),
                              bias_D=dp * od_D,
                              pct_of_effect_D=100 * dp * od_D / w['D'].mean(),
                              bias_error=dp * od_CE,
                              pct_of_effect_error=100 * dp * od_CE / w['CE'].mean()))

    w[['pid', 'order', 'C', 'P', 'CE', 'PE', 'D', 'd_practice', 'd_test']].to_csv(
        D / f'participant_measures_{ds.replace("-", "_").lower()}.csv', index=False)
    print(ds, 'n =', len(w), 'identity max abs dev =', ident)

pd.DataFrame(rows_summary).to_csv(D / 'summary_measures.csv', index=False)
pd.concat(rows_cells).to_csv(D / 'cell_means.csv', index=False)
pd.DataFrame(rows_bias).to_csv(D / 'bias_table.csv', index=False)
pd.DataFrame(rows_rel).to_csv(D / 'reliability.csv', index=False)
print(pd.DataFrame(rows_summary).to_string())
print(pd.concat(rows_cells).to_string())
print(pd.DataFrame(rows_bias).to_string())
print(pd.DataFrame(rows_rel).to_string())
