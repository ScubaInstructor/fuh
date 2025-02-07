import pandas as pd
import numpy as np
import argparse
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.feature_selection import VarianceThreshold
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def clean_dataset(file_path, output_path, correlation_threshold=0.9, missing_threshold=0.1, 
                  impute_strategy='mean', drop_categorical_columns=False, drop_highly_correlated=False,
                  drop_columns=None, scale_method=None, feature_selection=None, balance_method=None, assess_only=False, pca_variance=0.95):
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: The file '{file_path}' does not exist!")
        return None, None

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    report = {}

    # Print all options used
    options_used = {
        "file_path": file_path,
        "output_path": output_path,
        "correlation_threshold": correlation_threshold,
        "missing_threshold": missing_threshold,
        "impute_strategy": impute_strategy,
        "drop_categorical_columns": drop_categorical_columns,
        "drop_highly_correlated": drop_highly_correlated,
        "drop_columns": drop_columns,
        "scale_method": scale_method,
        "feature_selection": feature_selection,
        "balance_method": balance_method,
        "assess_only": assess_only
    }
    update_report(report, "Options Used", f"```{options_used}```")

    if drop_columns:
        drop_columns = [col.strip() for col in drop_columns.split(',')]

    # Load dataset
    df = pd.read_csv(file_path)
    dataset_name = os.path.basename(file_path)
    num_records = len(df)

    update_report(report, "Dataset Loaded", f"\n✅ Dataset Loaded Successfully: `{os.path.abspath(file_path)}`\n"
                                           f"- File Size: {file_size_mb:.2f} MB\n"
                                           f"- Number of Records: {num_records}\n")
 
    if(assess_only):
        update_report(report, "Assessment Mode", f"🔍 Running in assessment-only mode. No changes applied to the dataset.")
        

    # **1. Drop Manually Specified Columns First**
    
        if drop_columns:
            drop_columns = [col.strip() for col in drop_columns]
            existing_cols = set(df.columns)
            valid_drop_cols = [col for col in drop_columns if col in existing_cols]
            invalid_drop_cols = [col for col in drop_columns if col not in existing_cols]
            if not assess_only:
                if valid_drop_cols:
                    df.drop(columns=valid_drop_cols, inplace=True)
                    update_report(report,"Explicitly Dropped Columns", f"🗑️ `{valid_drop_cols}` manually removed")

                if invalid_drop_cols:
                    update_report(report,"Invalid Columns (Not Found)", f"⚠️ `{invalid_drop_cols}` could not be found in the dataset")
            else:
                if valid_drop_cols:
                    update_report(report, "Explicitly Dropped Columns", f"🗑️ `{valid_drop_cols}` to be manually removed")
                    drop_cmd = f"df.drop(columns={valid_drop_cols}, inplace=True)"
                    update_report(report, "Python Command to Drop Columns", f"💡 To drop these columns, use:\n```python\n{drop_cmd}\n```")
                if invalid_drop_cols:
                    update_report(report, "Invalid Columns (Not Found)", f"⚠️ `{invalid_drop_cols}` could not be found in the dataset")

    # **2. Removing Leading Spaces in Feature Names**
    original_columns = df.columns.tolist()
    columns_with_spaces = [col for col in original_columns if col.strip() != col]
    

    if not assess_only:
        df.columns = df.columns.str.strip()

        if columns_with_spaces:
            update_report(report, "Leading Spaces in Feature Names", f"✅ Fixed: Spaces removed from {len(columns_with_spaces)} feature names: `{columns_with_spaces}`")
        else:
            update_report(report, "Leading Spaces in Feature Names", "No issues found")
    else:
        if columns_with_spaces:
            fix_command = "df.columns = df.columns.str.strip()"
            update_report(report, "Leading Spaces in Feature Names", f"⚠️ Found {len(columns_with_spaces)} columns with leading/trailing spaces: `{columns_with_spaces}`\n💡 To fix, use:\n``````")
        else:
            update_report(report, "Leading Spaces in Feature Names", "No issues found")

    # **3. Identifying Categorical Columns**
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if categorical_cols:
        update_report(report, "Categorical Columns", f"⚠️ Found {len(categorical_cols)} categorical columns: `{categorical_cols}`")
        if drop_categorical_columns:
            if not assess_only:
                df.drop(columns=categorical_cols, inplace=True)
                update_report(report, "Categorical Columns Removed", f"🗑️ Dropped `{categorical_cols}`")
        else:
            drop_cmd = f"df.drop(columns={categorical_cols}, inplace=True)"
            update_report(report, "Categorical Columns Check", 
                "No categorical columns removed (Flag `--drop_categorical_columns=False`).\n"
                f"💡 To drop them manually, use:\n```python\n{drop_cmd}\n```")

    # Convert numerical columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if assess_only:
        columns_to_exclude = set(drop_columns + categorical_cols if drop_columns else categorical_cols)
        numeric_cols = [col for col in numeric_cols if col not in columns_to_exclude]
    df_numeric = df[numeric_cols]


    # **4. Analyzing Zero Variance Columns**
    zero_variance_cols = [col for col in df_numeric.columns if df_numeric[col].nunique() == 1]
    if zero_variance_cols:
        if not assess_only:
            df_numeric.drop(columns=zero_variance_cols, inplace=True)
            update_report(report, "Zero Variance Columns", f"🗑️ {len(zero_variance_cols)} columns removed: `{zero_variance_cols}`")
        else:
            drop_cmd = f"df_numeric.drop(columns={zero_variance_cols}, inplace=True)"
            update_report(report, "Zero Variance Columns", f"⚠️ Found {len(zero_variance_cols)} zero variance columns: `{zero_variance_cols}`\n💡 To drop these columns, use:\n```python\n{drop_cmd}```")
    else:
        update_report(report, "Zero Variance Columns", "No issues found")


    # **5. Handling Negative Values**
    negative_values_count = (df_numeric < 0).sum().sum()
    if negative_values_count > 0:
        if not assess_only:
            df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
            update_report(report, "Negative Values", f"✅ {negative_values_count} negative values found and replaced with zero")
        else:
            columns_with_negatives = df_numeric.columns[df_numeric.lt(0).any()].tolist()
            replace_cmd = "df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)"
            update_report(report, "Negative Values", f"⚠️ Found {negative_values_count} negative values in columns: `{columns_with_negatives}`\n💡 To replace with zero, use:\n```python\n{replace_cmd}\n```")
    else:
        update_report(report, "Negative Values", "No issues found")


    # **6. Handling Infinite Values**
    infinite_values_count = np.isinf(df_numeric).sum().sum()
    if infinite_values_count > 0:
        columns_with_inf = df_numeric.columns[np.isinf(df_numeric).any()].tolist()
        if not assess_only:
            df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
            update_report(report, "Infinite Values", f"⚠️ {infinite_values_count} infinite values found in columns `{columns_with_inf}` and replaced with NaN")
        else:
            replace_cmd = "df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)"
            update_report(report, "Infinite Values", f"⚠️ Found {infinite_values_count} infinite values in columns `{columns_with_inf}`.\n💡 To replace with NaN, use:\n```python\n{replace_cmd}\n```")
    else:
        update_report(report, "Infinite Values", "No issues found")
    

    # **7. Handling Missing Values**
    if impute_strategy:
        missing_values_count = df_numeric.isnull().sum().sum()
        if missing_values_count > 0:
            if not assess_only:
                imputer = SimpleImputer(strategy=impute_strategy)
                df_numeric.loc[:, df_numeric.columns] = imputer.fit_transform(df_numeric)
                update_report(report, "Missing Values", f"✅ {missing_values_count} missing values found and imputed with `{impute_strategy}` strategy")
            else:
                impute_cmd = f"imputer = SimpleImputer(strategy='{impute_strategy}')\ndf_numeric.loc[:, df_numeric.columns] = imputer.fit_transform(df_numeric)"
                update_report(report, "Missing Values", f"⚠️ Found {missing_values_count} missing values.\n💡 To impute with '{impute_strategy}' strategy, use:\n```python\n{impute_cmd}\n```")
        else:
            update_report(report, "Missing Values", "No issues found")


    # **8. Removing Highly Correlated Features**
    correlation_matrix = df_numeric.corr().abs()
    upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
    correlated_features = {col for col in upper_triangle.columns if any(upper_triangle[col] > correlation_threshold)}

    if not assess_only:
        if drop_highly_correlated:
            df_numeric.drop(columns=list(correlated_features), inplace=True)
            update_report(report, "Highly Correlated Features", f"🗑️ {len(correlated_features)} highly correlated features removed: `{list(correlated_features)}`")
        else:
            update_report(report, "Highly Correlated Features", f"⚠️ {len(correlated_features)} highly correlated features detected. Use:\n``````")
    else:
        drop_cmd = f"df_numeric.drop(columns={list(correlated_features)}, inplace=True)"
        update_report(report, "Highly Correlated Features", f"⚠️ Found {len(correlated_features)} highly correlated features (threshold: {correlation_threshold}).\n💡 To drop these features, use:\n```python\n{drop_cmd}\n```")


    # **9. Feature Scaling**
    current_cols = df_numeric.columns.tolist()
    columns_to_keep = [col for col in current_cols if col not in correlated_features]
    df_numeric = df_numeric[columns_to_keep]

    need_scaling = any(df_numeric.std() > 1)
    if need_scaling:
        if scale_method:
            if not assess_only:
                scaler = {'minmax': MinMaxScaler(), 'standard': StandardScaler(), 'robust': RobustScaler()}.get(scale_method)
                if scaler:
                    df_numeric.loc[:, df_numeric.columns] = scaler.fit_transform(df_numeric)
                    update_report(report, "Feature Scaling", f"✅ Applied `{scale_method}` scaling")
                else:
                    update_report(report, "Feature Scaling", f"⚠️ Invalid scaling method '{scale_method}' specified")
            else:
                scale_cmd = f"scaler = {scale_method.capitalize()}Scaler()\ndf_numeric.loc[:, df_numeric.columns] = scaler.fit_transform(df_numeric)"
                update_report(report, "Feature Scaling", f"⚠️ Scaling recommended. To apply `{scale_method}` scaling, use:\n```python\n{scale_cmd}\n```")
        else:
            update_report(report, "Feature Scaling", "⚠️ Scaling recommended but no method specified")
    else:
        update_report(report, "Feature Scaling", "✅ No scaling needed (standard deviation ≤ 1 for all features)")

    # **10. Feature Selection**
    if feature_selection == 'variance':
        if not assess_only:
            selector = VarianceThreshold(threshold=0.01)
            df_numeric = pd.DataFrame(selector.fit_transform(df_numeric), columns=df_numeric.columns[selector.get_support()])
            update_report(report, "Feature Selection", "✅ Low variance features removed")
        else:
            # Calculate variances without applying the transformation
            variances = df_numeric.var()
            low_variance_features = variances[variances <= 0.01].index.tolist()
            if low_variance_features:
                update_report(report, "Feature Selection", f"⚠️ Found {len(low_variance_features)} low variance features that could be removed: `{low_variance_features}`")
                update_report(report, "Feature Selection Command", "💡 To remove low variance features, use:\n``````")
            else:
                update_report(report, "Feature Selection", "✅ No low variance features found. Feature selection may not be necessary.")
    elif feature_selection == 'pca':
        if not assess_only:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=pca_variance)
            df_numeric_pca = pd.DataFrame(pca.fit_transform(df_numeric))
            update_report(report, "Feature Selection", f"✅ Applied PCA with variance threshold {pca_variance}, reduced to {pca.n_components_} components")
        else:
            from sklearn.decomposition import PCA
            df_numeric_finite = df_numeric[~np.isinf(df_numeric).any(axis=1)]
            pca = PCA().fit(df_numeric_finite)
            cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
            
            n_components_95 = np.argmax(cumulative_variance_ratio >= 0.95) + 1
            n_components_99 = np.argmax(cumulative_variance_ratio >= 0.99) + 1
            n_components_999 = np.argmax(cumulative_variance_ratio >= 0.999) + 1

            original_features = df_numeric_finite.shape[1]
            
            pca_report = f"PCA analysis results:\n"
            pca_report += f"  - 95% variance retained with {n_components_95} components (reduced from {original_features} to {n_components_95})\n"
            pca_report += f"  - 99% variance retained with {n_components_99} components (reduced from {original_features} to {n_components_99})\n"
            pca_report += f"  - 99.9% variance retained with {n_components_999} components (reduced from {original_features} to {n_components_999})\n"

            if n_components_95 < df_numeric_finite.shape[1] or n_components_99 < df_numeric_finite.shape[1] or n_components_999 < df_numeric_finite.shape[1]:
                update_report(report, "Feature Selection", f"⚠️ {pca_report}")
                pca_cmd = f"df_numeric_finite = df_numeric[~np.isinf(df_numeric).any(axis=1)]\npca = PCA(n_components={n_components_95})\ndf_numeric_pca = pd.DataFrame(pca.fit_transform(df_numeric_finite))"
                update_report(report, "Feature Selection Command", f"💡 To apply PCA, use:\n```python\n{pca_cmd}\n```")
            else:
                update_report(report, "Feature Selection", "✅ PCA may not be beneficial as all components are needed to retain the specified variance")

    # **11. Class Balancing**
    if balance_method:
        target_col = "Label"  # Modify as per dataset's class label column
        if target_col in df_numeric.columns:
            X, y = df_numeric.drop(columns=[target_col]), df_numeric[target_col]
            if balance_method == "smote":
                sampler = SMOTE()
            elif balance_method == "undersample":
                sampler = RandomUnderSampler()
            X_resampled, y_resampled = sampler.fit_resample(X, y)
            df_numeric = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.DataFrame(y_resampled, columns=[target_col])], axis=1)
            update_report(report, "Class Balancing", f"✅ Applied `{balance_method}` balancing")

    # **12. Report Available Columns**
    available_columns = df_numeric.columns.tolist()
    update_report(report, "Available Columns", f"After cleaning, the following columns are available: `{available_columns}`")

    # **13. Recommendation**
    recommendation = (
        "Based on the assessment, it is recommended to continue working with the available columns. "
        "You may consider the following:\n"
        f"- Performing further analysis using the available columns: `{available_columns}`\n"
        "- Training machine learning models with the reduced feature set."
    )

    available_columns = df_numeric.columns.tolist()

    # Create a markdown table for the report
    markdown_table = "| # | Column Name | Mapping |\n"
    markdown_table += "|---|---|---|\n"

    for index, column_name in enumerate(available_columns):
        # Create a clean column name for mapping
        mapped_column_name = column_name.lower().replace(" ", "_")

        # Add row to the markdown table
        markdown_table += f"| {index + 1} | {column_name} | {mapped_column_name} |\n"

    update_report(report, "Available Columns and Recommended Mapping", f"The following columns are available after cleaning. Recommended mapping:\n{markdown_table}")
    update_report(report, "Recommendation", recommendation)

    # **12. Save Cleaned Dataset**
    if not assess_only:
        cleaned_file_path = os.path.join(output_path, f"cleaned_{dataset_name}")
        df_numeric.to_csv(cleaned_file_path, index=False)
        update_report(report, "Save Cleaned Dataset", f"\n✅ Cleaned dataset saved as '{cleaned_file_path}'")

    # **13. Save Markdown Report**
    file_name_without_extension = os.path.splitext(dataset_name)[0]
    report_path = os.path.join(output_path, f"report_{file_name_without_extension}.md")
    with open(report_path, "w") as f:
        f.write(f"# Data Cleaning Report: `{dataset_name}`\n\n")
        for key, value in report.items():
            f.write(f"- **{key}**: {value}\n")

    print(f"📄 Cleaning report saved as '{report_path}'")

