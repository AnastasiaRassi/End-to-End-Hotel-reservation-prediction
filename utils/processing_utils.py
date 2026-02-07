from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PowerTransformer
import pandas as pd
import numpy as np
import sys
from loguru import logger

from utils.custom_exception import CustomException


class RareCategoryGrouper(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=500):
        self.threshold = threshold
        self.category_mappings_ = {}
    
    def fit(self, X, y=None):
        try:
            logger.info(f"Fitting RareCategoryGrouper with threshold={self.threshold}")
            for col in X.columns:
                counts = X[col].value_counts()
                rare_cats = counts[counts < self.threshold].index.tolist()
                self.category_mappings_[col] = rare_cats
                logger.debug(f"{col}: rare categories = {rare_cats}")
            return self
        
        except Exception as e:
            logger.exception("Error in RareCategoryGrouper.fit")
            raise CustomException(e, sys)

    def transform(self, X):
        try:
            logger.info("Transforming data with RareCategoryGrouper")
            X_copy = X.copy()
            for col, rare_cats in self.category_mappings_.items():
                X_copy[col] = X_copy[col].where(
                    ~X_copy[col].isin(rare_cats),
                    f'Other_{col}'
                )
                logger.debug(f"{col}: replaced {len(rare_cats)} rare categories with 'Other_{col}'")
            return X_copy
        
        except Exception as e:
            logger.exception("Error in RareCategoryGrouper.transform")
            raise CustomException(e, sys)


class TopNEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, n=3, prefix='category'):
        self.n = n
        self.prefix = prefix
        self.top_categories_ = None
        self.feature_names_ = None
    
    def fit(self, X, y=None):
        try:
            logger.info(f"Fitting TopNEncoder with top {self.n} categories")
            if isinstance(X, pd.DataFrame):
                X = X.iloc[:, 0]
            
            self.top_categories_ = X.value_counts().head(self.n).index.tolist()
            self.feature_names_ = [
                f"{self.prefix}_{cat.replace(' ', '_').lower()}"
                for cat in self.top_categories_
            ]
            logger.debug(f"Top categories: {self.top_categories_}")
            return self
        
        except Exception as e:
            logger.exception("Error in TopNEncoder.fit")
            raise CustomException(e, sys)
    
    def transform(self, X):
        try:
            logger.info("Transforming data with TopNEncoder")
            if isinstance(X, pd.DataFrame):
                X = X.iloc[:, 0]
            
            result = pd.DataFrame(index=X.index)
            for cat, feat_name in zip(self.top_categories_, self.feature_names_):
                result[feat_name] = (X == cat).astype(int)
                logger.debug(f"Encoded category '{cat}' into column '{feat_name}'")
            
            return result
        
        except Exception as e:
            logger.exception("Error in TopNEncoder.transform")
            raise CustomException(e, sys)


class SkewHandler(BaseEstimator, TransformerMixin):
    def __init__(self, skew_threshold=1.0):
        self.skew_threshold = skew_threshold
        self.skewness_ = {}
        self.transform_method_ = {}  # Track which transform per column
        self.power_transformers_ = {}  # Store fitted PowerTransformers
    
    def fit(self, X, y=None):
        try:
            logger.info(f"Fitting SkewHandler with skew_threshold={self.skew_threshold}")
            X_copy = X.copy()

            for col in X_copy.columns:
                col_skew = X_copy[col].skew()
                self.skewness_[col] = col_skew
                
                if col_skew > self.skew_threshold:
                    self.transform_method_[col] = 'log'
                elif col_skew < -self.skew_threshold:
                    self.transform_method_[col] = 'yeo-johnson'
                    pt = PowerTransformer(method='yeo-johnson')
                    pt.fit(X_copy[[col]])
                    self.power_transformers_[col] = pt
                else:
                    self.transform_method_[col] = 'none'
                
                logger.debug(f"{col}: skew={col_skew:.3f}, method={self.transform_method_[col]}")
            
            return self
        
        except Exception as e:
            logger.exception("Error in SkewHandler.fit")
            raise CustomException(e, sys)
    
    def transform(self, X):
        try:
            logger.info("Transforming data with SkewHandler")
            X_copy = X.copy()
            
            for col in X_copy.columns:
                method = self.transform_method_.get(col, 'none')
                if method == 'log':
                    X_copy[col] = np.log1p(X_copy[col])
                elif method == 'yeo-johnson':
                    pt = self.power_transformers_[col]
                    X_copy[col] = pt.transform(X_copy[[col]]).ravel()
                logger.debug(f"{col}: applied {method} transform")
            
            return X_copy
        
        except Exception as e:
            logger.exception("Error in SkewHandler.transform")
            raise CustomException(e, sys)
    
    def get_feature_names_out(self, input_features=None):
        try:
            if input_features is None:
                return list(self.transform_method_.keys())
            return list(input_features)
        
        except Exception as e:
            logger.exception("Error in SkewHandler.get_feature_names_out")
            raise CustomException(e, sys)
