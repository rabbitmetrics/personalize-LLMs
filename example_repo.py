from datetime import timedelta

import pandas as pd

from feast import (
    BigQuerySource,
    Entity,
    FeatureService,
    FeatureView,
    Field,
    PushSource,
    RequestSource,
)
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32, Float64, Int64, String


PROJECT_ID="..."
BIGQUERY_DATASET_NAME="..."
FEATURE_TABLE='...'

# Define an entity for the driver. You can think of an entity as a primary key used to
# fetch features.
customer = Entity(name="customer", join_keys=["email"])

# Defines a data source from which feature values can be retrieved. Sources are queried when building training
# datasets or materializing features into an online store.
feature_source = BigQuerySource(
    name="incentive_features",
    # The BigQuery table where features can be found
    table=f"{PROJECT_ID}.{BIGQUERY_DATASET_NAME}.{FEATURE_TABLE}",
    # The event timestamp is used for point-in-time joins and for ensuring only
    # features within the TTL are returned
    timestamp_field="feature_timestamp",
    # The (optional) created timestamp is used to ensure there are no duplicate
    # feature rows in the offline store or when building training datasets
    created_timestamp_column="created"
)

# Feature views are a grouping based on how features are stored in either the
# online or offline store.
incentives_fv = FeatureView(
    # The unique name of this feature view. Two feature views in a single
    # project cannot have the same name
    name="incentives",
    # The list of entities specifies the keys required for joining or looking
    # up features from this feature view. The reference provided in this field
    # correspond to the name of a defined entity (or entities)
    entities=[customer],
    # The timedelta is the maximum age that each feature value may have
    # relative to its lookup time. For historical features (used in training),
    # TTL is relative to each timestamp provided in the entity dataframe.
    # TTL also allows for eviction of keys from online stores and limits the
    # amount of historical scanning required for historical feature values
    # during retrieval
    ttl=timedelta(weeks=52 * 10),  # Set to be very long for example purposes only
    # The list of features defined below act as a schema to both define features
    # for both materialization of features into a store, and are used as references
    # during retrieval for building a training dataset or serving features
    schema=[
        Field(name="incentive", dtype=String),
        Field(name="first_name", dtype=String),
        Field(name="last_name", dtype=String),
    ],
    source=feature_source
)






