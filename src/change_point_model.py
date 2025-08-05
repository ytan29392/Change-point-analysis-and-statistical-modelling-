import numpy as np
import pymc3 as pm
import arviz as az
import matplotlib.pyplot as plt
import pandas as pd

def prepare_data(df, column='Price', sample_size=2000):
    """
    Prepare log returns for change point analysis.
    """
    df['Log_Returns'] = np.log(df[column] / df[column].shift(1))
    df.dropna(inplace=True)
    return df['Log_Returns'].values[-sample_size:], df.index[-sample_size:]

def run_change_point_model(data):
    """
    Run Bayesian change point detection using PyMC3.
    Returns the trace object.
    """
    with pm.Model() as model:
        tau = pm.DiscreteUniform('tau', lower=0, upper=len(data)-1)
        mu_1 = pm.Normal('mu_1', mu=np.mean(data), sigma=np.std(data))
        mu_2 = pm.Normal('mu_2', mu=np.mean(data), sigma=np.std(data))
        sigma = pm.HalfNormal('sigma', sigma=1)
        mu = pm.math.switch(tau >= np.arange(len(data)), mu_1, mu_2)
        likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=data)
        trace = pm.sample(2000, tune=1000, target_accept=0.95, return_inferencedata=True)
    return trace

def summarize_results(trace):
    """
    Print summary and plot traces.
    """
    print(az.summary(trace, var_names=['tau', 'mu_1', 'mu_2']))
    az.plot_trace(trace, var_names=['tau', 'mu_1', 'mu_2'])
    plt.show()

def get_change_point(trace, date_index):
    """
    Extract most probable change point date.
    """
    tau_posterior = trace.posterior['tau'].values.flatten()
    most_probable_tau = int(np.median(tau_posterior))
    change_point_date = date_index[most_probable_tau]
    return most_probable_tau, change_point_date

def plot_change_point(data, date_index, change_point_date):
    """
    Plot log returns with detected change point.
    """
    plt.figure(figsize=(14,7))
    plt.plot(date_index, data, label='Log Returns')
    plt.axvline(x=change_point_date, color='red', linestyle='--', label='Change Point')
    plt.title('Bayesian Change Point Detection')
    plt.legend()
    plt.show()

def calculate_impact(trace):
    """
    Calculate mean before and after the change point and the percentage difference.
    """
    mu_1_samples = trace.posterior['mu_1'].values.flatten()
    mu_2_samples = trace.posterior['mu_2'].values.flatten()
    
    mu_1_mean = mu_1_samples.mean()
    mu_2_mean = mu_2_samples.mean()
    
    impact_pct = ((mu_2_mean - mu_1_mean) / abs(mu_1_mean)) * 100
    
    return mu_1_mean, mu_2_mean, impact_pct

def match_event(change_point_date, events_df, days_threshold=30):
    """
    Find the closest event to the detected change point within a given threshold (days).
    """
    events_df['Date'] = pd.to_datetime(events_df['Date'])
    time_diff = abs(events_df['Date'] - change_point_date)
    closest_event = events_df.loc[time_diff.idxmin()]
    
    if time_diff.min().days <= days_threshold:
        return closest_event['Event'], closest_event['Date']
    else:
        return None, None
