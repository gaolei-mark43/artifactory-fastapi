
#!/bin/bash

# Kill existing process
pid=$(ps aux | grep repoAPI.py | grep -v grep | awk '{print $2}')
if [[ -n $pid ]]; then
    kill $pid
fi

# Start new process
nohup python3.10 repoAPI.py > logs/repoAPI.log 2>&1 &


