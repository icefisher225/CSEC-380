### Project Description
This project sets up a Web App environment with two instances of the Damn Vulnerable Web Application. The instance on port 8080 (HTTP) is protected by ModSecurity. The instances on port 443 (HTTPS) are load-balanced by NGINX. 

#### Components:
1. **DVWA**: Two instances of the Damn Vulnerable Web App (DVWA) are set up using the `vulnerables/web-dvwa` image. 
2. **ModSecurity**: A web app firewall service that uses the `owasp/modsecurity-crs:nginx` image. It listens on port `8080`. 
3. **NGINX**: A web server that uses the `nginx:latest` docker image. It listens for HTTPS requests on port `443` and serves two DVWA instances behing a reverse proxy. Load balancing is enabled. 

---

### Prerequisites: Installing Docker and Docker-Compose

1. **Install Docker**:
   - For most operating systems, you can follow the official [Docker installation guide](https://docs.docker.com/get-docker/).
   - For RHEL (Red Hat Enterprise Linux), you can use the following commands:

     ```bash
     sudo yum install -y yum-utils
     sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
     sudo yum install docker-ce docker-ce-cli containerd.io
     sudo systemctl start docker
     ```

2. **Install Docker Compose**:
   - For most operating systems, follow the official [Docker Compose installation guide](https://docs.docker.com/compose/install/).
   - For RHEL, Docker Compose comes bundled with Docker, so there's no need for a separate installation.

---

### Deployment Instructions

1. Clone this repository or download the project files.
2. Navigate to the project directory in your terminal.
3. For most operating systems, run the following command to start the services:

```bash
docker-compose up
```

For RHEL, use:

```bash
docker compose up
```

4. Once the services are up:
   - Access the load-balanced DVWA application by visiting `https://localhost` in your browser.
   - Access the ModSecurity instance by visiting `http://localhost:8080`.

5. To stop the services:

   - For most operating systems:

     ```bash
     docker-compose down
     ```

   - For RHEL:

     ```bash
     docker compose down
     ```

---

### Notes

This document was generated with the help of ChatGPT. 