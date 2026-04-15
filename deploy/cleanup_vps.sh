#!/bin/bash

echo "=== VPS Cleanup Script ==="
echo "Starting cleanup..."

# Show disk usage before
echo ""
echo "Disk usage BEFORE:"
df -h /

# Clean apt cache
echo ""
echo "Cleaning apt cache..."
sudo apt clean
sudo apt autoremove -y

# Clean journal logs (keep last 1 day)
echo ""
echo "Cleaning system logs..."
sudo journalctl --vacuum-time=1d
sudo rm -rf /var/log/*.gz
sudo rm -rf /var/log/*.1
sudo rm -rf /var/log/*.old

# Clean Docker
echo ""
echo "Cleaning Docker..."
sudo docker system prune -a --volumes -f

# Clean pip cache
echo ""
echo "Cleaning pip cache..."
pip cache purge 2>/dev/null || true
sudo pip cache purge 2>/dev/null || true

# Clean Python packages in /usr/local (if confirmed)
echo ""
read -p "Delete global Python packages in /usr/local/lib/python3.11? (y/N): " confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo "Removing global Python packages..."
    sudo rm -rf /usr/local/lib/python3.11/site-packages/*
fi

# Clean tmp files
echo ""
echo "Cleaning /tmp..."
sudo rm -rf /tmp/*

# Clean home caches
echo ""
echo "Cleaning user caches..."
sudo rm -rf /home/*/\.cache/*
sudo rm -rf /root/\.cache/*

# Clean Downloads folders
echo ""
echo "Cleaning Downloads folders..."
sudo rm -rf /home/*/Downloads/*
sudo rm -rf /root/Downloads/*

# Clean old venv folders in sagatoy
echo ""
echo "Cleaning old venv folders in sagatoy..."
sudo rm -rf /var/www/sagatoy/venv
sudo rm -rf /var/www/sagatoy/backend/venv
sudo rm -rf /var/www/sagatoy/backend/.mypy_cache
sudo rm -rf /var/www/sagatoy/backend/.pytest_cache

# Clean snap old versions
echo ""
echo "Cleaning snap old versions..."
sudo snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        sudo snap remove "$snapname" --revision="$revision"
    done

# Show disk usage after
echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Disk usage AFTER:"
df -h /

echo ""
echo "Top space usage:"
sudo du -sh /* 2>/dev/null | sort -rh | head -10
