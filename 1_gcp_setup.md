# Initial Setup

1. Create a Google Cloud account

2. Download Google Cloud SDK

3. Create a project in the console

4. Create a service account and give it `Viewer` role

5. Go to `manage keys` and donwload the `.json` file

6. Authenticate key with GCP

   export GOOGLE_APPLICATION_CREDENTIALS="<path_to_json>"
   
   gcloud auth application-default login
   
# Setup for Access
 
1. Grant service permissions for service account:
   * Go to the `IAM` section of `IAM & Admin`
   * Click the `Edit principal` icon for your service account
   * Add these roles in addition to `Viewer`: `Storage Admin`, `Storage Object Admin`, `BigQuery Admin`
   
2. Enable these APIs for your project:
   
   https://console.cloud.google.com/apis/library/iam.googleapis.com
   https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
