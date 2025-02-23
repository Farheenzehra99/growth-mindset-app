import pandas as pd
import json
import io
import plotly.express as px
import plotly.graph_objects as go

def read_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            df = pd.read_json(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
        return df
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def convert_df(df, output_format):
    try:
        if output_format == 'csv':
            return df.to_csv(index=False)
        elif output_format == 'xlsx':
            output = io.BytesIO()
            df.to_excel(output, index=False)
            return output.getvalue()
        elif output_format == 'json':
            return df.to_json(orient='records')
    except Exception as e:
        raise Exception(f"Error converting file: {str(e)}")

def clean_data(df, options):
    if 'remove_duplicates' in options:
        df = df.drop_duplicates()
    if 'drop_na' in options:
        df = df.dropna()
    if 'fill_na' in options:
        df = df.fillna(0)
    return df

def generate_visualizations(df):
    visualizations = {}

    # Basic statistics
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        # Distribution plot
        fig_dist = px.histogram(df[numeric_cols[0]], title=f'Distribution of {numeric_cols[0]}')
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        visualizations['distribution'] = fig_dist

        # Correlation heatmap
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr,
                x=corr.columns,
                y=corr.columns,
                colorscale='RdBu'
            ))
            fig_corr.update_layout(
                title='Correlation Heatmap',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            visualizations['correlation'] = fig_corr

    return visualizations

def generate_ai_suggestions(df):
    suggestions = []

    # Basic data quality checks
    missing_values = df.isnull().sum()
    if missing_values.any():
        suggestions.append("Found missing values in the dataset. Consider handling them.")

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        suggestions.append(f"Found {duplicates} duplicate rows. Consider removing them.")

    # Data type suggestions
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        suggestions.append("Consider normalizing numeric columns for better analysis.")

    categorical_cols = df.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        suggestions.append("Consider encoding categorical variables for machine learning tasks.")

    return suggestions

def apply_custom_transformation(df, transformations):
    """
    Apply custom transformations to the dataframe
    transformations: list of dictionaries containing:
        - column: column name to transform
        - operation: type of transformation
        - parameters: additional parameters for the transformation
    """
    try:
        for transform in transformations:
            column = transform.get('column')
            operation = transform.get('operation')
            parameters = transform.get('parameters', {})

            if column not in df.columns:
                continue

            if operation == 'multiply':
                factor = float(parameters.get('factor', 1))
                df[column] = pd.to_numeric(df[column], errors='coerce') * factor

            elif operation == 'round':
                decimals = int(parameters.get('decimals', 0))
                df[column] = pd.to_numeric(df[column], errors='coerce').round(decimals)

            elif operation == 'uppercase':
                df[column] = df[column].astype(str).str.upper()

            elif operation == 'lowercase':
                df[column] = df[column].astype(str).str.lower()

            elif operation == 'replace':
                old_value = parameters.get('old_value', '')
                new_value = parameters.get('new_value', '')
                df[column] = df[column].astype(str).str.replace(old_value, new_value)

        return df
    except Exception as e:
        raise Exception(f"Error applying custom transformation: {str(e)}")