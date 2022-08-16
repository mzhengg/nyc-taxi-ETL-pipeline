# terraform with google cloud infrastructure 

# set up terraform by establishing version, backend, and libraries
terraform {
  required_version = ">= 1.0"
  backend "local" {} # can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source = "hashicorp/google" # imports the google library
    }
  }
}

# terraform relies on plugins called providers to interact with cloud providers
# these plugins add predefined resource types and data sources that terraform can manage
provider "google" {
  project = var.gcp_project_id
  region = var.region
  // credentials = file(var.credentials)  # use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# creates a google storage bucket (data lake)
# ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name = "${local.data_lake_bucket}_${var.gcp_project_id}" # concatenating DL bucket & project name for unique naming
  location = var.region

  # optional, but recommended settings:
  storage_class = var.gcs_storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }

  force_destroy = true
}

# creates a google bigquery dataset (data warehouse)
# ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_id
  project = var.gcp_project_id
  location = var.region
}
