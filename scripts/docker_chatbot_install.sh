# It will do the following operations:
# 1. Install Docker
# 2. Enable and start docker service
# 3. Install docker-compose


# 1. Install Docker
sudo apt-get remove docker docker-engine docker.io containerd runc

# Set up the docker repository
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


#Install docker engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# 2.  Enable and start docker service
sudo systemctl enable docker.service
sudo systemctl start docker.service


# 3. Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# Make docker-compose binary executable
sudo chmod +x /usr/local/bin/docker-compose



