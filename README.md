This guide walks you through setting up an IAM user, configuring AWS on your machine, deploying infrastructure with Terraform, running a CPU stress test, and watching your Auto Scaling Group kick into action. When you're done, you’ll clean everything up so you’re not billed for anything you don't need.

Let’s get into it.

1. Create an IAM User in AWS

Log in to the AWS Management Console using your cloud_user account.

Search for IAM and open it.

Go to Users → Create user.

Step 1: User Details

Username: admin-user

Click Next

Step 2: Permissions

Select Attach policies directly

Search for AdministratorAccess and check it

Hit Next

Step 3: Review

Click Create user

Done!

2. Generate Access Keys

In the Users list, click on admin-user.

Choose Create access key.

Select Local code, confirm the checkbox, and continue.

For the description, put admin_key.

Click Create access key.

Copy the Access Key and Secret Access Key somewhere safe — you’ll need them soon.

(These keys are temporary, so don’t worry.)

3. Clone the Project and Set Up AWS CLI

Make sure you have Terraform, Git, the AWS CLI, and a code editor installed.

Clone the repo:

git clone https://github.com/pluralsight-cloud/Deploying-an-Auto-Scaling-Group-and-Load-Balancer-on-AWS-with-Terraform.git


Jump into the directory:

cd Deploying-an-Auto-Scaling-Group-and-Load-Balancer-on-AWS-with-Terraform


Set up your AWS credentials:

aws configure


When asked:

Access Key: paste it

Secret Access Key: paste that too

Default region: us-east-1

Output format: just press Enter

4. Initialize Terraform

Run:

terraform init


This sets up the Terraform environment and downloads needed providers.

5. Preview What Terraform Will Build

Before you create anything, take a look at the plan:

terraform plan


Terraform will show you everything it’s about to create. Give it a quick look so there are no surprises.

6. Deploy the Infrastructure

Now run:

terraform apply


Type yes when it asks for confirmation.

Terraform will build out the VPC, subnets, Auto Scaling Group, load balancer, and the rest of the setup.

7. Connect to an EC2 Instance

Head to the EC2 Dashboard.

Find one of the instances created by the Auto Scaling Group (look for the name pluralsight-asg).

Select the instance → click Connect

Choose EC2 Instance Connect to open a browser-based SSH session.

8. Run a CPU Stress Test

Python 3 is already installed on the instance, so you’re good to go.

Create a script:

nano stress_test.py


Paste this code:

import multiprocessing
import time

def cpu_stress():
    while True:
        pass

if __name__ == "__main__":
    num_cores = multiprocessing.cpu_count()
    processes = []

    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)

    time.sleep(180)

    for p in processes:
        p.terminate()


Save and exit:
Ctrl + X → Y → Enter

Run it:

python3 stress_test.py


This will max out the CPU for 3 minutes — plenty of time to trigger scaling.

9. Watch Auto Scaling in Action

In CloudWatch, open the cpu_high alarm. You should see a big spike when the stress test runs.

Go back to the EC2 dashboard — you’ll notice a third instance appear shortly.

In Auto Scaling Groups, open your group → go to Activity → scroll to Activity History to see the scaling events.

10. Clean Everything Up

When you’re done testing:

terraform destroy
