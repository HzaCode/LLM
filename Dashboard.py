
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from math import pi

results = {
   
}


df = pd.DataFrame(results).T

# Multi-level Grouped Bar Chart
def plot_grouped_bar_chart():
    labels = df.index
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width, df['Precision'], width, label='Precision')
    rects2 = ax.bar(x, df['Recall'], width, label='Recall')
    rects3 = ax.bar(x + width, df['F1 Score'], width, label='F1 Score')

    ax.set_ylabel('Scores')
    ax.set_title('Performance by metric and parameter')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend()

    plt.show()

# Stacked Bar Chart
def plot_stacked_bar_chart():
    labels = df.index
    x = np.arange(len(labels))

    fig, ax = plt.subplots()
    ax.bar(labels, df['Precision'], label='Precision', color='b')
    ax.bar(labels, df['Recall'], bottom=df['Precision'], label='Recall', color='g')
    ax.bar(labels, df['F1 Score'], bottom=df['Precision'] + df['Recall'], label='F1 Score', color='r')

    ax.set_ylabel('Cumulative Scores')
    ax.set_title('Stacked Performance by Parameter')
    ax.legend()

    plt.xticks(rotation=45)
    plt.show()

# Radar Chart
def plot_radar_chart():
    categories = df.index
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], categories)

    values = df.mean(axis=1).tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Average Score")
    ax.fill(angles, values, 'b', alpha=0.1)

    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()

# Heatmap
def plot_heatmap():
    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Performance Metrics Heatmap")
    plt.show()

# Plot all charts
plot_grouped_bar_chart()
plot_stacked_bar_chart()
plot_radar_chart()
plot_heatmap()
