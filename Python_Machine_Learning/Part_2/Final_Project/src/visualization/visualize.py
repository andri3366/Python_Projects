"""Visualization and PDF report generation utilities for all datasets."""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

from sklearn.metrics import accuracy_score, confusion_matrix, silhouette_score
from src.config.datasets import datasets

def create_report(dataset_name, models, X, raw_df, processed_df, scaled_df):
    """Create a multi-page PDF report for a supervised learning dataset."""
    
    config = datasets[dataset_name]
    pdf = PdfPages(str(REPORTS_DIR / f"{dataset_name}_report.pdf"))
        
    with pdf as r:
            print(f"Saving: reports/{dataset_name}")
            for plot in config["plot"]:
                
                if plot.get("data", "raw") == "raw":
                    df = raw_df
                else:
                    df = processed_df
                    
                if plot["type"] == "scatterplot":
                    fig = plot_scatter(
                        df,
                        plot["x"],
                        plot["y"],
                        plot.get("hue", None)
                    )
                        
                    r.savefig(fig)
                    plt.close(fig)
                        
                if plot["type"] == "boxplot":
                    fig = plot_box(
                        df,
                        plot["x"],
                        plot["y"]
                    )
                        
                    r.savefig(fig)
                    plt.close(fig)
                        
                if plot["type"] == "histplot":
                        
                    fig = plot_hist(
                        df,
                        plot["df"]
                    )
                        
                    r.savefig(fig)
                    plt.close(fig)
                        
                if plot["type"] == "heatmap":
                        
                    fig = plot_corr_heatmap(df)
                    r.savefig(fig)
                    plt.close(fig)
                    
                if plot["type"] == "countplot":
                    fig = single_bar(
                        df, 
                        plot["x"]
                    )
                    
                    r.savefig(fig)
                    plt.close(fig)
                
                if plot["type"] == "distplot":
                    fig = dist(
                        df,
                        scaled_df,
                        x=plot["x"],
                        compare_scaled=plot.get("compare_scaled", False)
                    )
                    
                    r.savefig(fig)
                    plt.close(fig)
            
            for model, model_config in zip(models, config["models"]):
                
                if hasattr(model, "feature_importances_"):
                    
                    print("Creating feature")
                    fig = plot_feature_importance(model, X)
                    r.savefig(fig)
                    plt.close(fig)
                    
                if hasattr(model, "loss_curve_"):
                    print("Plotting loss curve")
                    fig = plot_loss_curve(model, title=f"Activation: {model_config.get('kwargs', {}).get('activation', 'relu')}")
                    r.savefig(fig)
                    plt.close(fig)
                    
def create_cluster_report(pdf, model, X, feature_name, n_clusters):
    """Append cluster scatter visuals for two-feature clustering inputs."""
    
    if X.shape[1] == 2:

        fig = cluster_scatter(X, model.labels_, model.cluster_centers_, feature_name, n_clusters)

        pdf.savefig(fig)
        plt.close(fig)

    else:
        return None

def create_cluster_metrics(pdf, cluster_range, inertia, sil, feature_name):
    """Append elbow and silhouette metric plots for clustering diagnostics."""

    fig = elbow_plot(cluster_range, inertia, feature_name)

    pdf.savefig(fig)
    plt.close(fig)

    fig = silhouette_plot(cluster_range, sil, feature_name)

    pdf.savefig(fig)
    plt.close(fig)

def create_pair(r, df):
    """Append a pairplot overview for exploratory clustering analysis."""
    
    g = sns.pairplot(df)

    r.savefig(g.figure)
    plt.close(g.figure)

def cluster_scatter(X, labels, centers, feature_name, n_clusters):
    """Build a scatter plot showing cluster assignments and centroids."""
    fig, ax = plt.subplots()
    
    sns.scatterplot(
            x=X.iloc[:,0],
            y=X.iloc[:,1],
            hue=labels,
            palette="tab10",
            ax=ax
        )
    plt.scatter(centers[:,0], centers[:,1], c='black', s=200, alpha=0.5)

    ax.set_xlabel(X.columns[0])
    ax.set_ylabel(X.columns[1])
    ax.set_title(f"KMeans {n_clusters} Clusters for {feature_name}")

    return fig

