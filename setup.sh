python3 -m venv venv
while !find venv; do
    sleep 1
done
source venv/bin/activate
pip3 install -r requirements.txt