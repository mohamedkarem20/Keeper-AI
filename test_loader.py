from model_loader import get_metadata

metadata = get_metadata()

print("Numeric Features:")
print(metadata["numeric_features"])

print("\nNominal Features:")
print(metadata["nominal_features"])

print("\nOrdinal Features:")
print(metadata["ordinal_features"])