# Models Directory

The `.pkl` model files in this directory are **not committed to git** because they are binary artifacts that can be fully reproduced locally.

## How to generate the models

1. Download `results.csv` from [Kaggle — International Football Results 1872–2024](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)
2. Place the file at `data/results.csv`
3. Run the training pipeline:

```bash
python src/prepare_data.py
python src/model_training.py
```

This will produce:

| File | Description |
|------|-------------|
| `match_predictor.pkl` | Trained RandomForest classifier for match outcome prediction |
| `feature_scaler.pkl` | StandardScaler fitted on training features |
| `model_metrics.json` | Accuracy, classification report, and cross-validation scores |

## Notes

- Training data covers 49,329 international matches
- Model achieves ~60–65% accuracy on held-out test set
- IBM watsonx.ai (Granite) is used at inference time for natural-language explanations; the `.pkl` files handle the numeric prediction only