def update_report(report, key, value):
    report[key] = value
    print(f"- {key}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and preprocess IDS datasets")
    parser.add_argument("file_path", type=str, help="Path to the dataset CSV file")
    parser.add_argument("output_path", type=str, help="Path to save cleaned dataset")
    parser.add_argument("--drop-columns", type=str, help="Comma-separated list of columns to drop")
    parser.add_argument("--drop-categorical-columns", action="store_true", help="Drop categorical columns")
    parser.add_argument("--drop-highly-correlated", action="store_true", help="Drop highly correlated columns")
    parser.add_argument("--scale-method", type=str, choices=["minmax", "standard", "robust"], help="Feature scaling method")
    parser.add_argument("--feature-selection", type=str, choices=["variance", "correlation", "mutual_info", "chi2", "rfe", "pca"], help="Feature selection method")
    parser.add_argument("--impute-strategy", type=str, choices=["mean", "median", "knn"], default="mean", help="Imputation strategy")
    parser.add_argument("--balance-method", type=str, choices=["smote", "undersample"], help="Class balancing method")
    parser.add_argument("--assess-only", action="store_true", help="Perform assessment without applying changes")
    parser.add_argument("--correlation-threshold", type=float, default=0.9, help="Threshold for correlation analysis")
    parser.add_argument("--pca-variance", type=float, default=0.95, help="Variance threshold for PCA (default: 0.95)")

    args = parser.parse_args()
    clean_dataset(**vars(args))
