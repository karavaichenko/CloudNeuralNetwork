## Quick start

Install python requirements and rabbitMQ    
`pip3 install req.txt`  
`sh rabbitInstall.sh`   
Run celery worker and flower    
`cd src`    
`celery -A celeryConf worker --loglevel=info`   
`celery -A celeryConf flower`
