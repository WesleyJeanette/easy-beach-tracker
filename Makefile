# Variables
IMAGE_NAME = easy-beach-tracker
CONTAINER_NAME = easy-beach-tracker-container
PORT = 8023

run-local:
	python manage.py runserver 0.0.0.0:$(PORT)

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Rebuild the Docker image and run the container
rebuild: stop build run

# Clean up dangling Docker images
clean:
	docker rmi $(IMAGE_NAME) || true
	docker image prune -f