import matplotlib.pyplot as plt
import numpy as np
from numpy.random import binomial, normal
from scipy.stats import beta

plt.style.use('fivethirtyeight')

# Error rate
np.random.seed(42)
x = np.arange(100)
ref = np.array([100]*50 + [500]*20 + [200]*30)
err = np.array([binomial(n, 0.1) for n in ref])
err[10:12]+=10
err[60:62]+=50
err_rate = err / ref
plt.figure()
plt.title("Time series: error rate")
plt.xlabel("time")
plt.ylabel("error rate")
plt.plot(x, err_rate)
for day in [54, 34, 11, 61]:
    plt.axvline(day, alpha=0.1)
plt.savefig("static/blog/bayesian-anomaly-detection/error-rate-timeseries.png")


for day in [54, 34, 11, 61]:
    xrange = np.arange(0, 0.5, 0.001)
    plt.figure()
    plt.title(f"Day {day}")
    plt.plot(xrange, beta.pdf(xrange, err[day-7:day].sum()+1, ref[day-7:day].sum()-err[day-7:day].sum()+1), label="7 days before", c='C0')
    plt.plot(xrange, beta.pdf(xrange, err[day]+1, ref[day]-err[day]+1), label="current date", c='C1')
    x95 = beta.ppf(0.95, err[day-7:day].sum()+1, ref[day-7:day].sum()-err[day-7:day].sum()+1)
    plt.axvline(x95, c='C0')
    plt.fill_between(
        xrange[xrange<=x95],
        beta.pdf(xrange[xrange<=x95], err[day]+1, ref[day]-err[day]+1),
        color='C1',
        alpha=0.5,
    )
    print(
        beta.cdf(
            beta.ppf(0.95, err[day-7:day].sum()+1, ref[day-7:day].sum()-err[day-7:day].sum()+1),
            err[day]+1, ref[day]-err[day]+1
        )
    )
    plt.legend()
    plt.savefig(f"static/blog/bayesian-anomaly-detection/distributions-day{day}.png")


# Beta distribution
xrange = np.arange(0, 1., 0.001)
plt.figure()
plt.title("Beta distribution")
plt.plot(xrange, beta.pdf(xrange, 1, 1), label="Beta(1, 1)")
plt.plot(xrange, beta.pdf(xrange, 10, 10), label="Beta(10, 10)")
plt.plot(xrange, beta.pdf(xrange, 1000, 1000), label="Beta(1000, 1000)")
plt.legend()
plt.savefig("static/blog/bayesian-anomaly-detection/beta-distribution.png")