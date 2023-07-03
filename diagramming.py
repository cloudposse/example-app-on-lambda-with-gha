from diagrams import Cluster, Diagram
from diagrams.onprem.vcs import Github
from diagrams.oci.compute import Container
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3, SimpleStorageServiceS3Object as S3Object
from diagrams.aws.management import SSM

with Diagram("Publish Lambda", show=False):
    auto = Cluster("core-auto")
    artifacts = Cluster("core-artifacts")

    with artifacts:
        artifacts_bucket = S3("lambda artifacts")

    with Cluster("SSM parameters"):
        with Cluster("plat-dev"):
            dev_lambda_tag = SSM("/lambda/hello/tag")
        with Cluster("plat-staging"):
            staging_lambda_tag = SSM("/lambda/hello/tag")
        with Cluster("plat-prod"):
            prod_lambda_tag = SSM("/lambda/hello/tag")

    with auto:
        publish = Container("publish")
        promote = Container("promote")

    pr = Github("PR #1234")
    push = Github("push -> main")
    release = Github("release")
    
    # use undirected edges to show succession
    dev_lambda_tag - staging_lambda_tag - prod_lambda_tag
    
    # a pr will cause a publish, which puts a zip into the staging bucket and sets the tag
    pr >> publish >> [artifacts_bucket, dev_lambda_tag]
    push >> publish >> [artifacts_bucket, staging_lambda_tag]

    # a push to main will cause a promote, which copies the zip from staging to prod and sets the tag
    release >> promote << [artifacts_bucket, staging_lambda_tag]
    promote >> [artifacts_bucket, prod_lambda_tag]
