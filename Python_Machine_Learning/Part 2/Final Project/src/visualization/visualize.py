import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import numpy as np

from sklearn.metrics import accuracy_score, confusion_matrix
from src.config.datasets import datasets

def create_report(dataset_name, model, X, df):
    
    config = datasets[dataset_name]
    pdf = PdfPages(f"{dataset_name}_report.pdf")
        
    with pdf as r:
            print(f"Saving: reports/{dataset_name}")
            for plot in config["plot"]:
                if plot["type"] == "scatterplot":
                    fig = plot_scatter(
                        df,
                        plot["x"],
                        plot["y"]
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
                    
            if hasattr(model, "feature_importances_"):
                
                print("Creating feature")
                fig = plot_feature_importance(model, X)
                r.savefig(fig)
                plt.close(fig)
                    

def plot_scatter(df, x, y):
    
    fig, ax = plt.subplots()
    
    sns.scatterplot(x=x, y=y, data=df, ax=ax)
    
    ax.set_title(f"Scatter plot {x} to {y}")
    ax.set_ylabel(f"{y}")
    ax.set_xlabel(f"{x}")
    
    return fig
    
def plot_box(df, x, y=None):
    
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

    fig, ax = plt.subplots()
    
    sns.histplot(data=df, x=x, ax=ax)
    
    ax.set_title(f"Histogram plot {x}")
    
    return fig

def plot_corr_heatmap(df):
    
    fig, ax = plt.subplots()
    
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    
    ax.set_title("Correlation Matrix")
    
    return fig

def single_bar(df, x):
    
    fig, ax = plt.subplots()
    sns.countplot(data=df, x=x)
    
    ax.set_title(f"Count Plot of {x}")
    return fig

def plot_feature_importance(model, X):
    
    fig, ax = plt.subplots()
    
    sns.barplot(
        x=model.feature_importances_,
        y=X.columns,
        ax=ax
    )
    
    
    ax.set_title(f"{type(model).__name__} Feature Importance")
    plt.tight_layout()
    
    return fig