# Remove the current cifar10-csv/ if it exists
rm -rf cifar10-csv/

# Download the file and save it in the current directory
wget --quiet -O cifar10-csv.zip https://activeeon-public.s3.eu-west-2.amazonaws.com/datasets/cifar10-csv.zip

# Create the target subfolder if it doesn't exist
mkdir -p cifar10-csv

# Unzip the content into the specified subfolder
unzip cifar10-csv.zip -d cifar10-csv

# Remove the downloaded zip file
rm -f cifar10-csv.zip
