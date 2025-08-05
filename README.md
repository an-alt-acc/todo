# AWS TODO app
## AWS Architecture
- 1 CodePipeline pipeline comprising
  - Source: from this GitHub repo / your fork of it
    - Set to full clone
  - Test: CodeBuild project pointing to `buildspec-test.yml` to run `pytest` on the app
    - Allow the CodeBuild project's service role to create, edit and delete DynamoDB tables
  - Build: CodeBuild project pointing to `buildspec-build.yml` to build the app with the `Dockerfile` and publish it onto ECR
    - Allow the CodeBuild project's service role to upload new images onto ECR
    - Enable privileged access
    - Set the following environment variables:
      - `AWS_REGION` to your AWS region
      - `AWS_ACCOUNT_ID` to your account ID
      - `ECR_REPO_NAME` to the repository **name** in ECR
- 1 ECR repository (take note of the image URI)
- 1 DynamoDB table (take note of the table name)
- 1 ECS cluster with 1 service
  - References 1 Task Definition
    - Task role should allow read and write access to the above DynamoDB table
    - Image URI should reference the ECR repository, with tag `latest`
    - Container port is port 5000
    - Set environment variable `TABLE_NAME` to your DynamoDB table name
    - Set environment variable `REGION` to your AWS region
  - _n_ desired tasks (we chose _n_=3)
  - 1 Application Load Balancer on a VPC with _n_ public subnets across _n_ AZs
    - Listen on port 80 and set target group port to 5000
  
Upon commit push, CodePipeline will detect the pushes and test, build and upload the Docker image automatically. Manual approval ("quick service update") will be required on ECS to deploy the latest image.

## Development
To set up your environment, (create a virtual environment and) run `pip install -r requirements/dev.txt`

Run `python app.py` to start the application. Set your AWS access key environment variables (there are 3 of them) and optionally `PORT` (default 5000)

Run `pytest` to test. This also requires AWS access keys