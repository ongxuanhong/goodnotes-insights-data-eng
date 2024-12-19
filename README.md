# Note-Taking App Analytics Pipeline

## Overview
This documentation outlines my solution for processing and analyzing user interaction data. The pipeline is built using Apache Spark and follows a modern data lakehouse architecture with bronze, silver, and gold layers for optimal data processing and analytics.

## Data Architecture

![Data architecture diagram](diagrams/figures/data_architecture.png)

### Storage
- **Storage System**: MinIO (S3-compatible storage)
- **Data Format**: Parquet (columnar storage)
- **Partitioning Strategy**: 
  - Interactions data: Partitioned by date
  - User metadata: Partitioned by country

### Data Layers
1. **Bronze Layer**: Raw data ingested from CSV sources
2. **Silver Layer**: Cleaned and transformed data in fact/dimension model
3. **Gold Layer**: Pre-aggregated metrics and analytics

### Scalability Features

1. **Efficient Data Storage**
   - Parquet format for columnar compression
   - Date-based partitioning for quick data access
   - Partition pruning during query execution

2. **Incremental Processing**
   - Daily incremental updates instead of full reprocessing
   - Lookback windows for handling period boundaries
   - Partition-based writes for atomic updates

3. **Performance Optimizations**
   - Pre-aggregated metrics in gold layer
   - Broadcast joins for dimension tables
   - Caching of frequently accessed DataFrames

### Usage

1. **Daily Processing**
```python
etl = DataLakehouseETL()
metrics = etl.create_gold_layer(datetime.now().date())
```

2. **Historical Backfill**
```python
etl.backfill_gold_metrics(
    start_date=datetime(2023, 1, 1).date(),
    end_date=datetime(2023, 12, 31).date(),
    parallel=True
)
```

## Tasks

1. Calculate Daily Active Users (DAU) and Monthly Active Users (MAU) for the past year:
   - Define clear criteria for what constitutes an "active" user
   - Implement a solution that scales efficiently for large datasets
   - [Optional] Explain how you:
     - Handle outliers and extremely long duration values, OR
     - Describe challenges you might face while creating similar metrics and how you would address them

2. Calculate session-based metrics:
   - Calculate metrics including:
     - Average session duration
     - Actions per session
   - Define clear criteria for what constitutes a "session"
   - [Optional] Provide analysis of the results if time permits