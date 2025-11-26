import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# Page configuration
st.set_page_config(
    page_title="Performance Log Analyzer Dashboard",
    page_icon="",
    layout="wide"
)

# Title
st.title("Performance Log Analyzer Dashboard")
st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a performance log file (.jsonl)",
    type=['jsonl'],
    help="Select a JSONL file containing performance metrics"
)

if uploaded_file is not None:
    try:
        # Read and parse JSONL file
        lines = uploaded_file.read().decode('utf-8').split('\n')
        data = []
        
        for line in lines:
            if line.strip():  # Skip empty lines
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        if not data:
            st.error("No valid JSON data found in the file.")
        else:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Ensure timestamp is datetime if it exists
            if 'timestamp' in df.columns:
                try:
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                except:
                    pass
            
            # Display file info
            st.success(f"Successfully loaded {len(df)} records")
            st.info(f"Columns found: {', '.join(df.columns.tolist())}")
            st.markdown("---")
            
            # Check if required columns exist
            available_metrics = {
                'cpu_user': 'cpu_user' in df.columns,
                'cpu_sys': 'cpu_sys' in df.columns,
                'cpu_idle': 'cpu_idle' in df.columns,
                'mem_percent': 'mem_percent' in df.columns,
                'gpu_util': 'gpu_util' in df.columns,
                'ctx_switches': 'ctx_switches' in df.columns
            }
            
            # 2x2 Grid Layout
            # Row 1
            col1, col2 = st.columns(2)
            
            with col1:
                if available_metrics['cpu_user']:
                    st.subheader("CPU User")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.plot(df['timestamp'], df['cpu_user'], color='#1f77b4', linewidth=1.5)
                    ax.set_xlabel('Timestamp')
                    ax.set_ylabel('CPU User (%)')
                    ax.set_title('CPU User Over Time')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.warning("cpu_user column not found")
            
            with col2:
                if available_metrics['cpu_sys']:
                    st.subheader("CPU System")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.plot(df['timestamp'], df['cpu_sys'], color='#ff7f0e', linewidth=1.5)
                    ax.set_xlabel('Timestamp')
                    ax.set_ylabel('CPU System (%)')
                    ax.set_title('CPU System Over Time')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.warning("cpu_sys column not found")
            
            # Row 2
            col3, col4 = st.columns(2)
            
            with col3:
                if available_metrics['mem_percent']:
                    st.subheader("Memory Usage")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.plot(df['timestamp'], df['mem_percent'], color='#d62728', linewidth=1.5)
                    ax.set_xlabel('Timestamp')
                    ax.set_ylabel('Memory Usage (%)')
                    ax.set_title('Memory Usage Over Time')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.warning("mem_percent column not found")
            
            with col4:
                if available_metrics['gpu_util']:
                    st.subheader("GPU Utilization")
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.plot(df['timestamp'], df['gpu_util'], color='#9467bd', linewidth=1.5)
                    ax.set_xlabel('Timestamp')
                    ax.set_ylabel('GPU Utilization (%)')
                    ax.set_title('GPU Utilization Over Time')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                else:
                    st.warning("gpu_util column not found")
            
            st.markdown("---")
            
            # Additional metrics below the grid
            if available_metrics['cpu_idle']:
                st.header("CPU Idle")
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(df['timestamp'], df['cpu_idle'], color='#2ca02c', linewidth=1.5)
                ax.set_xlabel('Timestamp')
                ax.set_ylabel('CPU Idle (%)')
                ax.set_title('CPU Idle Over Time')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            if available_metrics['ctx_switches']:
                st.header("Context Switches")
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(df['timestamp'], df['ctx_switches'], color='#8c564b', linewidth=1.5)
                ax.set_xlabel('Timestamp')
                ax.set_ylabel('Context Switches')
                ax.set_title('Context Switches Over Time')
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            
            st.markdown("---")
            
            # Data preview
            with st.expander("View Raw Data"):
                st.dataframe(df, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.exception(e)

else:
    # Instructions when no file is uploaded
    st.info("Please upload a JSONL file to begin analysis")
    
    st.markdown("### Expected File Format")
    st.code("""
{"timestamp": "2024-01-01T10:00:00", "cpu_user": 25.5, "cpu_sys": 10.2, "cpu_idle": 64.3, "mem_percent": 45.8, "gpu_util": 30.0, "ctx_switches": 1000}
{"timestamp": "2024-01-01T10:00:01", "cpu_user": 26.1, "cpu_sys": 10.5, "cpu_idle": 63.4, "mem_percent": 46.2, "gpu_util": 32.0, "ctx_switches": 1050}
...
    """, language="json")
    
    st.markdown("### Metrics Analyzed")
    st.markdown("""
    - **CPU User**: User-space CPU usage percentage
    - **CPU System**: System/kernel CPU usage percentage
    - **CPU Idle**: Idle CPU percentage
    - **Memory Percent**: Memory usage percentage
    - **GPU Utilization**: GPU usage percentage
    - **Context Switches**: Number of context switches
    """)

# ============================================================================
# FUTURE FEATURES (Commented for future implementation)
# ============================================================================

# TODO: Combined CPU view (user/sys/idle overlay)
# def plot_combined_cpu(df):
#     """
#     Create a combined CPU view showing user, system, and idle CPU usage
#     overlaid on the same chart.
#     """
#     fig, ax = plt.subplots(figsize=(12, 6))
#     ax.plot(df['timestamp'], df['cpu_user'], label='CPU User', color='#1f77b4')
#     ax.plot(df['timestamp'], df['cpu_sys'], label='CPU System', color='#ff7f0e')
#     ax.plot(df['timestamp'], df['cpu_idle'], label='CPU Idle', color='#2ca02c')
#     ax.set_xlabel('Timestamp')
#     ax.set_ylabel('CPU Usage (%)')
#     ax.set_title('Combined CPU Metrics')
#     ax.legend()
#     ax.grid(True, alpha=0.3)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     return fig

# TODO: GPU vs CPU correlation graph
# def plot_gpu_cpu_correlation(df):
#     """
#     Create a scatter plot or dual-axis plot showing correlation between
#     GPU utilization and CPU usage.
#     """
#     fig, ax1 = plt.subplots(figsize=(12, 6))
#     ax2 = ax1.twinx()
#     
#     ax1.plot(df['timestamp'], df['cpu_user'], label='CPU User', color='#1f77b4')
#     ax2.plot(df['timestamp'], df['gpu_util'], label='GPU Util', color='#9467bd')
#     
#     ax1.set_xlabel('Timestamp')
#     ax1.set_ylabel('CPU Usage (%)', color='#1f77b4')
#     ax2.set_ylabel('GPU Utilization (%)', color='#9467bd')
#     ax1.set_title('GPU vs CPU Correlation')
#     ax1.legend(loc='upper left')
#     ax2.legend(loc='upper right')
#     ax1.grid(True, alpha=0.3)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     return fig

# TODO: Export graph as PNG
# def export_chart_as_png(fig, filename):
#     """
#     Export a matplotlib figure as PNG file.
#     """
#     fig.savefig(filename, dpi=300, bbox_inches='tight')
#     return filename

# TODO: Rolling average smoothing toggle
# def apply_rolling_average(df, column, window_size=10):
#     """
#     Apply rolling average smoothing to a column.
#     """
#     return df[column].rolling(window=window_size, center=True).mean()

# TODO: Multi-file comparison mode
# def compare_multiple_files(file_list):
#     """
#     Allow uploading multiple JSONL files and compare metrics across them.
#     """
#     # Implementation would involve:
#     # 1. Parse multiple files
#     # 2. Add source identifier to each dataframe
#     # 3. Plot metrics with different colors/styles for each file
#     pass