def elbow_plot(cluster_range, inertias, feature_name):
    """Build an elbow plot from inertia values across candidate k values."""

    fig, ax = plt.subplots()

    ax.plot(cluster_range, inertias, marker='o')

    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Inertia")
    ax.set_title(f"KMeans {feature_name} Elbow Method")

    return fig

def silhouette_plot(cluster_range, silhouettes, feature_name):
    """Build a silhouette score line plot across candidate k values."""

    fig, ax = plt.subplots()

    ax.plot(cluster_range, silhouettes, marker='o')

    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Silhouette Score")
    ax.set_title(f"KMeans {feature_name} Silhouette Method")

    return fig

def plot_scatter(df, x, y, hue):
    """Create a scatter plot with an optional hue grouping."""
    
    fig, ax = plt.subplots()
    
    if hue is None:
        sns.scatterplot(x=x, y=y, data=df, ax=ax)       
    else:
        sns.scatterplot(x=x, y=y, hue=hue, data=df, ax=ax)
    
    ax.set_title(f"Scatter plot {x} to {y}")
    ax.set_ylabel(f"{y}")
    ax.set_xlabel(f"{x}")
    
    return fig
    
def plot_box(df, x, y=None):
    """Create a one-variable or two-variable box plot."""
    
    fig, ax = plt.subplots()
    
    if y is None:
        sns.boxplot(x=x, data=df, ax=ax)
        ax.set_title(f"Box plot {x}")
        ax.set_xlabel(f"{x}")
    if y is not None:
        sns.boxplot(x=x, y=y, data=df, ax=ax)
        ax.set_title(f"Box plot {x} to {y}")
        ax.set_ylabel(f"{y}")
        ax.set_xlabel(f"{x}")
    
    return fig   

def plot_hist(df, x):
    """Create a histogram for a selected numeric feature."""

    fig, ax = plt.subplots()
    
    sns.histplot(data=df, x=x, ax=ax)
    
    ax.set_title(f"Histogram plot {x}")
    
    return fig

def plot_corr_heatmap(df):
    """Create a correlation heatmap for numeric columns."""
    
    fig, ax = plt.subplots()
    
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    
    ax.set_title("Correlation Matrix")
    
    return fig

def single_bar(df, x):
    """Create a count plot for a categorical feature."""
    
    fig, ax = plt.subplots()
    sns.countplot(data=df, x=x)
    
    ax.set_title(f"Count Plot of {x}")
    return fig

def dist(og_df, scaled_df, x, compare_scaled=False):
    """Create distribution plots and optionally compare scaled vs original."""
    
    
    if compare_scaled:
        fig, (ax1, ax2)= plt.subplots(1,2, figsize=(10,4))
        sns.histplot(
            data = og_df, x=x, kde=True, stat="density", ax=ax1
        )
        
        sns.histplot(
            data = scaled_df, x=x, kde=True, stat="density", ax=ax2
        )
        ax2.set_title(f"Scaled {x}")
        ax1.set_title(f"Original {x}")
    
    else:
        fig, ax = plt.subplots()
        sns.histplot(
            data = og_df, x=x, kde=True, stat="density", ax=ax
        )
        
        ax.set_title(f"Original {x}")
    return fig
def plot_feature_importance(model, X):
    """Create a feature-importance bar chart for tree-based models."""
    
    fig, ax = plt.subplots()
    
    sns.barplot(
        x=model.feature_importances_,
        y=X.columns,
        ax=ax
    )
    
    
    ax.set_title(f"{type(model).__name__} Feature Importance")
    plt.tight_layout()
    
    return fig

def plot_loss_curve(model, title):
    """Create a neural-network training loss curve plot."""
    fig, ax = plt.subplots()
    
    ax.plot(model.loss_curve_, label='Loss', color='blue')
    
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Loss")
    ax.set_title(title)
    ax.grid(True)
    
    return fig