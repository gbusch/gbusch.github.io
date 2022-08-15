---
title: "Bayesian Anomaly Detection in Time Series Data"
date: 2022-08-04T18:56:04+02:00
draft: true
---
{{< katex >}}

{{< lead >}}
Find anomalous data in time series using Bayesian statistics.
{{< /lead >}}

In a recent project, we were asked to detect anomalies in time series data. The special aspect was that the time series data resembled error rates, a quotient of the number of errors and a reference number, here the number of operations that were able to fail at that date. 

![Error Rate Time Series](/blog/bayesian-anomaly-detection/error-rate-timeseries.png)

We wanted to make use not only of the ratio but numbers that form it: Heuristically, you would be more confident about an error rate of 0.1 = 10,000 errors / 100,000 operations compared to the same but 0.1 = 1 error / 10 operations.

In a Bayesian approach, we do not just compare error rates with each other. Instead, we want to derive probability distributions for both, the current date and a comparison interval and compare these.

## Bayes' theorem

The Bayes' theorem helps us to derive the posterior distribution of the error rate based on our prior belief and the observed data.

Let us consider the success of an operation to be _Bernoulli distributed_. This means an error occurs with a probability of \\(\theta\\). 

Given a number of operations (reference) \\(N_r\\), the absolute number of errors will then follow a _Binomial distribution_:
\\( P(N_e | N_r, \theta) = \binom{N_r}{N_e} \theta^{N_e} (1-\theta)^{N_r-N_e} \\).

The Bayes' theorem now tells us how to derive the posterior probability, that means the probability distribution of the intrinsic error rate given our previous belief/knowledge and our observation of successful and failing operations:

{{< alert " " >}}
$$ P(\theta | N_e, N_r) \propto P(N_e | N_r, \theta) \times P(\theta) $$
{{< /alert >}}

But what is our prior probability? In doubt, we use an uninformed prior that gives equal weight to all values of \\(\theta\\) between 0 and 1 which can be modeled with a Beta function Beta(1, 1).

The great thing in this setup is that the Beta distribution is the _conjugate prior_ of the Binomial distribution. What this means is that given a Binomial likelihood and a Beta prior, the posterior is again a Beta distribution. Moreover, we get a simple update rule that saves us a lot of computation.


## Beta distribution

Let us first have a look at the Beta distribution. The function is defined in the interval between 0 and 1 and parametrized by two positive shape parameters which are usually denoted \\(\alpha\\) and \\(\beta\\). 

If both shape parameters have the value \\(\alpha = \beta = 1\\), the distribution is uniform between 0 and 1, resembling a so-called uninformed prior, meaning, all values between 0 and 1 are considered equally likely.

Using the knowledge from above, we can now use the observed data to calculate the posterior distribution: The simple update rule is: \\(\alpha' = N_e + \alpha \\) and \\(\beta' = (N_r - N_e) +\beta \\). Heuristically, this means the parameters \\(\alpha\\) and \\(\beta\\) denote the number of positive (here errors) and negative (here reference minus errors) outcomes of the experiment (plus 1 for our uninformed prior).

In the plot we can see that the distribution peaks around the expected error rate (errors / reference operations) and also that the peak is much narrower when we have more data.

![Beta Distribution](/blog/bayesian-anomaly-detection/beta-distribution.png)
