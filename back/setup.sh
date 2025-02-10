#!/bin/bash

# Define the project directory
PROJECT_DIR="$(pwd)"

# Create the run.sh script
echo "Creating run.sh script..."

cat <<EOL > "$PROJECT_DIR/run.sh"
#!/bin/bash

# Activate the virtual environment (optional)
source venv/bin/activate

# Start Daphne (replace with your ASGI app)
exec env $(cat ./environment | xargs) daphne -b 0.0.0.0 -p 8000 back.asgi:application

EOL

# Make run.sh executable by everyone
chmod +x "$PROJECT_DIR/run.sh"
chmod a+x "$PROJECT_DIR/run.sh"  # This allows everyone to execute it

# Create the systemd service file
echo "Creating emishop.service..."

cat <<EOL | sudo tee /etc/systemd/system/emishop.service > /dev/null
[Unit]
Description=EmiShop Django Application (Daphne)
After=network.target

[Service]
ExecStart=$PROJECT_DIR/run.sh
WorkingDirectory=$PROJECT_DIR
Restart=always
EnvironmentFile=/etc/environment

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to apply the changes
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start at boot
echo "Enabling emishop service to start on boot..."
sudo systemctl enable emishop

# Start the service
echo "Starting emishop service..."
sudo systemctl start emishop

# Show the status of the service
sudo systemctl status emishop
