# locals are constants
locals {
  data_lake_bucket = "dtc_data_lake"
}

# variables can change
# variables with 'default' are optional runtime arguments
# variables without 'default' are mandatory runtime arguments
variable "gcp_project_id" {
  description = "Your GCP Project ID"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "gcs_storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "bq_dataset_id" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data_all"
}