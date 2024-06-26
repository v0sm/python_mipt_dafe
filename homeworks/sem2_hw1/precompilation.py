import numpy as np


class ShapeMismatchError(Exception):
    pass


def train_test_split(
    features: np.ndarray,
    targets: np.ndarray,
    shuf: bool,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if features.shape[0] != targets.shape[0]:
        raise ShapeMismatchError(
            f"Features shape {features.shape[0]} != targets shape {targets.shape[0]}"
        )

    if shuf:
        indices = np.arange(features.shape[0])
        np.random.shuffle(indices)
        features = features[indices]
        targets = targets[indices]

    unique_targets, targets_count = np.unique(targets, return_counts=True)

    features_train, features_test, targets_train, targets_test = [], [], [], []

    for target_index, target in enumerate(unique_targets):
        target_mask = targets == target
        target_features = features[target_mask]
        train_count = int(targets_count[target_index] * train_ratio)

        features_train.append(target_features[:train_count])
        features_test.append(target_features[train_count:])
        targets_train.append(np.full(train_count, target))
        targets_test.append(np.full(targets_count[target_index] - train_count, target))

    features_train = np.concatenate(features_train, axis=0)
    features_test = np.concatenate(features_test, axis=0)
    targets_train = np.concatenate(targets_train, axis=0)
    targets_test = np.concatenate(targets_test, axis=0)

    return features_train, features_test, targets_train, targets_test
