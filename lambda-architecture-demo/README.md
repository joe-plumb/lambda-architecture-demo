# lambda-architecture-demo
This is a work in progress repo that aims to build out a technical foundation of lab exersizes and examples to demonstrate integration of data services in Azure.

## Pre-requistes
- Install Docker in your local environment
	- [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
	- [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- Clone this GitHub repo into your local environment

## Setup
This demo repo is a work in progress. It currently contains a _containerized producer to run locally_ to publish messages onto _Event Hubs_. To get started, clone the repo to your machine and follow the below steps:
0. Provision an Event Hub namespace and Event Hub in your Azure environment. Guidance for doing this can be found in [the documentation](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).
1. Create a `config.py` file in the folder using `config-template.py` for guidance. This makes the required secrets to allow the producer application to communicate with the Event Hub.
2. Build the Docker container `docker build -t yourusername/repository-name .` (the full stop is important!)
3. Run the Docker container `docker run yourusername/repository-name`. You will now see the events being generated on `stdout`. Navigate to your Event Hub in the [Azure Portal](https://portal.azure.com/) to see the traffic.

## TODO
- Integrate producer code with MSI for remote execution of docker container
- Integrate Event Hub with downstream processing with:
	- Azure Databricks
	- Azure Stream Analytics
- Develop Power BI front end for visualisation of data