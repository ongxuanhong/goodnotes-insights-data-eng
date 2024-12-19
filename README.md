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

## Active User Metrics

### Definition of Active Users

An "active user" is defined as a unique user who performed at least one of these actions within the measurement period:
- Page view
- Edit
- Create
- Delete
- Share

### Metrics Calculation

#### Daily Active Users (DAU)
```sql
SELECT 
    partition_date,
    COUNT(DISTINCT user_id) as daily_active_users
FROM fact_interactions
GROUP BY partition_date
```

#### Monthly Active Users (MAU)
```sql
SELECT 
    DATE_TRUNC('month', partition_date) as month_date,
    COUNT(DISTINCT user_id) as monthly_active_users
FROM fact_interactions
GROUP BY DATE_TRUNC('month', partition_date)
```

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