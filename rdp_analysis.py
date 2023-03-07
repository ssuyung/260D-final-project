import numpy as np
from decimal import *
from scipy.special import comb

getcontext().prec = 128


def rdp2dp(rdp, bad_event, alpha):
    """
    convert RDP to DP, ref (Proposition 12):
    Canonne, Clément L., Gautam Kamath, and Thomas Steinke. The discrete gaussian for differential privacy. In NeurIPS, 2020.
    """
    return rdp + 1.0/(alpha-1) * (np.log(1.0/bad_event) + (alpha-1)*np.log(1-1.0/alpha) - np.log(alpha))

def compute_rdp(alpha, q, sigma):
    """
    RDP for subsampled Gaussian mechanism, ref:
    - Mironov, Ilya, Kunal Talwar, and Li Zhang. "R\'enyi differential privacy of the sampled gaussian mechanism." arXiv preprint 2019.
    """
    sum_ = Decimal(0.0)
    for k in range(0, alpha+1):
        sum_ += Decimal(comb(alpha, k)) * Decimal(1-q)**Decimal(alpha-k) * Decimal(q**k) * Decimal(np.e)**(Decimal(k**2-k)/Decimal(2*sigma**2))
    rdp = sum_.ln() / Decimal(alpha-1)
    return float(rdp)
        
def search_dp(q, sigma, bad_event, iters=1):
    min_dp = 1e5
    for alpha in list(range(2, 101))+[256, 512, 1024]:
        rdp = iters * compute_rdp(alpha, q, sigma)
        dp = rdp2dp(rdp, bad_event, alpha)
        min_dp = min(min_dp, dp)
    return min_dp